from PySide6.QtWidgets import QMainWindow, QStackedWidget
from PySide6.QtCore import QSize, QTimer

from .signin_widget import SignInWidget
from .nodelist_widget import NodeListWidget
from .connected_widget import ConnectedWidget
import notification_service


class MainWindow(QMainWindow):
    """The main window that controls screen transitions and state."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Vantage VPN")
        self.setMinimumSize(QSize(450, 600))

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Create all three screens

        self.signin_screen = SignInWidget()
        self.nodelist_screen = NodeListWidget()
        self.connected_screen = ConnectedWidget()

        self.stacked_widget.addWidget(self.signin_screen)
        self.stacked_widget.addWidget(self.nodelist_screen)
        self.stacked_widget.addWidget(self.connected_screen)

        # --- Signal Connections ---

        self.signin_screen.login_successful.connect(self.show_nodelist_screen)
        self.nodelist_screen.connection_requested.connect(self._handle_connection_flow)
        self.connected_screen.disconnected.connect(self._handle_disconnection)

        # Start on the sign-in screen

        self.show_signin_screen()

    def _handle_connection_flow(self, node):
        """Simulates the connection and switches to the connected screen."""
        notification_service.show_notification(
            "Vantage VPN", f"Connecting to {node.name}..."
        )

        # Simulate a 2-second connection delay before switching screens

        QTimer.singleShot(2000, lambda: self.show_connected_screen(node))

    def _handle_disconnection(self):
        """Handles the disconnection flow."""
        self.connected_screen.stop_connection()
        self.show_nodelist_screen()
        notification_service.show_notification(
            "Vantage VPN", "You have been disconnected."
        )

    def show_signin_screen(self):
        self.stacked_widget.setCurrentWidget(self.signin_screen)

    def show_nodelist_screen(self):
        self.stacked_widget.setCurrentWidget(self.nodelist_screen)

    def show_connected_screen(self, node):
        """Switches to and initializes the connected screen."""
        self.connected_screen.start_connection(node)
        self.stacked_widget.setCurrentWidget(self.connected_screen)
        notification_service.show_notification(
            "Vantage VPN", f"Securely connected to {node.name}!"
        )
