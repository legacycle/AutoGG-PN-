import sys
import os
import smtplib
from email.mime.text import MIMEText
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QMessageBox, QInputDialog
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import QPropertyAnimation, QRect
import keyboard
import json

class AutoGGApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.load_config()
        self.start_animation()
        self.show_notification()

    def initUI(self):
        self.setWindowTitle('PikaNetwork Auto GG')
        self.setGeometry(100, 100, 400, 250)
        self.setWindowIcon(QIcon('icon.png'))

        self.message_label = QLabel('Message to Type:', self)
        self.message_label.move(50, 50)

        self.message_entry = QLineEdit(self)
        self.message_entry.setText('GG!')
        self.message_entry.move(180, 50)
        self.message_entry.resize(150, 30)

        self.hotkey_label = QLabel('Set Hotkey:', self)
        self.hotkey_label.move(50, 100)

        self.hotkey_entry = QLineEdit(self)
        self.hotkey_entry.setText(self.hotkey if hasattr(self, 'hotkey') else '')
        self.hotkey_entry.move(180, 100)
        self.hotkey_entry.resize(150, 30)

        self.set_button = QPushButton('Set Hotkey', self)
        self.set_button.setGeometry(150, 150, 100, 30)
        self.set_button.setFont(QFont('Helvetica', 12, QFont.Bold))
        self.set_button.clicked.connect(self.set_hotkey)

        self.clear_button = QPushButton('Clear Settings', self)
        self.clear_button.setGeometry(260, 150, 120, 30)
        self.clear_button.setFont(QFont('Helvetica', 12, QFont.Bold))
        self.clear_button.clicked.connect(self.clear_settings)

        self.feedback_button = QPushButton('Give Feedback', self)
        self.feedback_button.setGeometry(50, 200, 150, 30)
        self.feedback_button.setFont(QFont('Helvetica', 12, QFont.Bold))
        self.feedback_button.clicked.connect(self.give_feedback)

        self.show()

    def start_animation(self):
        self.anim = QPropertyAnimation(self, b"geometry")
        self.anim.setDuration(1000)
        self.anim.setStartValue(QRect(100, 100, 400, 200))
        self.anim.setEndValue(QRect(100, 100, 400, 250))
        self.anim.start()

    def set_hotkey(self):
        hotkey = self.hotkey_entry.text().strip()
        if len(hotkey.split()) > 1:
            QMessageBox.warning(self, 'Warning', 'Please enter a single key or combination without spaces.')
            return

        try:
            keyboard.add_hotkey(hotkey, self.type_message)
            self.hotkey = hotkey
            self.setWindowTitle('PikaNetwork Auto GG - Hotkey Set')
            self.set_button.setStyleSheet("background-color: green;")
            self.save_config()
            QMessageBox.information(self, 'Success', f"Hotkey '{hotkey}' set!")
        except ValueError:
            QMessageBox.warning(self, 'Warning', 'Invalid hotkey. Please enter a valid key or combination.')

    def clear_settings(self):
        self.hotkey_entry.setText('')
        self.message_entry.setText('GG!')
        self.hotkey = ''
        self.setWindowTitle('PikaNetwork Auto GG')
        self.set_button.setStyleSheet("")
        self.save_config()

    def type_message(self):
        message = 'GG!'  # Set message to 'GG!' directly
        keyboard.write(message)
        keyboard.press_and_release('enter')

    def load_config(self):
        config_file = os.path.join(os.path.dirname(__file__), 'config.json')
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                try:
                    config = json.load(f)
                    self.hotkey = config.get('hotkey', '')
                    self.message_entry.setText(config.get('message', 'GG!'))
                except json.JSONDecodeError:
                    QMessageBox.warning(self, 'Config Error', 'Failed to load config.json: Invalid JSON format.')
        else:
            QMessageBox.warning(self, 'Config Error', 'Config file (config.json) not found.')

    def save_config(self):
        config_file = os.path.join(os.path.dirname(__file__), 'config.json')
        config = {
            'hotkey': self.hotkey,
            'message': self.message_entry.text()
        }
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=4)

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Confirm Close', 'Are you sure you want to close the application?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def show_notification(self):
        if hasattr(self, 'hotkey') and self.hotkey:
            QMessageBox.information(self, 'Settings Loaded', f"Previous settings loaded: Hotkey '{self.hotkey}' and Message '{self.message_entry.text()}'.")

    def give_feedback(self):
        feedback, ok = QInputDialog.getText(self, 'Feedback', 'Please enter your feedback:')
        if ok and feedback.strip():
            self.send_feedback(feedback.strip())
            QMessageBox.information(self, 'Feedback Sent', 'Thank you for your feedback!')

    def send_feedback(self, feedback):
        try:
            sender_email = "prototype@gmail.com"
            sender_password = "1234567"
            receiver_email = "leonotdeo@gmail.com"
            
            message = MIMEText(feedback)
            message['Subject'] = 'Feedback from AutoGGApp'
            message['From'] = sender_email
            message['To'] = receiver_email

            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, message.as_string())
            server.quit()
        except smtplib.SMTPAuthenticationError:
            QMessageBox.warning(self, 'Authentication Error', 'Failed to send feedback: Authentication error. com.lega/proxyerror/loadup/Error79')
        except Exception as e:
            QMessageBox.warning(self, 'Feedback Error', f'Failed to send feedback: {str(e)}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    autoGGApp = AutoGGApp()
    sys.exit(app.exec_())
