"""
MIT License

Copyright (c) 2024 MahdiG

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import sys
import os
import json
import re
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLabel, QComboBox, QPushButton, QLineEdit, QProgressBar, QDialog, QVBoxLayout, QHBoxLayout, QMessageBox
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QColor, QPalette, QIcon
from PyQt5.QtCore import Qt
import wmi
from version import __version__


class DNSChanger(QWidget):

    def __init__(self):
        super().__init__()
        
        self.wmi_obj = wmi.WMI()
        self.adapters = self.wmi_obj.Win32_NetworkAdapterConfiguration(IPEnabled=True)
        
        self.dns_list = self.load_dns_list()
        
        self.initUI()

    def initUI(self):
        # Get the path to the icon
        if hasattr(sys, '_MEIPASS'):
            icon_path = os.path.join(sys._MEIPASS, 'icon.png')
        else:
            icon_path = 'icon.png'

        self.setWindowIcon(QIcon(icon_path))
        
        # Set window properties
        self.setWindowTitle(f'DNS Changer v{__version__}')
        screen = QApplication.primaryScreen()
        dpi = screen.logicalDotsPerInch()
        scale_factor = dpi / 96.0  # 96 DPI is the standard DPI
        width = int(420 * scale_factor)
        height = int(200 * scale_factor)
        self.setFixedSize(width, height)

        # Create layout
        grid = QGridLayout()
        grid.setSpacing(int(10 * scale_factor))

        # Add widgets
        title = QLabel('DNS Changer')
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QtGui.QFont('Times', int(16 * scale_factor), QtGui.QFont.Bold))

        dnsLabel = QLabel('DNS Server:')
        dnsLabel.setFont(QtGui.QFont('Times', int(9 * scale_factor)))
        
        self.dnsCombo = QComboBox()
        self.update_dns_combo()
        self.dnsCombo.setFont(QtGui.QFont('Helvetica', int(8 * scale_factor)))
        self.dnsCombo.setMinimumWidth(int(250 * scale_factor))
        
        self.setDNSBtn = QPushButton('Set DNS')
        self.setDNSBtn.clicked.connect(self.setDNS)        
        self.setDNSBtn.setFont(QtGui.QFont('Helvetica', int(9 * scale_factor)))
        self.setDNSBtn.setMinimumWidth(int(150 * scale_factor))
        
        self.clearDNSBtn = QPushButton('Clear DNS')
        self.clearDNSBtn.clicked.connect(self.clearDNS)
        self.clearDNSBtn.setFont(QtGui.QFont('Helvetica', int(9 * scale_factor)))
        self.clearDNSBtn.setMinimumWidth(int(90 * scale_factor))

        self.addDNSBtn = QPushButton('Add')
        self.addDNSBtn.clicked.connect(self.add_custom_dns)
        self.addDNSBtn.setFont(QtGui.QFont('Helvetica', int(8 * scale_factor)))
        self.addDNSBtn.setMaximumWidth(int(90 * scale_factor))

        self.removeDNSBtn = QPushButton('Remove')
        self.removeDNSBtn.clicked.connect(self.remove_dns)
        self.removeDNSBtn.setFont(QtGui.QFont('Helvetica', int(8 * scale_factor)))
        self.removeDNSBtn.setMaximumWidth(int(90 * scale_factor))
        
        self.progress = QProgressBar()
        self.progress.setTextVisible(False)
        self.progress.setFont(QtGui.QFont('Helvetica', int(1 * scale_factor)))
        
        self.status_label = QLabel('')
        self.status_label.setFont(QtGui.QFont('Helvetica', int(7 * scale_factor)))
        self.status_label.setStyleSheet("QLabel {color: green; border: 1px solid darkGreen; border-radius: 5px; padding: 3px;}")

        footer = QLabel('<a href="https://github.com/Mahdi1160/DNSChanger">Github</a> | MIT License Copyright (c) 2024 MahdiG')
        footer.setAlignment(Qt.AlignCenter)
        footer.setFont(QtGui.QFont('Helvetica', int(8 * scale_factor)))
        footer.setStyleSheet("QLabel {color: gray;}")
        footer.setOpenExternalLinks(True)

        grid.addWidget(self.status_label, 5, 0, 1, 2)

        grid.addWidget(title, 0, 0, 1, 2)
        grid.addWidget(dnsLabel, 1, 0)
        grid.addWidget(self.dnsCombo, 1, 1)
        grid.addWidget(self.clearDNSBtn, 2, 0)
        grid.addWidget(self.setDNSBtn, 2, 1)
        grid.addWidget(self.removeDNSBtn, 3, 0)
        grid.addWidget(self.addDNSBtn, 3, 1)
        grid.addWidget(footer, 6, 0, 1, 2)
        
        self.setLayout(grid)
        
        # Set palette
        self.palette = self.palette()
        self.palette.setColor(QPalette.Window, QColor(240, 240, 240))
        self.setPalette(self.palette)

        self.show()


    def setDNS(self):
        
        # Disable set button
        self.setDNSBtn.setEnabled(False)
        
        # Get selected DNS
        dns = self.dnsCombo.currentText()
        dns_name = dns.split(' - ')[0]
        dns_pair = self.dns_list[dns_name]
            
        # Set DNS  
        self.set_dns(dns_pair)
        
        # Re-enable button
        self.setDNSBtn.setEnabled(True)

    def set_dns(self, dns_pair):
      
        self.progress.setValue(0)
      
        for i, adapter in enumerate(self.adapters):
          
            adapter.SetDNSServerSearchOrder(dns_pair)
          
            pct = int((i+1) / len(self.adapters) * 100)
            self.progress.setValue(pct)
            
        self.status_label.setText(f"DNS set to {dns_pair[0]} and {dns_pair[1]}")
        self.status_label.setStyleSheet("QLabel {color: green; border: 1px solid darkGreen; border-radius: 5px; padding: 3px;}")
        
    def clearDNS(self):
        
        for adapter in self.adapters:
            adapter.SetDNSServerSearchOrder([])
        
        self.status_label.setText("DNS cleared") 
        self.status_label.setStyleSheet("QLabel {color: red; border: 1px solid darkRed; border-radius: 5px; padding: 3px;}")
        self.progress.setValue(0)
        
    def add_custom_dns(self):
        dialog = CustomDNSDialog(self)
        if dialog.exec_():
            name, dns_pair = dialog.get_dns()
            if self.validate_ip(dns_pair[0]) and self.validate_ip(dns_pair[1]):
                self.dns_list[name] = dns_pair
                self.save_dns_list()
                self.update_dns_combo()
                self.status_label.setText(f"DNS {name} added: {dns_pair[0]}, {dns_pair[1]}")
                self.status_label.setStyleSheet("QLabel {color: green; border: 1px solid darkGreen; border-radius: 5px; padding: 3px;}")
            else:
                QMessageBox.critical(self, "Invalid IP", "Please enter valid IP addresses in the format X.X.X.X")

    def remove_dns(self):
        dns = self.dnsCombo.currentText()
        dns_name = dns.split(' - ')[0]
        if dns_name in self.dns_list:
            reply = QMessageBox.question(self, 'Confirm Remove', f"Are you sure you want to remove DNS {dns_name}?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                del self.dns_list[dns_name]
                self.save_dns_list()
                self.update_dns_combo()
                self.status_label.setText(f"DNS {dns_name} removed")
                self.status_label.setStyleSheet("QLabel {color: red; border: 1px solid darkRed; border-radius: 5px; padding: 3px;}")

        
    def update_dns_combo(self):
        self.dnsCombo.clear()
        for name, dns_pair in self.dns_list.items():
            if len(dns_pair) < 2:
                dns_pair.append('')  # Add an empty string if the second address is missing
            self.dnsCombo.addItem(f"{name} - {dns_pair[0]}, {dns_pair[1]}")
        

    def load_dns_list(self):
        default_dns_list = {
            "Google": ["8.8.8.8", "8.8.4.4"],
            "Cloudflare": ["1.1.1.1", "1.0.0.1"],
            "Electro": ["78.157.42.100", "78.157.42.101"],
            "Shekan": ["178.22.122.100", "185.51.200.2"],
            "Radar Games": ["10.202.10.10", "10.202.10.11"]
        }

        try:
            with open('dns_list.json', 'r') as file:
                dns_list = json.load(file)
                if not isinstance(dns_list, dict):
                    raise ValueError("Invalid content")
                return dns_list
        except (FileNotFoundError, ValueError, json.JSONDecodeError):
            with open('dns_list.json', 'w') as file:
                json.dump(default_dns_list, file, indent=4)
            return default_dns_list

        
    def save_dns_list(self):
        with open('dns_list.json', 'w') as file:
            json.dump(self.dns_list, file)

    def validate_ip(self, ip):
        pattern = re.compile(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")
        if pattern.match(ip):
            parts = ip.split(".")
            for part in parts:
                if int(part) < 0 or int(part) > 255:
                    return False
            return True
        return False

class CustomDNSDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setWindowTitle('Add Custom DNS')
        self.resize(300, 200)
        
        layout = QVBoxLayout()
        
        self.nameInput = QLineEdit()
        self.nameInput.setPlaceholderText('Enter DNS name')
        self.nameInput.setFont(QtGui.QFont('Helvetica', 9))
        
        self.dnsInput1 = QLineEdit()
        self.dnsInput1.setPlaceholderText('Enter primary DNS address (e.g. 8.8.8.8)')
        self.dnsInput1.setFont(QtGui.QFont('Helvetica', 9))
        
        self.dnsInput2 = QLineEdit()
        self.dnsInput2.setPlaceholderText('Enter secondary DNS address (e.g. 8.8.4.4)')
        self.dnsInput2.setFont(QtGui.QFont('Helvetica', 9))
        
        buttonLayout = QHBoxLayout()
        self.okButton = QPushButton('OK')
        self.okButton.clicked.connect(self.accept)
        self.cancelButton = QPushButton('Cancel')
        self.cancelButton.clicked.connect(self.reject)
        
        buttonLayout.addWidget(self.okButton)
        buttonLayout.addWidget(self.cancelButton)
        
        layout.addWidget(self.nameInput)
        layout.addWidget(self.dnsInput1)
        layout.addWidget(self.dnsInput2)
        layout.addLayout(buttonLayout)
        
        self.setLayout(layout)
        
    def get_dns(self):
        name = self.nameInput.text()
        dns_pair = [self.dnsInput1.text(), self.dnsInput2.text()]
        return name, dns_pair

if __name__ == '__main__':
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
    
    app = QApplication(sys.argv)
    dnsChanger = DNSChanger()
    sys.exit(app.exec_())

