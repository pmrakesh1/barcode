from barcode import get_barcode_class


import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QWidget
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
import barcode
from barcode.writer import ImageWriter
import io
class BarcodeGenerator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Barcode Generator")
        self.setGeometry(200, 200, 400, 400) 
        
        self.initUI()

    def initUI(self):
        """
        Initializes the user interface with labels, input fields, and buttons for generating barcodes.
        """
        layout = QVBoxLayout()

        # Label and input for barcode data
        self.label_data = QLabel("Enter Data:")
        layout.addWidget(self.label_data)
        self.input_data = QLineEdit()
        self.input_data.textChanged.connect(self.preview_barcode)
        layout.addWidget(self.input_data)

        # Label and input for save path
        self.label_path = QLabel("Save Path:")
        layout.addWidget(self.label_path)
        self.input_path = QLineEdit()
        layout.addWidget(self.input_path)

        # Browse button for selecting save path
        self.btn_browse = QPushButton("Browse")
        self.btn_browse.clicked.connect(self.browse_path)
        layout.addWidget(self.btn_browse)

        # Generate button to create the barcode
        self.btn_generate = QPushButton("Generate Barcode")
        self.btn_generate.clicked.connect(self.save_barcode)
        layout.addWidget(self.btn_generate)

        # Live preview for the barcode
        self.preview_label = QLabel("Barcode Preview:")
        self.preview_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.preview_label)

        # Setting layout to main window
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def browse_path(self):
        """
        Opens a directory selection dialog and updates the save path input.
        """
        path = QFileDialog.getExistingDirectory(self, "Select Save Directory")
        if path:
            self.input_path.setText(path)

    def save_barcode(self):
        """
        Saves the barcode to the specified directory.
        """
        data = self.input_data.text()
        path = self.input_path.text()
        

        if not data:
            self.show_message("Error", "Please enter the data for the barcode.", error=True)
            return

        if not path:
            self.show_message("Error", "Please select a valid save path.", error=True)
            return

        try:
            # Generating the barcode
            EAN = barcode.get_barcode_class('code128')
           
            ean = EAN(data, writer=ImageWriter())
            
            
            #full_path = path.join(path, f"{data}.png")
            full_path = path+"/"+data+".png"
            ean.save(full_path)
            self.show_message("Success", f"Barcode saved successfully at:\n{full_path}")
        except Exception as e:
            self.show_message("Error", f"Failed to save barcode.\nError: {str(e)}", error=True)

    def preview_barcode(self):
        """
        Generates and updates a live preview of the barcode in the preview label.
        """
        data = self.input_data.text()
        if not data:
            self.preview_label.setText("Enter data to see live preview")
            self.preview_label.setPixmap(QPixmap())
            return

        try:
            # Generating the barcode preview
            EAN = barcode.get_barcode_class('code128')
            ean = EAN(data, writer=ImageWriter())
            output = io.BytesIO()
            ean.write(output, options={"module_height": 10.0, "font_size": 10})

            # Convert the BytesIO output to a QImage
            output.seek(0)
            image = QImage()
            image.loadFromData(output.read(), "PNG")
            pixmap = QPixmap.fromImage(image)

            # Display the barcode preview in the QLabel
            self.preview_label.setPixmap(pixmap.scaled(300, 100, Qt.KeepAspectRatio))
        except Exception as e:
            self.preview_label.setText(f"Preview generation failed: {str(e)}")

    def show_message(self, title, message, error=False):
        """
        Displays a message to the user in the preview label (can be enhanced with QMessageBox).
        """
        color = "red" if error else "green"
        self.preview_label.setStyleSheet(f"color: {color};")
        self.preview_label.setText(message)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BarcodeGenerator()
    window.show()
    sys.exit(app.exec_())
    