from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QHBoxLayout,
    QListWidget,
    QListWidgetItem,
    QLineEdit,
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Signal, QTimer, Qt

import api_client
from models import VPNNode


class NodeItemWidget(QWidget):
    """A custom widget for a single row in the NodeListWidget."""

    connect_requested = Signal(VPNNode)

    def __init__(self, node):
        super().__init__()
        self.node = node

        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 0, 0, 0)  # Add a small left margin

        info_label = QLabel(f"<b>{node.name}</b><br>{node.country}")
        self.latency_label = QLabel(f"{node.latency_ms} ms")
        self.latency_label.setStyleSheet("color: #2ecc71;")

        connect_button = QPushButton("Connect")
        connect_button.setFixedWidth(100)
        connect_button.clicked.connect(lambda: self.connect_requested.emit(self.node))

        layout.addWidget(info_label)
        layout.addStretch()
        layout.addWidget(self.latency_label)
        layout.addWidget(connect_button)

    def update_latency(self, new_latency):
        self.node.latency_ms = new_latency
        self.latency_label.setText(f"{new_latency} ms")


# Full implementation of NodeListWidget


class NodeListWidget(QWidget):
    connection_requested = Signal(VPNNode)

    def __init__(self):
        super().__init__()
        self._all_nodes = []  # Store the master list of nodes
        self._item_widgets = {}
        main_layout = QVBoxLayout(self)

        title_label = QLabel("Select a Node")
        font = QFont()
        font.setPointSize(18)
        font.setBold(True)
        title_label.setFont(font)

        # Search and Sort Controls

        controls_layout = QHBoxLayout()
        search_bar = QLineEdit()
        search_bar.setPlaceholderText("Search by country or name...")
        search_bar.textChanged.connect(self._filter_list)

        sort_ping_button = QPushButton("Sort by Ping")
        sort_ping_button.clicked.connect(self._sort_by_latency)

        sort_country_button = QPushButton("Sort by Country")
        sort_country_button.clicked.connect(self._sort_by_country)

        controls_layout.addWidget(search_bar)
        controls_layout.addWidget(sort_ping_button)
        controls_layout.addWidget(sort_country_button)

        self.list_widget = QListWidget()
        main_layout.addWidget(title_label)
        main_layout.addLayout(controls_layout)
        main_layout.addWidget(self.list_widget)

        self._refresh_timer = QTimer(self)
        self._refresh_timer.timeout.connect(self._update_nodes)
        self._refresh_timer.start(5000)

        self._load_nodes()

    def _populate_list(self, nodes):
        """Helper function to clear and fill the list from a list of nodes."""
        self.list_widget.clear()
        self._item_widgets.clear()

        for node in nodes:
            item_widget = NodeItemWidget(node)
            item_widget.connect_requested.connect(self.connection_requested.emit)
            list_item = QListWidgetItem(self.list_widget)
            list_item.setSizeHint(item_widget.sizeHint())
            self.list_widget.addItem(list_item)
            self.list_widget.setItemWidget(list_item, item_widget)
            self._item_widgets[node.id] = item_widget

    def _load_nodes(self):
        """Builds the initial list of nodes."""
        self._all_nodes = api_client.fetch_nodes()
        if not self._all_nodes:
            self.list_widget.addItem("Could not fetch nodes.")
            return
        self._populate_list(self._all_nodes)

    def _update_nodes(self):
        """Fetches new data and updates existing widgets."""
        new_nodes = api_client.fetch_nodes()
        node_map = {n.id: n for n in new_nodes}
        for node in self._all_nodes:
            if node.id in node_map:
                node.latency_ms = node_map[node.id].latency_ms
        for node_id, widget in self._item_widgets.items():
            if node_id in node_map:
                widget.update_latency(node_map[node_id].latency_ms)

    def _filter_list(self, text):
        """Hides or shows items in the list based on the search text."""
        search_text = text.lower()
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            widget = self.list_widget.itemWidget(item)
            node = widget.node

            is_match = (
                search_text in node.name.lower() or search_text in node.country.lower()
            )
            item.setHidden(not is_match)

    def _sort_by_latency(self):
        """Sorts the master list by latency and rebuilds the UI list."""
        self._all_nodes.sort(key=lambda node: node.latency_ms)
        self._populate_list(self._all_nodes)

    def _sort_by_country(self):
        """Sorts the master list by country and rebuilds the UI list."""
        self._all_nodes.sort(key=lambda node: node.country)
        self._populate_list(self._all_nodes)
