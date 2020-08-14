import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QDate,   QDateTime , QTime

class DateTimeEditDemo(QWidget):
    def __init__(self):
        super(DateTimeEditDemo, self).__init__()
        self.initUI()

    def initUI(self):
        #设置窗口的标题与初始大小
        self.setWindowTitle('QDateTimeEdit例子')
        self.resize(300, 90)

        #垂直布局
        vlayout = QVBoxLayout()

        #实例化编辑时间日期的控件

        #默认下，不指定日期的时间，系统会设置一个和本地相同的日期时间格式，时间默认2000年1月1日0时0分0秒
        dateTimeEdit = QDateTimeEdit(self)
        #指定当前日期时间为控件的日期时间
        dateTimeEdit2 = QDateTimeEdit(QDateTime.currentDateTime(), self)
        #指定当前地日期为控件的日期，注意没有指定时间
        dateEdit = QDateTimeEdit(QDate.currentDate(), self)
        #指定当前地时间为控件的时间，注意没有指定日期
        timeEdit = QDateTimeEdit(QTime.currentTime(), self)

        # 设置日期时间格式，可以选择/ . : -等符号自定义数据连接符
        dateTimeEdit.setDisplayFormat("yyyy-MM-dd HH:mm:ss")
        dateTimeEdit2.setDisplayFormat("yyyy/MM/dd HH-mm-ss")
        dateEdit.setDisplayFormat("yyyy.MM.dd")
        timeEdit.setDisplayFormat("HH:mm:ss")

        #布局控件添加，设置主窗口的布局
        vlayout.addWidget( dateTimeEdit )
        vlayout.addWidget( dateTimeEdit2)
        vlayout.addWidget( dateEdit )
        vlayout.addWidget( timeEdit )
        self.setLayout(vlayout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = DateTimeEditDemo()
    demo.show()
    sys.exit(app.exec_())