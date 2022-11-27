import sys
from PyQt5.Qt import *
from PyQt5 import QtWidgets, QtCore, QtGui


class Ui_application_pages(object):
    def setupUi(self, application_pages):
        if not application_pages.objectName():
            application_pages.setObjectName(u"application_pages")
        application_pages.resize(1056, 657)
        
        self.page_1 = QWidget()
        self.page_1.setObjectName(u"page_1")
#        self.page_1.setStyleSheet(dark_theme)              # ? dark_theme
        self.centrallayout = QHBoxLayout(self.page_1)     
        self.centrallayout.setObjectName(u"centrallayout")

        self.textEdit = PlainTextEdit()                     # QPlainTextEdit()
        self.textEdit.setObjectName(u"lineEdit")
        self.centrallayout.addWidget(self.textEdit)


class LineNumberArea(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.myeditor = editor

    def sizeHint(self):
        return Qsize(self.editor.lineNumberAreaWidth(), 0)

    def paintEvent(self, event):
        self.myeditor.lineNumberAreaPaintEvent(event)


class PlainTextEdit(QPlainTextEdit):
    def __init__(self):
        super().__init__()
        
        self.setTabStopDistance(QFontMetricsF(self.font()).width(' ') * 4)
        self.lineNumberArea = LineNumberArea(self)
        self.blockCountChanged[int].connect(self.updateLineNumberAreaWidth)
        self.updateRequest[QRect,int].connect(self.updateLineNumberArea)
        self.cursorPositionChanged.connect(self.highlightCurrentLine)
        self.updateLineNumberAreaWidth(0)

    def lineNumberAreaWidth(self):
        digits = 1
        count = max(1, self.blockCount())
        while count >= 10:
            count   /= 10
            digits  +=  1
        space = 3 + self.fontMetrics().width('9') * digits
        return space

    def updateLineNumberAreaWidth(self, _):
        self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)

    def updateLineNumberArea(self, rect, dy):
        if dy:
            self.lineNumberArea.scroll(0, dy)
        else:
            self.lineNumberArea.update(0, rect.y(), self.lineNumberArea.width(),
                       rect.height())

        if rect.contains(self.viewport().rect()):
            self.updateLineNumberAreaWidth(0)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect();
        self.lineNumberArea.setGeometry(QRect(cr.left(), cr.top(),
                    self.lineNumberAreaWidth(), cr.height()))

    def lineNumberAreaPaintEvent(self, event):
        mypainter = QPainter(self.lineNumberArea)
        mypainter.fillRect(event.rect(), Qt.lightGray)

        block       = self.firstVisibleBlock()
        blockNumber = block.blockNumber()
        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        bottom = top + self.blockBoundingRect(block).height()

        height = self.fontMetrics().height()
        while block.isValid() and (top <= event.rect().bottom()):
            if block.isVisible() and (bottom >= event.rect().top()):
                number = str(blockNumber + 1)
                mypainter.setPen(Qt.black)
                mypainter.drawText(0, top, self.lineNumberArea.width(), height,
                 Qt.AlignRight, number)

            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            blockNumber += 1

    def highlightCurrentLine(self):
        extraSelections = []
        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()
            lineColor = QColor(Qt.yellow).lighter(160)
            selection.format.setBackground(lineColor)
            selection.format.setProperty(QTextFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extraSelections.append(selection)
        self.setExtraSelections(extraSelections)


class MainWindow(QWidget, Ui_application_pages):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.page_1)


StyleSheet = """
QScrollBar:vertical {              
    border: none;
    background: white;
    width: 5px;               
    margin: 0px 0px 0px 0px;
    min-height: 0px;  
}
QScrollBar::handle:vertical {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
    stop: 0 rgb(32, 47, 130), stop: 0.5 rgb(32, 47, 130), stop:1 rgb(32, 47, 130));
    min-height: 0px;
}
QScrollBar::add-line:vertical {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
    stop: 0 rgb(32, 47, 130), stop: 0.5 rgb(32, 47, 130),  stop:1 rgb(32, 47, 130));
    height: 0px;
    subcontrol-position: bottom;
    subcontrol-origin: margin;
}
QScrollBar::sub-line:vertical {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
    stop: 0  rgb(32, 47, 130), stop: 0.5 rgb(32, 47, 130),  stop:1 rgb(32, 47, 130));
    height: 0 px;
    subcontrol-position: top;
    subcontrol-origin: margin;
}
"""

QSS = '''
QWidget {
    background-color: #1a1a26;
}
/* VERTICAL SCROLLBAR */
QScrollBar:vertical {
    border: none;
    background: rgb(45, 45, 68);
    width: 14px;
    margin: 15px 0 15px 0;
    border-radius: 0px;
}

/*  HANDLE BAR VERTICAL */
QScrollBar::handle:vertical {
    background-color: rgb(80, 80, 122);
    min-height: 30px;
    border-radius: 7px;
}
QScrollBar::handle:vertical:hover{
    background-color: rgb(255, 0, 127);
}
QScrollBar::handle:vertical:pressed {
    background-color: rgb(185, 0, 92);
}

/* BTN TOP - SCROLLBAR */
QScrollBar::sub-line:vertical {
    border: none;
    background-color: rgb(59, 59, 90);
    height: 15px;
    border-top-left-radius: 7px;
    border-top-right-radius: 7px;
    subcontrol-position: top;
    subcontrol-origin: margin;
}
QScrollBar::sub-line:vertical:hover { 
    background-color: rgb(255, 0, 127);
}
QScrollBar::sub-line:vertical:pressed {
    background-color: rgb(185, 0, 92);
}

/* BTN BOTTOM - SCROLLBAR */
QScrollBar::add-line:vertical {
    border: none;
    background-color: rgb(59, 59, 90);
    height: 15px;
    border-bottom-left-radius: 7px;
    border-bottom-right-radius: 7px;
    subcontrol-position: bottom;
    subcontrol-origin: margin;
}
QScrollBar::add-line:vertical:hover { 
    background-color: rgb(255, 0, 127);
}
QScrollBar::add-line:vertical:pressed { 
    background-color: rgb(185, 0, 92);
}

/* RESET ARROW */
QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
    background: none;
}
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
    background: none;
}

/* HORIZONTAL SCROLLBAR - HOMEWORK */
QScrollBar:horizontal {
}
QScrollBar::handle:horizontal {
}
QScrollBar::add-line:horizontal {
}
QScrollBar::sub-line:horizontal {
}
QScrollBar::up-arrow:horizontal, QScrollBar::down-arrow:horizontal
{
}
QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal
{
}

QPlainTextEdit{
    background-color: #6D9886;
    border: 3px solid #7611ed;
    border-radius: 10px;
    color: #212121;
    font: 87 15pt \"Segoe UI Black\";
}
     
QTextEdit{
    background-color: #22222e;
    border: 3px solid #7611ed;
    border-radius: 10px;
    color: #f5f5f5;
    font: 87 8pt \"Segoe UI Black\";
}
'''


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(QSS)                # (StyleSheet)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_()) 