from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSpacerItem,
    QSizePolicy,
)
from PySide6.QtGui import QFont


class SignInWidget(QWidget):
    """The widget for the Sign-In screen with full UI and logic."""

    # A signal that will be emitted when login is successful

    login_successful = Signal()

    def __init__(self):
        super().__init__()

        # --- UI Elements ---

        main_layout = QVBoxLayout(self)

        # Title

        title_label = QLabel("Vantage VPN")
        title_font = QFont()
        title_font.setPointSize(24)
        title_font.setBold(True)
        title_label.setFont(title_font)

        # Input Fields

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)  # Hides password text

        # Login Button

        login_button = QPushButton("Sign In")

        # Error Message Label

        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color: red;")  # Style the error message

        # --- Layout ---

        main_layout.addSpacerItem(
            QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        )
        main_layout.addWidget(title_label)
        main_layout.addWidget(self.email_input)
        main_layout.addWidget(self.password_input)
        main_layout.addWidget(self.error_label)
        main_layout.addWidget(login_button)
        main_layout.addSpacerItem(
            QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        )

        # --- Logic ---

        login_button.clicked.connect(self._handle_login)

    def _handle_login(self):
        """Handles the mock login validation."""
        email = self.email_input.text()
        password = self.password_input.text()

        # Mock validation

        if email == "test@test.com" and password == "password":
            self.error_label.setText("")  # Clear any previous errors
            self.login_successful.emit()  # Tell that login was successful
        else:
            self.error_label.setText("Invalid credentials. Please try again.")
