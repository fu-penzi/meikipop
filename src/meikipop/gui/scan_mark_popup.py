from typing import List, Optional

from PyQt6.QtCore import QTimer, QPoint, QSize
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QCursor, QFont, QFontMetrics, QFontInfo
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame, QApplication
from meikipop.dictionary.lookup import DictionaryEntry
from meikipop.config.config import config

class ScanMarkPopup(QWidget):
    def __init__(self):
        super().__init__()
        self.is_visible = False
        self.width = 0
        self.height = 0
        self.x = 0
        self.y = 0
        self.probe_label = QLabel()
        self.probe_label.setWordWrap(True)
        self.probe_label.setTextFormat(Qt.TextFormat.RichText)

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setStyleSheet("background: transparent;")

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        self.frame = QFrame()
        self._apply_frame_stylesheet()
        main_layout.addWidget(self.frame)

        self.content_layout = QVBoxLayout(self.frame)
        self.content_layout.setContentsMargins(0, 0, 0, 0)

        self.display_label = QLabel()
        self.display_label.setWordWrap(True)
        self.display_label.setTextFormat(Qt.TextFormat.RichText)
        self.content_layout.addWidget(self.display_label)
        self.screen = QApplication.primaryScreen()
        self.devicePixelRatio = self.screen.devicePixelRatio()

        self.words = []
        self.img_w = 0
        self.current_marked_text = ""
        self.hide()

    def set_fixed_height(self, height):
        height = max(0, height - 10)
        if height != self.height:
            self.height = height

    def move(self, x, y):
        x = int(x / self.devicePixelRatio)
        y = int(y / self.devicePixelRatio)
        if (x, y) != (self.x, self.y):
            self.x = x
            self.y = y

    def show(self, entries: Optional[List[DictionaryEntry]]):
        if config.highlight_enabled is False:
            return

        if entries is None or len(entries) == 0:
            self.hide()
            return

        if entries[0].written_form != self.current_marked_text:
            self.current_marked_text = entries[0].written_form
            char_num = len(self.current_marked_text)
            width = 0
            last_word_idx = 0
            for word in self.words:
                if char_num <= 0:
                    break
                char_num -= len(word.text)
                last_word_idx += 1
            last_word_idx = max(0, last_word_idx - 1)
            left_edge = self.words[0].box.center_x - (self.words[0].box.width / 2)
            right_edge = self.words[last_word_idx].box.center_x + (self.words[last_word_idx].box.width / 2)
            width = right_edge - left_edge
            self.width = width

        super().move(self.x, self.y)
        super().setFixedWidth(int(self.width * self.img_w / self.devicePixelRatio))
        super().setFixedHeight(self.height)
        if not self.is_visible:
            super().show()
            self.is_visible = True  

    def hide(self):
        if self.is_visible:
            super().hide()
            self.is_visible = False

    def _apply_frame_stylesheet(self):
        bg_color = QColor(255)
        r, g, b = bg_color.red(), bg_color.green(), bg_color.blue()
        a = 0.2
        self.probe_label.setFont(QFont('Arial'))
        self.frame.setStyleSheet(f"""
            QFrame {{
                background-color: rgba({r}, {g}, {b}, {a});
                color: white;
                border-radius: 8px;
                border: 1px solid #555;
            }}
            QLabel {{
                background-color: transparent;
                border: none;
                font-family: "Arial";
            }}
            hr {{
                border: none;
                height: 1px;
            }}
        """)