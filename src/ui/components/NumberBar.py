from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import QRect, pyqtSlot, Qt
from PyQt6.QtGui import QPainter, QColor







class NumberBar(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.editor = editor
        self.editor.blockCountChanged.connect(self.update_width)
        self.editor.updateRequest.connect(self.update_area)
        self.update_width(0)

    def update_width(self, _):
        digits = len(str(self.editor.blockCount()))
        space = 10 + self.fontMetrics().horizontalAdvance('9') * digits
        self.setFixedWidth(space)

    @pyqtSlot(QRect, int)
    def update_area(self, rect, dy):
        if dy:
            self.scroll(0, dy)
        else:
            self.update(0, rect.y(), self.width(), rect.height())
        if rect.contains(self.editor.viewport().rect()):
            self.update_width(0)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(event.rect(), QColor(240, 240, 240))

        block = self.editor.firstVisibleBlock()
        block_number = block.blockNumber()
        top = self.editor.blockBoundingGeometry(block).translated(self.editor.contentOffset()).top()
        bottom = top + self.editor.blockBoundingRect(block).height()

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(block_number + 1)
                painter.setPen(Qt.GlobalColor.black)
                font = painter.font()
                font.setBold(True)
                painter.setFont(font)
                width = self.width()
                height = self.fontMetrics().height()
                painter.drawText(0, int(top), width - 5, height, Qt.AlignmentFlag.AlignRight, number)
            block = block.next()
            top = bottom
            bottom = top + self.editor.blockBoundingRect(block).height()
            block_number += 1
