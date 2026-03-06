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
    """Minimal Python syntax highlighter using Houdini-friendly dark colours."""

    def __init__(self, document):
        super().__init__(document)

        self._rules = []

        def add(pattern, colour, bold=False, italic=False):
            fmt = QtGui.QTextCharFormat()
            fmt.setForeground(QtGui.QColor(colour))
            if bold:
                fmt.setFontWeight(QtGui.QFont.Weight.Bold)
            if italic:
                fmt.setFontItalic(True)
            self._rules.append((QtCore.QRegularExpression(pattern), fmt))

        # Keywords
        keywords = [
            "False",
            "None",
            "True",
            "and",
            "as",
            "assert",
            "async",
            "await",
            "break",
            "class",
            "continue",
            "def",
            "del",
            "elif",
            "else",
            "except",
            "finally",
            "for",
            "from",
            "global",
            "if",
            "import",
            "in",
            "is",
            "lambda",
            "nonlocal",
            "not",
            "or",
            "pass",
            "raise",
            "return",
            "try",
            "while",
            "with",
            "yield",
        ]
        kw_pattern = r"\b(" + "|".join(keywords) + r")\b"
        add(kw_pattern, "#569CD6", bold=True)

        # Built-ins
        builtins = [
            "print",
            "len",
            "range",
            "int",
            "float",
            "str",
            "list",
            "dict",
            "tuple",
            "set",
            "bool",
            "type",
            "isinstance",
            "hasattr",
            "getattr",
            "setattr",
            "enumerate",
            "zip",
            "map",
            "filter",
            "sorted",
            "reversed",
            "open",
            "super",
            "self",
        ]
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

    def highlightBlock(self, text):
        for pattern, fmt in self._rules:
            it = pattern.globalMatch(text)
            while it.hasNext():
                m = it.next()
                self.setFormat(m.capturedStart(), m.capturedLength(), fmt)


# ---------------------------------------------------------------------------
# Node tree model
# ---------------------------------------------------------------------------


class NodeTreeItem:
    def __init__(self, node, parent=None):
        self.node = node
        self.parent_item = parent
        self.children = []

    def child(self, row):
        return self.children[row]

    def child_count(self):
        return len(self.children)

    def row(self):
        if self.parent_item:
            return self.parent_item.children.index(self)
        return 0


class NodeTreeModel(QtCore.QAbstractItemModel):
    def __init__(self, root_path="/", parent=None):
        super().__init__(parent)
        self._root = NodeTreeItem(None)
        self._populate(self._root, hou.node(root_path))

    def _populate(self, parent_item, node):
        if node is None:
            return
        item = NodeTreeItem(node, parent_item)
        parent_item.children.append(item)
        for child in node.children():
            self._populate(item, child)

    def index(self, row, column, parent=QtCore.QModelIndex()):
        if not self.hasIndex(row, column, parent):
            return QtCore.QModelIndex()
        parent_item = parent.internalPointer() if parent.isValid() else self._root
        child = parent_item.child(row)
        if child:
            return self.createIndex(row, column, child)
        return QtCore.QModelIndex()

    def parent(self, index):
        if not index.isValid():
            return QtCore.QModelIndex()
        item = index.internalPointer()
        p = item.parent_item
        if p is self._root or p is None:
            return QtCore.QModelIndex()
        return self.createIndex(p.row(), 0, p)

    def rowCount(self, parent=QtCore.QModelIndex()):
        p = parent.internalPointer() if parent.isValid() else self._root
        return p.child_count()

    def columnCount(self, parent=QtCore.QModelIndex()):
        return 1

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None
        item = index.internalPointer()
        if role == Qt.ItemDataRole.DisplayRole:
            node = item.node
            return f"{node.name()}  [{node.type().name()}]"
        if role == Qt.ItemDataRole.UserRole:
            return item.node
        return None

    def flags(self, index):
        if not index.isValid():
            return Qt.ItemFlag.NoItemFlags
        return Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable


# ---------------------------------------------------------------------------
# Main dialog
# ---------------------------------------------------------------------------


class CodeExplorerDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Code Explorer")
        self.resize(1100, 700)
        self._build_ui()
        self._connect_signals()

    # ------------------------------------------------------------------
    # UI construction
    # ------------------------------------------------------------------

    def _build_ui(self):
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
        toolbar.addWidget(QtWidgets.QLabel("Root:"))
        toolbar.addWidget(self._root_edit)
        toolbar.addWidget(self._refresh_btn)
        toolbar.addStretch()
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
        font = QtGui.QFont("Courier New", 10)
        font.setFixedPitch(True)
        self._editor.setFont(font)
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

    def _connect_signals(self):
        self._tree_view.selectionModel().currentChanged.connect(self._on_node_selected)
        self._refresh_btn.clicked.connect(self._reload_tree)
        self._copy_btn.clicked.connect(self._copy_code)
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

    def _reload_tree(self):
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

    def _on_node_selected(self, current, previous):
        if not current.isValid():
            return
        node = current.data(Qt.ItemDataRole.UserRole)
        if node is None:
            return
        self._current_node = node
        self._show_node_code(node)

    def _refresh_code(self):
        """Re-run asCode on the current node when any option checkbox changes."""
        node = getattr(self, "_current_node", None)
        if node is not None:
            self._show_node_code(node)

    def _build_ascode_kwargs(self):
        """Return a dict of kwargs for node.asCode() from the current checkbox state."""
        kwargs = {}
        for attr, kwarg, _label, _default in self._ascode_opts:
            kwargs[kwarg] = getattr(self, attr).isChecked()
        return kwargs

    def _show_node_code(self, node):
        try:
            kwargs = self._build_ascode_kwargs()
            code = node.asCode(**kwargs)
            self._editor.setPlainText(code)
            self._status_label.setText(
                f"{node.path()}  [{node.type().name()}]  "
                f"— {len(code.splitlines())} lines"
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

    def _search_flags(self):
        flags = QtGui.QTextDocument.FindFlag(0)
        if self._search_case_cb.isChecked():
            flags |= QtGui.QTextDocument.FindFlag.FindCaseSensitively
        return flags

    def _count_matches(self, term):
        """Return the total number of occurrences of term in the document."""
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

    def _on_search_changed(self):
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

    def _highlight_all(self, term):
        """Paint a dim background on every occurrence in the document."""
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

    def _search_next(self):
        term = self._search_edit.text()
        if not term:
            return
        found = self._editor.find(term, self._search_flags())
        if not found:
            # Wrap around to top
            self._editor.moveCursor(QtGui.QTextCursor.MoveOperation.Start)
            self._editor.find(term, self._search_flags())

    def _search_prev(self):
        term = self._search_edit.text()
        if not term:
            return
        flags = self._search_flags() | QtGui.QTextDocument.FindFlag.FindBackward
        found = self._editor.find(term, flags)
        if not found:
            # Wrap around to bottom
            self._editor.moveCursor(QtGui.QTextCursor.MoveOperation.End)
            self._editor.find(term, flags)

    def _copy_code(self):
        text = self._editor.toPlainText()
        if text:
            QtWidgets.QApplication.clipboard().setText(text)
            self._status_label.setText("Code copied to clipboard.")

    def eventFilter(self, obj, event):
        """Intercept Shift+Enter in the search field to go backwards."""
        if obj is self._search_edit and event.type() == QtCore.QEvent.Type.KeyPress:
            if (
                event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter)
                and event.modifiers() & Qt.KeyboardModifier.ShiftModifier
            ):
                self._search_prev()
                return True
        return super().eventFilter(obj, event)

    def closeEvent(self, event):
        super().closeEvent(event)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def show():
    """Create and show the Code Explorer dialog, parented to Houdini's main window."""
    dialog = CodeExplorerDialog()
    dialog.setParent(hou.qt.mainWindow(), Qt.WindowType.Window)
    dialog.show()
    return dialog


# Allow running directly from the Houdini Python Shell or Script Editor:
#   exec(open('/path/to/CodeExplorer.py').read())
if __name__ == "__main__" or "hou" in dir():
    show()
