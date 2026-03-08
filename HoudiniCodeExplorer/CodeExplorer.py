"""
This is 100% vibe coded from a basic demo I wrote a long time ago.
See the file CodeExplorerSession.md in the github repo here:
https://github.com/NCCA/PipelineAndTD/blob/main/HoudiniCodeExplorer/CodeExplorerSession.md
"""

from typing import Dict, List, Optional, Tuple

try:
    import hou
except ImportError:
    hou = None  # Allow linting outside Houdini
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt
from PySide6.QtGui import QPalette

from HouTextEditor import HoudiniTextEditor
from NodeTree import NodeTreeModel
from PythonHighlighter import PythonHighlighter

# ---------------------------------------------------------------------------
# Main dialog
# ---------------------------------------------------------------------------


class CodeExplorerDialog(QtWidgets.QDialog):
    """
    Main dialog window for the Code Explorer tool.

    Allows navigating the Houdini node tree and viewing the generated Python code
    (asCode) for selected nodes.

    Args:
        parent (Optional[QtWidgets.QWidget], optional): Parent widget. Defaults to None.
    """

    def __init__(self, parent: Optional[QtWidgets.QWidget] = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Code Explorer")
        self.resize(1100, 700)

        self._current_node: Optional["hou.Node"] = None
        self._ascode_opts: List[Tuple[str, str, str, bool]] = []

        # UI Elements (initialized in _build_ui)
        self._root_edit: Optional[QtWidgets.QLineEdit] = None
        self._refresh_btn: Optional[QtWidgets.QPushButton] = None
        self._copy_btn: Optional[QtWidgets.QPushButton] = None
        self._font_btn: Optional[QtWidgets.QPushButton] = None
        self._tree_view: Optional[QtWidgets.QTreeView] = None
        self._search_edit: Optional[QtWidgets.QLineEdit] = None
        self._search_prev_btn: Optional[QtWidgets.QPushButton] = None
        self._search_next_btn: Optional[QtWidgets.QPushButton] = None
        self._search_case_cb: Optional[QtWidgets.QCheckBox] = None
        self._search_count_label: Optional[QtWidgets.QLabel] = None
        self._editor: Optional[QtWidgets.QPlainTextEdit] = None
        self._highlighter: Optional[PythonHighlighter] = None
        self._status_label: Optional[QtWidgets.QLabel] = None
        self._font = None
        self._load_settings()

        self._build_ui()
        self._connect_signals()

    def _load_settings(self) -> None:
        """Load font settings from QSettings."""
        self._settings = QtCore.QSettings("NCCA", "CodeExplorer")
        self._settings.beginGroup("Font")
        name = self._settings.value("font-name", type=str, defaultValue="Courier New")
        size = self._settings.value("font-size", type=int, defaultValue=18)
        weight = self._settings.value("font-weight", type=int, defaultValue=50)
        italic = self._settings.value("font-italic", type=bool, defaultValue=False)
        self._settings.endGroup()
        self._font = QtGui.QFont(name, size)
        self._font.setWeight(QtGui.QFont.Weight(weight))
        self._font.setItalic(italic)

    # ------------------------------------------------------------------
    # UI construction
    # ------------------------------------------------------------------

    def _build_ui(self) -> None:
        """Construct the UI layout and widgets."""
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(6, 6, 6, 6)
        main_layout.setSpacing(4)

        # Toolbar row
        toolbar = QtWidgets.QHBoxLayout()
        self._root_edit = QtWidgets.QLineEdit("/")
        self._root_edit.setPlaceholderText("Root node path (e.g. /obj)")
        self._root_edit.setFixedWidth(200)
        self._refresh_btn = QtWidgets.QPushButton("Refresh Tree")
        self._copy_btn = QtWidgets.QPushButton("Copy Code")
        self._font_btn = QtWidgets.QPushButton("Font...")
        self._font_btn.setToolTip("Change the editor code font")
        toolbar.addWidget(QtWidgets.QLabel("Root:"))
        toolbar.addWidget(self._root_edit)
        toolbar.addWidget(self._refresh_btn)
        toolbar.addStretch()
        toolbar.addWidget(self._font_btn)
        self._save_btn = QtWidgets.QPushButton("Save")
        self._save_btn.setToolTip("Save code to file")
        toolbar.addWidget(self._save_btn)
        toolbar.addWidget(self._copy_btn)
        main_layout.addLayout(toolbar)

        # asCode options row
        # Each tuple: (attr_name, kwarg_name, label, default)
        # 'brief' is the inverse of verbose so handled separately.
        self._ascode_opts = [
            ("_cb_brief", "brief", "Brief", False),
            ("_cb_recurse", "recurse", "Recurse", False),
            ("_cb_channels_only", "save_channels_only", "Channels only", False),
            ("_cb_creation_cmds", "save_creation_commands", "Creation commands", True),
            ("_cb_keys_in_frames", "save_keys_in_frames", "Keys in frames", False),
            ("_cb_outgoing_wires", "save_outgoing_wires", "Outgoing wires", False),
            (
                "_cb_parm_values_only",
                "save_parm_values_only",
                "Parm values only",
                False,
            ),
            ("_cb_spare_parms", "save_spare_parms", "Spare parms", True),
            ("_cb_box_membership", "save_box_membership", "Box membership", True),
        ]
        opts_layout = QtWidgets.QHBoxLayout()
        opts_layout.setSpacing(10)
        opts_layout.addWidget(QtWidgets.QLabel("asCode:"))
        for attr, _kwarg, label, default in self._ascode_opts:
            cb = QtWidgets.QCheckBox(label)
            cb.setChecked(default)
            setattr(self, attr, cb)
            opts_layout.addWidget(cb)
        opts_layout.addStretch()
        main_layout.addLayout(opts_layout)

        # Splitter: tree on left, editor on right
        splitter = QtWidgets.QSplitter(Qt.Orientation.Horizontal)

        # Left: node tree
        self._tree_view = QtWidgets.QTreeView()
        self._tree_view.setHeaderHidden(True)
        self._tree_view.setMinimumWidth(260)
        self._tree_view.setAlternatingRowColors(True)
        splitter.addWidget(self._tree_view)

        # Right: search bar + code editor + status bar
        right_widget = QtWidgets.QWidget()
        right_layout = QtWidgets.QVBoxLayout(right_widget)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(2)

        # Search bar
        search_layout = QtWidgets.QHBoxLayout()
        search_layout.setSpacing(4)
        self._search_edit = QtWidgets.QLineEdit()
        self._search_edit.setPlaceholderText("Search code...  (Enter / Shift+Enter)")
        self._search_prev_btn = QtWidgets.QPushButton("▲")
        self._search_prev_btn.setFixedWidth(28)
        self._search_prev_btn.setToolTip("Previous match")
        self._search_next_btn = QtWidgets.QPushButton("▼")
        self._search_next_btn.setFixedWidth(28)
        self._search_next_btn.setToolTip("Next match")
        self._search_case_cb = QtWidgets.QCheckBox("Aa")
        self._search_case_cb.setToolTip("Case sensitive")
        self._search_count_label = QtWidgets.QLabel("")
        self._search_count_label.setStyleSheet("color: #888; min-width: 80px;")
        search_layout.addWidget(QtWidgets.QLabel("Find:"))
        search_layout.addWidget(self._search_edit, 1)
        search_layout.addWidget(self._search_prev_btn)
        search_layout.addWidget(self._search_next_btn)
        search_layout.addWidget(self._search_case_cb)
        search_layout.addWidget(self._search_count_label)
        right_layout.addLayout(search_layout)

        self._editor = HoudiniTextEditor()  # QtWidgets.QPlainTextEdit()
        self._editor.setReadOnly(True)
        self._editor.set_font(self._font)
        self._editor.document().setDefaultFont(self._font)
        # Dark background to match Houdini's script editor feel
        palette = self._editor.palette()
        palette.setColor(QPalette.ColorRole.Base, QtGui.QColor("#1E1E1E"))
        palette.setColor(QPalette.ColorRole.Text, QtGui.QColor("#D4D4D4"))
        self._editor.setPalette(palette)
        self._highlighter = PythonHighlighter(self._editor.document())

        self._status_label = QtWidgets.QLabel("")
        self._status_label.setStyleSheet("color: #888; font-size: 11px;")

        right_layout.addWidget(self._editor)
        right_layout.addWidget(self._status_label)
        splitter.addWidget(right_widget)

        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 3)
        main_layout.addWidget(splitter)

        # Populate tree with default root
        self._reload_tree()

    # ------------------------------------------------------------------
    # Signal wiring
    # ------------------------------------------------------------------

    def _connect_signals(self) -> None:
        """Connect UI signals to slots."""
        self._tree_view.selectionModel().currentChanged.connect(self._on_node_selected)
        self._refresh_btn.clicked.connect(self._reload_tree)
        self._copy_btn.clicked.connect(self._copy_code)
        self._font_btn.clicked.connect(self._choose_font)
        self._save_btn.clicked.connect(self._save_code)
        # Re-run asCode whenever any option checkbox changes
        for attr, _kwarg, _label, _default in self._ascode_opts:
            getattr(self, attr).stateChanged.connect(self._refresh_code)
        # Search
        self._search_edit.textChanged.connect(self._on_search_changed)
        self._search_edit.returnPressed.connect(self._search_next)
        self._search_edit.installEventFilter(self)
        self._search_next_btn.clicked.connect(self._search_next)
        self._search_prev_btn.clicked.connect(self._search_prev)
        self._search_case_cb.stateChanged.connect(self._on_search_changed)

    # ------------------------------------------------------------------
    # Slots
    # ------------------------------------------------------------------

    def _reload_tree(self) -> None:
        """Reload the node tree model based on the root path input."""
        if not hou:
            self._status_label.setText("Houdini module not found.")
            return

        root_path = self._root_edit.text().strip() or "/"
        node = hou.node(root_path)
        if node is None:
            self._status_label.setText(f"Node not found: {root_path}")
            return
        model = NodeTreeModel(root_path)
        self._tree_view.setModel(model)
        # Re-wire selection after model replacement
        self._tree_view.selectionModel().currentChanged.connect(self._on_node_selected)
        self._tree_view.expandToDepth(1)
        self._status_label.setText(f"Tree loaded from {root_path}")

    def _on_node_selected(self, current: QtCore.QModelIndex, previous: QtCore.QModelIndex) -> None:
        """
        Handle selection changes in the tree view.

        Args:
            current (QtCore.QModelIndex): The newly selected index.
            previous (QtCore.QModelIndex): The previously selected index.
        """
        if not current.isValid():
            return
        node = current.data(Qt.ItemDataRole.UserRole)
        if node is None:
            return
        self._current_node = node
        self._show_node_code(node)

    def _refresh_code(self) -> None:
        """Re-run asCode on the current node when any option checkbox changes."""
        node = getattr(self, "_current_node", None)
        if node is not None:
            self._show_node_code(node)

    def _build_ascode_kwargs(self) -> Dict[str, bool]:
        """
        Return a dict of kwargs for node.asCode() from the current checkbox state.

        Returns:
            Dict[str, bool]: Key-value pairs of options.
        """
        kwargs = {}
        for attr, kwarg, _label, _default in self._ascode_opts:
            kwargs[kwarg] = getattr(self, attr).isChecked()
        return kwargs

    def _show_node_code(self, node: "hou.Node") -> None:
        """
        Generate and display the asCode for the given node.

        Args:
            node (hou.Node): The Houdini node to generate code for.
        """
        try:
            kwargs = self._build_ascode_kwargs()
            code = node.asCode(**kwargs)
            self._editor.setPlainText(code)
            self._status_label.setText(f"{node.path()}  [{node.type().name()}]  — {len(code.splitlines())} lines")
        except Exception as exc:
            self._editor.setPlainText(f"# Error generating code for {node.path()}\n# {exc}")
            self._status_label.setText(f"Error: {exc}")
        # Re-apply any active search highlights after content changes
        self._on_search_changed()

    # ------------------------------------------------------------------
    # Search
    # ------------------------------------------------------------------

    def _search_flags(self) -> QtGui.QTextDocument.FindFlag:
        """
        Get the current search flags based on UI state.

        Returns:
            QtGui.QTextDocument.FindFlag: Active find flags.
        """
        flags = QtGui.QTextDocument.FindFlag(0)
        if self._search_case_cb.isChecked():
            flags |= QtGui.QTextDocument.FindFlag.FindCaseSensitively
        return flags

    def _count_matches(self, term: str) -> int:
        """
        Return the total number of occurrences of term in the document.

        Args:
            term (str): Search term.

        Returns:
            int: Number of matches.
        """
        if not term:
            return 0
        doc = self._editor.document()
        flags = self._search_flags()
        # Count from document start
        cursor = doc.find(term, 0, flags)
        count = 0
        while not cursor.isNull():
            count += 1
            cursor = doc.find(term, cursor, flags)
        return count

    def _on_search_changed(self) -> None:
        """Handle changes to the search text or options."""
        term = self._search_edit.text()
        if not term:
            # Clear any extra selections and reset field colour
            self._editor.setExtraSelections([])
            self._search_count_label.setText("")
            self._search_edit.setStyleSheet("")
            return
        # Highlight all matches with a background colour
        self._highlight_all(term)
        # Jump to first match from the top
        self._editor.moveCursor(QtGui.QTextCursor.MoveOperation.Start)
        found = self._editor.find(term, self._search_flags())
        total = self._count_matches(term)
        if not found and total == 0:
            self._search_edit.setStyleSheet("background-color: #5a1a1a;")
            self._search_count_label.setText("0 matches")
        else:
            self._search_edit.setStyleSheet("")
            self._search_count_label.setText(f"{total} match{'es' if total != 1 else ''}")

    def _highlight_all(self, term: str) -> None:
        """
        Paint a dim background on every occurrence in the document.

        Args:
            term (str): The search term to highlight.
        """
        selections = []
        if term:
            doc = self._editor.document()
            flags = self._search_flags()
            cursor = doc.find(term, 0, flags)
            fmt = QtGui.QTextCharFormat()
            fmt.setBackground(QtGui.QColor("#3a3a00"))
            while not cursor.isNull():
                sel = QtWidgets.QTextEdit.ExtraSelection()
                sel.cursor = cursor
                sel.format = fmt
                selections.append(sel)
                cursor = doc.find(term, cursor, flags)
        self._editor.setExtraSelections(selections)

    def _search_next(self) -> None:
        """Find the next occurrence of the search term."""
        term = self._search_edit.text()
        if not term:
            return
        found = self._editor.find(term, self._search_flags())
        if not found:
            # Wrap around to top
            self._editor.moveCursor(QtGui.QTextCursor.MoveOperation.Start)
            self._editor.find(term, self._search_flags())

    def _search_prev(self) -> None:
        """Find the previous occurrence of the search term."""
        term = self._search_edit.text()
        if not term:
            return
        flags = self._search_flags() | QtGui.QTextDocument.FindFlag.FindBackward
        found = self._editor.find(term, flags)
        if not found:
            # Wrap around to bottom
            self._editor.moveCursor(QtGui.QTextCursor.MoveOperation.End)
            self._editor.find(term, flags)

    def _choose_font(self) -> None:
        """Open a font dialog and apply the chosen font to the editor, persisting it to QSettings."""
        current_font = self._editor.font()
        font, accepted = QtWidgets.QFontDialog.getFont(self, "Choose Editor Font", current_font)
        if not accepted:
            return
        self._editor.set_font(font)
        # The syntax highlighter's QTextCharFormat blocks override the
        # widget font, so we must also update the document's default font
        # and rehighlight to make the new size/family visible everywhere.
        self._editor.document().setDefaultFont(font)
        self._highlighter.rehighlight()
        self._settings = QtCore.QSettings("NCCA", "CodeExplorer")
        self._settings.beginGroup("Font")
        self._settings.setValue("font-name", font.family())
        self._settings.setValue("font-size", font.pointSize())
        self._settings.setValue("font-weight", int(font.weight().value))
        self._settings.setValue("font-italic", font.italic())
        self._settings.endGroup()
        self._settings.sync()

    def _copy_code(self) -> None:
        """Copy the current editor content to the system clipboard."""
        text = self._editor.toPlainText()
        if text:
            QtWidgets.QApplication.clipboard().setText(text)
            self._status_label.setText("Code copied to clipboard.")

    def _save_code(self) -> None:
        """Open Houdini file dialog and save current editor content to a .py file."""
        text = self._editor.toPlainText()
        if not text:
            self._status_label.setText("No code to save.")
            return
        path = hou.ui.selectFile(
            title="Save Python file",
            pattern="*.py",
            file_type=hou.fileType.Any,
            chooser_mode=hou.fileChooserMode.Write,
        )
        if not path:
            return
        if not path.lower().endswith(".py"):
            path += ".py"
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(text)
            self._status_label.setText(f"Saved to {path}")
        except Exception as e:
            self._status_label.setText(f"Error saving file: {e}")

    def eventFilter(self, obj: QtCore.QObject, event: QtCore.QEvent) -> bool:
        """
        Intercept Shift+Enter in the search field to go backwards.

        Args:
            obj (QtCore.QObject): The object being filtered.
            event (QtCore.QEvent): The event occurring.

        Returns:
            bool: True if event was handled, False otherwise.
        """
        if obj is self._search_edit and event.type() == QtCore.QEvent.Type.KeyPress:
            if (
                event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter)
                and event.modifiers() & Qt.KeyboardModifier.ShiftModifier
            ):
                self._search_prev()
                return True
        return super().eventFilter(obj, event)

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        """
        Handle the close event.

        Args:
            event (QtGui.QCloseEvent): The close event.
        """
        super().closeEvent(event)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def run_package() -> CodeExplorerDialog:
    """
    Create and show the Code Explorer dialog, parented to Houdini's main window.

    Returns:
        CodeExplorerDialog: The created dialog instance.
    """
    dialog = CodeExplorerDialog()
    if hou:
        dialog.setParent(hou.qt.mainWindow(), Qt.WindowType.Window)
    dialog.show()
    return dialog


# Allow running directly from the Houdini Python Shell or Script Editor:
#   exec(open('/path/to/CodeExplorer.py').read())
if __name__ == "__main__" or "hou" in dir():
    run_package()
