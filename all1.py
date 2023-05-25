import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QGridLayout
from PyQt5.QtGui import QPixmap, QPainter, QColor, QPen, QPainterPath
from PyQt5.QtCore import Qt, QSize, QRectF, QTimer
from PyQt5.QtNetwork import QTcpSocket


class CircleLabel(QWidget):
    def __init__(self, color, parent=None):
        super().__init__(parent)
        self.setMinimumSize(QSize(50, 50))  # Set the desired size of the circle label
        self.color = color

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Calculate the size of the circle
        size = min(self.width(), self.height())

        # Calculate the position to center the circle within the widget
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2

        # Create a rounded rectangle path with a radius equal to half of the circle's size
        rect = QRectF(x, y, size, size)
        path = QPainterPath()
        path.addRoundedRect(rect, size / 2, size / 2)

        # Set the brush color and fill the path
        painter.setBrush(QColor(self.color))

        # Set the pen color and width for the border line
        pen = QPen(QColor("black"))
        pen.setWidth(2)
        painter.setPen(pen)

        # Draw the circle and border
        painter.drawEllipse(rect)
        painter.drawPath(path)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()


        # Create a QTcpSocket for communication with the Pi server
        self.socket = QTcpSocket(self)
        self.socket.connectToHost('192.168.24.26', 6000)
        self.socket.readyRead.connect(self.receive_data)
 
        self.setWindowTitle("Robot GUI")
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QHBoxLayout(central_widget)

        # Camera streams
        camera_widget = QWidget()
        camera_layout = QGridLayout(camera_widget)

        camera1_label = QLabel()
        camera2_label = QLabel()

        camera_layout.addWidget(camera1_label, 0, 0)
        camera_layout.addWidget(camera2_label, 1, 0)

        layout.addWidget(camera_widget)

        # Rest of the GUI components
        components_widget = QWidget()
        components_layout = QVBoxLayout(components_widget)

        # Fire icon
        self.fire_icon_label = QLabel()
        fire_icon_image = QPixmap('fire_icon.png')  # Replace with the path to your fire icon image
        self.fire_icon_label.setPixmap(fire_icon_image)
        components_layout.addWidget(self.fire_icon_label)        # Number displays
        
        self.x_position_label = QLabel()
        self.y_position_label = QLabel()
        self.temperature1_label = QLabel()
        self.temperature2_label = QLabel()
        components_layout.addWidget(self.x_position_label)
        components_layout.addWidget(self.y_position_label)
        components_layout.addWidget(self.temperature1_label)
        components_layout.addWidget(self.temperature2_label)

        # Circles
        circles_widget = QWidget()
        circles_layout = QHBoxLayout(circles_widget)

        self.circle1_label = CircleLabel("blue")
        self.circle2_label = CircleLabel("blue")
        self.circle3_label = CircleLabel("blue")
        self.circle4_label = CircleLabel("blue")

        circles_layout.addWidget(self.circle1_label)
        circles_layout.addWidget(self.circle2_label)
        circles_layout.addWidget(self.circle3_label)
        circles_layout.addWidget(self.circle4_label)

        components_layout.addWidget(circles_widget)

        layout.addWidget(components_widget)

        # Set layout alignments
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        camera_widget.setMaximumWidth(int(self.width() / 2))
        components_widget.setMinimumWidth(int(self.width() / 2))

        # Update values periodically
        self.timer = QTimer()
        self.timer.timeout.connect(self.receive_data)
        self.timer.start(1000)  # Update every 1 second


    def receive_data(self):
        # Read the received data from the socket
        data = self.socket.readAll().data().decode()

        # Extract values from the received data
        data = data.split(',')

        if len(data) >= 9:
            # Extract values from the data array
            x_position = int(data[0])
            y_position = int(data[1])
            temperature1 = float(data[2])
            temperature2 = float(data[3])
            array_values = list(map(int, data[4:]))

            # Update fire icon glow
            if array_values[0] == 1:
                self.fire_icon_label.setStyleSheet("background-color: red")
            else:
                self.fire_icon_label.setStyleSheet("background-color: none")

            # Update x, y, and sensors values
            self.x_position_label.setText(f"X Position: {x_position}")
            self.y_position_label.setText(f"Y Position: {y_position}")
            self.temperature1_label.setText(f"Temperature 1: {temperature1}")
            self.temperature2_label.setText(f"Temperature 2: {temperature2}")

            # Update circle colors
            self.circle1_label.color = "green" if array_values[1] == 1 else "blue"
            self.circle2_label.color = "green" if array_values[2] == 1 else "blue"
            self.circle3_label.color = "green" if array_values[3] == 1 else "blue"
            self.circle4_label.color = "green" if array_values[4] == 1 else "blue"

            # Trigger a repaint of the circles
            self.circle1_label.update()
            self.circle2_label.update()
            self.circle3_label.update()
            self.circle4_label.update()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
