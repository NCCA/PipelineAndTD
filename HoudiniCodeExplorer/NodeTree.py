from typing import Any, Dict, List, Optional, Tuple, Union

from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt
from PySide6.QtGui import QPalette

try:
    import hou
except ImportError:
    hou = None  # Allow linting outside Houdini

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

    def __init__(self, node: Optional["hou.Node"], parent: Optional["NodeTreeItem"] = None) -> None:
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

    def __init__(self, root_path: str = "/", parent: Optional[QtCore.QObject] = None) -> None:
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

    def data(self, index: QtCore.QModelIndex, role: int = Qt.ItemDataRole.DisplayRole) -> Any:
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
