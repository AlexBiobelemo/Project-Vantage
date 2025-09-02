import random
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QSpacerItem,
    QSizePolicy,
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Signal, QTimer, QTime, Qt


class ConnectedWidget(QWidget):
    """The UI which shows the active connection status and details."""

    disconnected = Signal()

    def __init__(self):
        super().__init__()
        self._time = QTime(0, 0, 0)
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._update_display)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setAlignment(Qt.AlignCenter)

        status_label = QLabel("You Are Securely Connected")
        font = QFont()
        font.setPointSize(16)
        font.setBold(True)
        status_label.setFont(font)
        status_label.setAlignment(Qt.AlignCenter)

        self.server_label = QLabel("Server: N/A")
        self.ip_label = QLabel("IP Address: N/A")
        self.duration_label = QLabel("Duration: 00:00:00")

        self.download_label = QLabel("Download: -- Mbps")
        self.upload_label = QLabel("Upload: -- Mbps")

        # Center align all text labels

        for label in [
            self.server_label,
            self.ip_label,
            self.duration_label,
            self.download_label,
            self.upload_label,
        ]:
            label.setAlignment(Qt.AlignCenter)
        disconnect_button = QPushButton("Disconnect")
        disconnect_button.clicked.connect(self.disconnected.emit)

        # --- Layout ---

        main_layout.addSpacerItem(
            QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        )
        main_layout.addWidget(status_label)
        main_layout.addSpacerItem(
            QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)
        )
        main_layout.addWidget(self.server_label)
        main_layout.addWidget(self.ip_label)
        main_layout.addWidget(self.duration_label)
        main_layout.addWidget(self.download_label)
        main_layout.addWidget(self.upload_label)
        main_layout.addStretch()
        main_layout.addWidget(disconnect_button)
        main_layout.addSpacerItem(
            QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        )

    def start_connection(self, node):
        """Called by the main window to start the timer and update labels."""
        self.server_label.setText(f"Server: {node.name} ({node.country})")
        self.ip_label.setText(f"IP Address: {node.ip_address}")

        self._time.setHMS(0, 0, 0)
        self.duration_label.setText("Duration: 00:00:00")
        self._timer.start(1000)

    def stop_connection(self):
        """Stops the timer when disconnected or navigating away."""
        self._timer.stop()

    def _update_display(self):
        """Updates the duration and simulates new speeds every second."""
        self._time = self._time.addSecs(1)
        self.duration_label.setText(f"Duration: {self._time.toString('hh:mm:ss')}")

        download_speed = 85.31 + random.uniform(-5.5, 5.5)
        upload_speed = 22.19 + random.uniform(-2.5, 2.5)
        self.download_label.setText(f"Download: {download_speed:.2f} Mbps")
        self.upload_label.setText(f"Upload: {upload_speed:.2f} Mbps")
