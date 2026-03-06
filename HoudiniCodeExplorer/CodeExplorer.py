"""
This is 100% vibe coded from a basic demo I wrote a long time ago.
See the file CodeExplorerSession.md in the github repo here:
https://github.com/NCCA/PipelineAndTD/blob/main/HoudiniCodeExplorer/CodeExplorerSession.md
"""

import sys
from typing import Any, Dict, List, Optional, Tuple, Union

try:
    import hou
except ImportError:
    hou = None  # Allow linting outside Houdini

from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt
from PySide6.QtGui import QPalette

# ---------------------------------------------------------------------------
# Syntax highlighter for Python code
# ---------------------------------------------------------------------------


class PythonHighlighter(QtGui.QSyntaxHighlighter):
    """
    Minimal Python syntax highlighter using Houdini-friendly dark colours.

    Args:
        document (QtGui.QTextDocument): The text document to highlight.
    """

    def __init__(self, document: QtGui.QTextDocument) -> None:
        super().__init__(document)

        self._rules: List[Tuple[QtCore.QRegularExpression, QtGui.QTextCharFormat]] = []

        def add(
            pattern: str, colour: str, bold: bool = False, italic: bool = False
        ) -> None:
            """
            Helper to add a highlighting rule.

            Args:
                pattern (str): Regex pattern to match.
                colour (str): Hex colour code.
                bold (bool, optional): Whether to make the text bold. Defaults to False.
                italic (bool, optional): Whether to make the text italic. Defaults to False.
            """
            fmt = QtGui.QTextCharFormat()
            fmt.setForeground(QtGui.QColor(colour))
            if bold:
                fmt.setFontWeight(QtGui.QFont.Weight.Bold)
            if italic:
                fmt.setFontItalic(True)
            self._rules.append((QtCore.QRegularExpression(pattern), fmt))

        # Keywords
        # fmt: off
        keywords = [
            "False", "None", "True", "and", "as", "assert", "async", "await", "break",
            "class", "continue", "def", "del", "elif", "else", "except", "finally",
            "for", "from", "global", "if", "import", "in", "is", "lambda", "nonlocal",
            "not", "or", "pass", "raise", "return", "try", "while", "with", "yield",
            "hou.",
        ]
        # fmt: on
        kw_pattern = r"\b(" + "|".join(keywords) + r")\b"
        add(kw_pattern, "#569CD6", bold=True)

        # Built-ins
        # fmt: off
        builtins = [
            "print", "len", "range", "int", "float", "str", "list", "dict", "tuple",
            "set", "bool", "type", "isinstance", "hasattr", "getattr", "setattr",
            "enumerate", "zip", "map", "filter", "sorted", "reversed", "open", "super",
            "self",
        ]
        # fmt: on
        add(r"\b(" + "|".join(builtins) + r")\b", "#DCDCAA")

        # Decorators
        add(r"@\w+", "#C586C0")

        # Numbers
        add(r"\b[0-9]+\.?[0-9]*([eE][+-]?[0-9]+)?\b", "#B5CEA8")

        # Double-quoted strings
        add(r'"[^"\\]*(\\.[^"\\]*)*"', "#CE9178")
        # Single-quoted strings
        add(r"'[^'\\]*(\\.[^'\\]*)*'", "#CE9178")

        # Triple-quoted strings (simple, single-line match only)
        add(r'""".*?"""', "#CE9178")
        add(r"'''.*?'''", "#CE9178")

        # Comments
        add(r"#[^\n]*", "#6A9955", italic=True)

        # hou module references
        add(r"\bhou\b", "#4EC9B0", bold=True)

    def highlightBlock(self, text: str) -> None:
        """
        Apply highlighting to a block of text.

        Args:
            text (str): The text block to highlight.
        """
        for pattern, fmt in self._rules:
            it = pattern.globalMatch(text)
            while it.hasNext():
                m = it.next()
                self.setFormat(m.capturedStart(), m.capturedLength(), fmt)


# ---------------------------------------------------------------------------
# Node tree model
# ---------------------------------------------------------------------------


class NodeTreeItem:
    """
    Wrapper item for the NodeTreeModel to hold Houdini nodes.

    Args:
        node (Optional[hou.Node]): The Houdini node to wrap. None for the root item.
        parent (Optional[NodeTreeItem], optional): The parent item. Defaults to None.
    """

    def __init__(
        self, node: Optional["hou.Node"], parent: Optional["NodeTreeItem"] = None
    ) -> None:
        self.node: Optional["hou.Node"] = node
        self.parent_item: Optional["NodeTreeItem"] = parent
        self.children: List["NodeTreeItem"] = []

    def child(self, row: int) -> "NodeTreeItem":
        """
        Get the child item at the given row.

        Args:
            row (int): The row index of the child.

        Returns:
            NodeTreeItem: The child item.
        """
        return self.children[row]

    def child_count(self) -> int:
        """
        Get the number of children.

        Returns:
            int: The count of children.
        """
        return len(self.children)

    def row(self) -> int:
        """
        Get the row index of this item within its parent.

        Returns:
            int: The row index.
        """
        if self.parent_item:
            return self.parent_item.children.index(self)
        return 0


class NodeTreeModel(QtCore.QAbstractItemModel):
    """
    Qt Item Model for displaying the Houdini node hierarchy.

    Args:
        root_path (str, optional): The path to the root node. Defaults to "/".
        parent (Optional[QtCore.QObject], optional): The parent object. Defaults to None.
    """

    def __init__(
        self, root_path: str = "/", parent: Optional[QtCore.QObject] = None
    ) -> None:
        super().__init__(parent)
        self._root = NodeTreeItem(None)
        # Assuming hou is available if this class is used, or will handle None node gracefully
        node = hou.node(root_path) if hou else None
        self._populate(self._root, node)

    def _populate(self, parent_item: NodeTreeItem, node: Optional["hou.Node"]) -> None:
        """
        Recursively populate the tree model with children of the given node.

        Args:
            parent_item (NodeTreeItem): The parent item in the tree model.
            node (Optional[hou.Node]): The Houdini node to inspect for children.
        """
        if node is None:
            return
        item = NodeTreeItem(node, parent_item)
        parent_item.children.append(item)
        # Assuming hou.Node.children() returns a sequence of nodes
        for child in node.children():
            self._populate(item, child)

    def index(
        self,
        row: int,
        column: int,
        parent: QtCore.QModelIndex = QtCore.QModelIndex(),
    ) -> QtCore.QModelIndex:
        """
        Get the model index for the given row, column, and parent index.

        Args:
            row (int): Row number.
            column (int): Column number.
            parent (QtCore.QModelIndex, optional): Parent model index. Defaults to invalid index.

        Returns:
            QtCore.QModelIndex: The corresponding model index.
        """
        if not self.hasIndex(row, column, parent):
            return QtCore.QModelIndex()
        parent_item = parent.internalPointer() if parent.isValid() else self._root
        child = parent_item.child(row)
        if child:
            return self.createIndex(row, column, child)
        return QtCore.QModelIndex()

    def parent(self, index: QtCore.QModelIndex) -> QtCore.QModelIndex:
        """
        Get the parent model index for the given index.

        Args:
            index (QtCore.QModelIndex): The index to find the parent for.

        Returns:
            QtCore.QModelIndex: The parent model index.
        """
        if not index.isValid():
            return QtCore.QModelIndex()
        item: NodeTreeItem = index.internalPointer()
        p = item.parent_item
        if p is self._root or p is None:
            return QtCore.QModelIndex()
        return self.createIndex(p.row(), 0, p)

    def rowCount(self, parent: QtCore.QModelIndex = QtCore.QModelIndex()) -> int:
        """
        Get the number of rows under the given parent.

        Args:
            parent (QtCore.QModelIndex, optional): Parent index. Defaults to invalid index.

        Returns:
            int: Number of rows.
        """
        p = parent.internalPointer() if parent.isValid() else self._root
        return p.child_count()

    def columnCount(self, parent: QtCore.QModelIndex = QtCore.QModelIndex()) -> int:
        """
        Get the number of columns. Always 1 for this model.

        Args:
            parent (QtCore.QModelIndex, optional): Parent index. Defaults to invalid index.

        Returns:
            int: Number of columns (1).
        """
        return 1

    def data(
        self, index: QtCore.QModelIndex, role: int = Qt.ItemDataRole.DisplayRole
    ) -> Any:
        """
        Get data for the given index and role.

        Args:
            index (QtCore.QModelIndex): The model index.
            role (int, optional): The data role. Defaults to Qt.ItemDataRole.DisplayRole.

        Returns:
            Any: The data for the requested role, or None.
        """
        if not index.isValid():
            return None
        item: NodeTreeItem = index.internalPointer()
        if role == Qt.ItemDataRole.DisplayRole:
            node = item.node
            if node:
                return f"{node.name()}  [{node.type().name()}]"
            return "Unknown Node"
        if role == Qt.ItemDataRole.UserRole:
            return item.node
        return None

    def flags(self, index: QtCore.QModelIndex) -> Qt.ItemFlag:
        """
        Get the item flags for the given index.

        Args:
            index (QtCore.QModelIndex): The model index.

        Returns:
            Qt.ItemFlag: The combined flags for the item.
        """
        if not index.isValid():
            return Qt.ItemFlag.NoItemFlags
        return Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable


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

        self._build_ui()
        self._connect_signals()

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

        self._editor = QtWidgets.QPlainTextEdit()
        self._editor.setReadOnly(True)
        # Load saved font from QSettings, falling back to the default
        _settings = QtCore.QSettings("NCCA", "CodeExplorer")
        _saved_font = _settings.value("editor/font")
        if isinstance(_saved_font, QtGui.QFont):
            _editor_font = _saved_font
        else:
            _editor_font = QtGui.QFont("Courier New", 10)
            _editor_font.setFixedPitch(True)
        self._editor.setFont(_editor_font)
        self._editor.document().setDefaultFont(_editor_font)
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

    def _on_node_selected(
        self, current: QtCore.QModelIndex, previous: QtCore.QModelIndex
    ) -> None:
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
            self._status_label.setText(
                f"{node.path()}  [{node.type().name()}]  — {len(code.splitlines())} lines"
            )
        except Exception as exc:
            self._editor.setPlainText(
                f"# Error generating code for {node.path()}\n# {exc}"
            )
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
            self._search_count_label.setText(
                f"{total} match{'es' if total != 1 else ''}"
            )

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
        font, accepted = QtWidgets.QFontDialog.getFont(
            current_font, self, "Choose Editor Font"
        )
        if accepted:
            self._editor.setFont(font)
            # The syntax highlighter's QTextCharFormat blocks override the
            # widget font, so we must also update the document's default font
            # and rehighlight to make the new size/family visible everywhere.
            self._editor.document().setDefaultFont(font)
            self._highlighter.rehighlight()
            settings = QtCore.QSettings("NCCA", "CodeExplorer")
            settings.setValue("editor/font", font)

    def _copy_code(self) -> None:
        """Copy the current editor content to the system clipboard."""
        text = self._editor.toPlainText()
        if text:
            QtWidgets.QApplication.clipboard().setText(text)
            self._status_label.setText("Code copied to clipboard.")

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


def show() -> CodeExplorerDialog:
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
    show()
