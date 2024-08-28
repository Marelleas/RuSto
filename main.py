# -*- coding: utf-8 -*-
import sys
import json
from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt, QSize, QUrl
from PyQt6.QtGui import QIcon, QPixmap, QFont, QTextDocument, QDesktopServices
from html import unescape
from main_ui import Ui_MainWindow

class NewWindow(QDialog):
    def __init__(self, task_num):
        super().__init__()
        self.task_num = task_num
        self.setWindowTitle(f"Задание {self.task_num}")
        self.setGeometry(50, 100, 1300, 600)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)

        self.text_browser = QTextBrowser() 
        self.scroll.setWidget(self.text_browser)

        layout = QVBoxLayout()
        layout.addWidget(self.scroll)
        self.setLayout(layout)

class TestWindow(QDialog):
    def __init__(self, task_num):
        super().__init__()
        self.task_num = task_num

        self.setWindowTitle(f"Задание {self.task_num}")
        self.setGeometry(50, 100, 1300, 600)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)

        self.text_browser = QTextBrowser()
        self.edit = QLineEdit()
        self.edit.resize(400, 50)
        self.button = QPushButton("Проверка", self)
        self.prev_button = QPushButton("<=", self)
        self.next_button = QPushButton("=>", self)

        self.scroll.setWidget(self.text_browser)

        layout = QVBoxLayout()
        Hlayout = QHBoxLayout()

        Hlayout.addWidget(self.edit)
        Hlayout.addWidget(self.button) 
        Hlayout.addWidget(self.prev_button) 
        Hlayout.addWidget(self.next_button)

        layout.addWidget(self.scroll)
        layout.addLayout(Hlayout)

        self.setLayout(layout)

        self.button.clicked.connect(self.check_answer)
        self.prev_button.clicked.connect(self.prev_example)
        self.next_button.clicked.connect(self.next_example)

        self.current_example = 0

        with open(r"./Praktika/tasks.json", 'r', encoding='utf-8') as f:
            data = json.load(f)

        task = next((task for task in data['tasks'] if task['task_number'] == int(task_num)), None)

        if task is not None:
            self.total_examples = len(task['examples'])
            self.text_browser.setHtml(unescape(task['examples'][self.current_example]['example']))
        
    def check_answer(self):
        answer = self.edit.text()
        example = self.get_current_example()

        if answer == example['answer']:
            self.edit.setStyleSheet("background-color: green; color: white;")
        else:
            self.edit.setStyleSheet("background-color: red; color: white;")

    def prev_example(self):
        if self.current_example > 0:
            self.current_example -= 1
            self.text_browser.setHtml(unescape(self.get_current_example()['example']))
        self.edit.setStyleSheet('')
        self.edit.clear()

    def next_example(self):
        if self.current_example < self.total_examples - 1:
            self.current_example += 1
            self.text_browser.setHtml(unescape(self.get_current_example()['example']))
        self.edit.setStyleSheet('')
        self.edit.clear()

    def get_current_example(self):
        with open(r"./Praktika/tasks.json", 'r', encoding='utf-8') as f:
            data = json.load(f)

        task = next((task for task in data['tasks'] if task['task_number'] == int(self.task_num)), None)

        if task is not None:
            example = task['examples'][self.current_example]
            example['example'] = example['example'].encode('utf-8').decode('utf-8')
            return example

        return None

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowIcon(QIcon(r"icon\Logo.png"))
        self.setWindowTitle("РУСТО")

        self.title_label = self.ui.title_label
        self.title_label.setText("РУСТО")

        self.title_icon = self.ui.title_icon
        self.title_icon.setText("")
        self.title_icon.setPixmap(QPixmap(r"icon\Logo.png"))
        self.title_icon.setScaledContents(True)

        self.side_menu = self.ui.listWidget
        self.side_menu.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.side_menu_icon_only = self.ui.listWidget_icon_only
        self.side_menu_icon_only.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.side_menu_icon_only.hide()

        self.menu_btn = self.ui.menu_btn
        self.menu_btn.setText("")
        self.menu_btn.setIcon(QIcon(r"icon\close.svg"))
        self.menu_btn.setIconSize(QSize(30, 30))
        self.menu_btn.setCheckable(True)
        self.menu_btn.setChecked(False)

        self.main_content = self.ui.stackedWidget

        self.menu_list = [
            {
                "name": "Теория",
                "icon": r"icon\orders.svg"
            },
            {
                "name": "Практика",
                "icon": r"icon\reports.svg"
            },
            {
                "name": "NGGYU",
                "icon": r"icon\customers.svg"
            },
        ]

        self.init_list_widget()
        self.init_stackwidget()
        self.init_single_slot()


    def init_single_slot(self):
        self.menu_btn.toggled['bool'].connect(self.side_menu.setHidden)
        self.menu_btn.toggled['bool'].connect(self.title_label.setHidden)
        self.menu_btn.toggled['bool'].connect(self.side_menu_icon_only.setVisible)
        self.menu_btn.toggled['bool'].connect(self.title_icon.setHidden)

        self.side_menu.currentRowChanged['int'].connect(self.main_content.setCurrentIndex)
        self.side_menu_icon_only.currentRowChanged['int'].connect(self.main_content.setCurrentIndex)
        self.side_menu.currentRowChanged['int'].connect(self.side_menu_icon_only.setCurrentRow)
        self.side_menu_icon_only.currentRowChanged['int'].connect(self.side_menu.setCurrentRow)
        self.menu_btn.toggled.connect(self.button_icon_change)
        self.side_menu.currentRowChanged.connect(self.change_content)

    def init_list_widget(self):
        self.side_menu_icon_only.clear()
        self.side_menu.clear()

        for menu in self.menu_list:
            item = QListWidgetItem()
            item.setIcon(QIcon(menu.get("icon")))
            item.setSizeHint(QSize(40, 40))
            self.side_menu_icon_only.addItem(item)
            self.side_menu_icon_only.setCurrentRow(0)

            item_new = QListWidgetItem()
            item_new.setIcon(QIcon(menu.get("icon")))
            item_new.setText(menu.get("name"))
            self.side_menu.addItem(item_new)
            self.side_menu.setCurrentRow(0)

    def init_stackwidget(self):
        widget_list = self.main_content.findChildren(QWidget)
        for widget in widget_list:
            self.main_content.removeWidget(widget)

        for menu in self.menu_list:
            text = menu.get("name")
            layout = QGridLayout()
            label = QLabel(text)
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            font = QFont()
            font.setPixelSize(20)
            label.setFont(font)
            layout.addWidget(label)
            new_page = QWidget()
            new_page.setLayout(layout)
            self.main_content.addWidget(new_page)

    def button_icon_change(self, status):
        if status:
            self.menu_btn.setIcon(QIcon(r"icon\open.svg"))
        else:
            self.menu_btn.setIcon(QIcon(r"icon\close.svg"))

    def change_content(self, row):
        widget_list = self.main_content.findChildren(QWidget)
        for widget in widget_list:
            self.main_content.removeWidget(widget)

        if row == 0:
            layout = QGridLayout()
            teor_buttons = []
            for i in range(1, 27):
                teor_button = QPushButton(f"Теория {i}")
                teor_button.clicked.connect(lambda checked, num=i+100: self.open_new_window(num))
                teor_buttons.append(teor_button)
                layout.addWidget(teor_button)
            new_page = QWidget()
            new_page.setLayout(layout)
            self.main_content.addWidget(new_page)
        elif row == 1:
            layout = QGridLayout()
            pract_buttons = []
            for i in range(1, 27):
                pract_button = QPushButton(f"Задание {i}")
                pract_button.clicked.connect(lambda checked, num=i: self.open_new_window(num))
                pract_buttons.append(pract_button)
                layout.addWidget(pract_button)
            new_page = QWidget()
            new_page.setLayout(layout)
            self.main_content.addWidget(new_page)
        elif row == 2:
            self.play_rick_roll()
        
    def play_rick_roll(self):
        self.video_window = QWidget()
        video_layout = QVBoxLayout()

        video_label = QLabel()
        video_btn = QPushButton("Hmmmmm....")
        video_btn.clicked.connect(lambda: self.open_video_in_browser("https://www.youtube.com/watch?v=dQw4w9WgXcQ"))

        video_layout.addWidget(video_btn)
        video_layout.addWidget(video_label)

        self.video_window.setLayout(video_layout)
        self.main_content.addWidget(self.video_window)

    def open_video_in_browser(self, url):
        QDesktopServices.openUrl(QUrl(url))
        

    def open_new_window(self, num):
        if num >= 101 and num <= 127:
            num = num % 100
            new_window = NewWindow(str(num))
            filename = f'.\\Text_theory\\Task_{num}.html'
            with open(filename, "r", encoding='utf-8') as f:
                content = f.read()
                document = QTextDocument()
                document.setHtml(unescape(content))
                new_window.text_browser.setDocument(document)
        
        elif 1 <= num <= 27:
            new_window = TestWindow(str(num))
            with open(r"./Praktika/tasks.json", 'r', encoding='utf-8') as f:
                data = json.load(f)

            for task in data['tasks']:
                if task['task_number'] == num:
                    document = QTextDocument()
                    text = task['examples'][0]['example']
                    document.setHtml(text)
                    new_window.text_browser.setDocument(document)
                    break
        new_window.exec()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    with open(r"style.qss") as f:
        style_str = f.read()

    app.setStyleSheet(style_str)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())

