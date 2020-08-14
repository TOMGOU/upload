import win_unicode_console
win_unicode_console.enable()
import sys,os
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QDate, QDateTime
from PyQt5.QtWidgets import (QWidget, QPushButton, QLineEdit, QLabel, QComboBox, QDateTimeEdit, QApplication, QFileDialog)
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime
import time
import shutil
# from moviepy.editor import VideoFileClip

class Upload(QWidget):
  def __init__(self):
    super(Upload, self).__init__()
    self.switch = True
    self.initUI()

  def initUI(self):
    #源文件选择按钮和选择编辑框
    self.source_btn = QPushButton('源文件', self)
    self.source_btn.move(30, 30)
    self.source_btn.resize(80,30)
    self.source_btn.clicked.connect(self.select_source)
    self.source_le = QLineEdit(self)
    self.source_le.move(120, 30)
    self.source_le.resize(250,30)

    #抖音视频分类输入框和提示
    self.catLabel = QLabel(self)
    self.catLabel.move(30, 75)
    self.catLabel.resize(100,30)
    self.catLabel.setText("抖音视频分类：")
    self.combo_from = QComboBox(self)	
    self.cat_form = '体育'
    self.combo_from.addItems(['体育', '音乐', '搞笑', '影视', '娱乐', '舞蹈', '情感', '知识', '动植物', '剧情', '游戏', '才艺', '时尚', '美食', '文化教育', '动漫二次元', '亲子', '旅行', '汽车', '科技', '政务', '创意', '校园', '日常生活', '新闻资讯', '三农', '其他'])
    self.combo_from.activated[str].connect(self.onLanFromActivated)  
    self.combo_from.move(120, 75)
    self.combo_from.resize(250, 30)

     #发布时间间隔输入框和提示
    self.gapLabel = QLabel(self)
    self.gapLabel.move(30, 120)
    self.gapLabel.resize(100,30)
    self.gapLabel.setText("发布时间间隔：")
    self.gap_le = QLineEdit('1', self)
    self.gap_le.move(120,120)
    self.gap_le.resize(250, 30)

    # 时间选择器
    self.dateTimeLabel = QLabel(self)
    self.dateTimeLabel.move(30, 165)
    self.dateTimeLabel.resize(100,30)
    self.dateTimeLabel.setText("发布开始时间：")
    self.dateTime_le = QDateTimeEdit(QDateTime.currentDateTime(), self)
    self.dateTime_le.setDisplayFormat("yyyy-MM-dd HH:mm")
    self.dateTime_le.move(120, 165)
    self.dateTime_le.resize(250, 30)

    #上传按钮
    self.save_btn = QPushButton('开始上传',self)
    self.save_btn.move(200, 220)
    self.save_btn.resize(140, 30)
    self.save_btn.clicked.connect(self.kick)

    #用户提示区
    self.result_le = QLabel('视频分类与抖音后台保持一致', self)
    self.result_le.move(30, 270)
    self.result_le.resize(340, 30)
    self.result_le.setStyleSheet('color: blue;')

    #整体界面设置
    self.resize(400, 400)
    self.center()
    self.setWindowTitle('抖音视频自动化上传')#设置界面标题名
    self.show()
  
  # 窗口居中函数
  def center(self):
    screen = QtWidgets.QDesktopWidget().screenGeometry()#获取屏幕分辨率
    size = self.geometry()#获取窗口尺寸
    self.move(int((screen.width() - size.width()) / 2), int((screen.height() - size.height()) / 2))#利用move函数窗口居中

  # 打开的视频文件名称
  def select_source(self):
    dir_path = QFileDialog.getExistingDirectory(self, "请选择文件夹路径", "C:/")
    self.source_le.setText(str(dir_path))

  def set_label_func(self, text):
    self.result_le.setText(text)
  
  def onLanFromActivated(self, text):
    self.cat_form = text

  def switch_func(self, bools):
    self.switch = bools

  def kick(self):
    source = self.source_le.text().strip()#源文件夹路径
    category = self.cat_form.strip()#视频分类
    gap = self.gap_le.text().strip()#时间间隔
    # start_time = str(self.dateTime_le.text())#定时发布开始时间
    # start_time = time.mktime(time.strptime(self.dateTime_le.text(), '%Y-%m-%d %H:%M'))#定时发布开始时间
    start_time = datetime.datetime.strptime(self.dateTime_le.text(),"%Y-%m-%d %H:%M")#定时发布开始时间
    if self.switch and source != '' and category != '' and gap != '':
      self.switch = False
      self.set_label_func('请耐心等待，正在打开浏览器！')
      self.my_thread = MyThread(source, category, gap, start_time, self.set_label_func)#实例化线程对象
      self.my_thread.start()#启动线程
      self.my_thread.my_signal.connect(self.switch_func)

class MyThread(QThread):#线程类
  my_signal = pyqtSignal(bool)  #自定义信号对象。参数bool就代表这个信号可以传一个布尔值
  def __init__(self, source, category, gap, start_time, set_label_func):
    super(MyThread, self).__init__()
    self.source = source
    self.category = category
    self.gap = gap
    self.start_time = start_time
    self.set_label_func = set_label_func

  def run(self): #线程执行函数
    string = self.fetchData(self.source, self.category, self.gap, self.start_time, self.set_label_func)
    self.set_label_func(string)
    self.my_signal.emit(True)  #释放自定义的信号

  def fetchData(self, source, category, gap, start_time, set_label_func):
    upload_file = self.file_name(source)
    total_num = len(upload_file['file_name'])
    if total_num == 0:
      return '您选择的文件夹里没有视频'
    filePath = source + r'/../finished'
    self.makeDir(filePath)
    ###  WINDOWS ###
    # option = webdriver.ChromeOptions()
    # option.add_argument(r'user-data-dir=C:\Users\zhuan\AppData\Local\Google\Chrome\User Data')
    # option.add_argument('--ignore-certificate-errors')
    # browser = webdriver.Chrome(options=option)
    # browser = webdriver.Chrome()
    ###  MAC ###
    option = webdriver.ChromeOptions()
    # option.add_argument(r'user-data-dir=/Users/tangyong/Library/Application Support/Google/Chrome')
    browser = webdriver.Chrome(chrome_options=option, executable_path='/Users/tangyong/Application/chromedriver')
    browser.get('https://creator.douyin.com/content/upload')

    # self.sleep(10)
    WebDriverWait(browser, 100).until(
      EC.presence_of_element_located((By.CLASS_NAME,"semi-button-primary"))
    )
    exiting = self.isElementExist(browser, 'button.semi-button-primary')
    if exiting:
      button = browser.find_element_by_class_name('semi-button-primary')
      button.click()
      self.set_label_func('请扫码登录！')

      WebDriverWait(browser, 600).until(EC.visibility_of_element_located((By.XPATH,'//*[contains(text(),"开始体验") and @class="semi-button-content"]')))
      experience_button = browser.find_element_by_xpath('//*[contains(text(),"开始体验") and @class="semi-button-content"]')
      experience_button.click()
      next_button = browser.find_element_by_xpath('//*[contains(text(),"下一步") and @class="semi-button-content"]')
      next_button.click()
      finish_button = browser.find_element_by_xpath('//*[contains(text(),"完成") and @class="semi-button-content"]')
      finish_button.click()

    index_int = 0
    for index in range(total_num):
      uploadPath = upload_file['url_name'][index]
      # 视频长度判断，后续优化
      # videoDuration = VideoFileClip(uploadPath).duration
      # if videoDuration > 15 * 60:
      #   continue
      progress_str = '视频上传进度:' + str(index + 1) + '/' + str(total_num)
      self.set_label_func(progress_str)
      print(progress_str)

      WebDriverWait(browser, 600).until(EC.visibility_of_element_located((By.XPATH,'//*[contains(text(),"发布视频") and @class="semi-button-content"]')))
      
      self.sleep(3)
      video_upload = browser.find_element_by_xpath('//*[contains(text(),"发布视频") and @class="semi-button-content"]')
      video_upload.click()

      self.sleep(1)
      upload_button = browser.find_element_by_class_name('upload-btn-input--1NeEX')

      self.sleep(1)
      upload_button.send_keys(uploadPath)

      self.sleep(1)
      title_input =  browser.find_element_by_xpath('//div[contains(@class, "public-DraftStyleDefault-block")]/span')
      title_input.send_keys(upload_file['file_name'][index][0:39])

      if self.isElementExist(browser, '.select-value--3XRKF'):
        category_select = browser.find_element_by_class_name('select-value--3XRKF')
        category_select.click()
        cat_text = '//*[contains(text(),"' + category + '")]'
        cat_element = browser.find_element_by_xpath(cat_text)
        cat_element.click()

      timing = browser.find_elements_by_class_name('one-line--3sqFc')[1]
      timing.click()
      
      dist_time = browser.find_element_by_class_name('semi-input-default')
      self.sleep(1)

      time_stamp = start_time + datetime.timedelta(hours = index * int(gap) + index_int * 10 + 2.2)
      hours = int(time_stamp.strftime('%H'))
      if hours > 22 or hours < 9:
        index_int = index_int + 1
        time_stamp = start_time + datetime.timedelta(hours = index * int(gap) + index_int * 10 + 2.2)
      month_time = time_stamp.strftime('%m')
      day_time = str(int(time_stamp.strftime('%d'))) 
      hour_time = int(time_stamp.strftime('%H'))
      minute_time = int(time_stamp.strftime('%M'))
      current_month = start_time.strftime('%m')
      print('预定的发布时间：' + time_stamp.strftime('%Y-%m-%d %H:%M'))
      dist_time.click()
      self.sleep(1)
      if month_time != current_month:
        next_month = browser.find_elements_by_class_name('semi-button semi-button-primary semi-button-borderless semi-button-with-icon just-icon')[1]
        next_month.click()
      time_dom = browser.find_elements_by_class_name('semi-datepicker-switch-text')
      time_dom[0].click()
      target_day = browser.find_element_by_xpath('//div[@class="semi-datepicker-day-main"]/span[text()="' + day_time + '"]')
      target_day.click()
      time_dom[1].click()
      self.sleep(1)
      self.hourLoop(browser, hour_time)
      self.sleep(1)
      self.minuteLoop(browser, minute_time)

      # 关闭时间选择器
      self.sleep(1)
      arrow_element = browser.find_element_by_class_name('semi-icons-chevron_down')
      arrow_element.click()

      WebDriverWait(browser, 600).until(
        EC.presence_of_element_located((By.CLASS_NAME,"upload-myicon--11Yqt"))
      )
      
      distribute = browser.find_element_by_xpath('//button[contains(text(),"发布")]')
      distribute.click()
      self.sleep(2)
      print('第' + str(index + 1) + '个视频发布了')

      if index == 0 and self.isElementExist(browser, '.icon--1x02I'):
        bind_button = browser.find_element_by_class_name('icon--1x02I')
        bind_button.click()

        WebDriverWait(browser, 30).until(
          EC.presence_of_element_located((By.CLASS_NAME,"icon--3ap82"))
        )
        close_icon = browser.find_element_by_class_name('icon--3ap82')
        close_icon.click()
      
      fullFileName = filePath + r'/' + upload_file['full_file_name'][index]
      if os.path.exists(fullFileName):
        os.remove(fullFileName)
      shutil.move(upload_file['url_name'][index], filePath)
      print('第' + str(index + 1) + '个文件被移动到finished文件夹')

    return '自动上传了' + str(total_num) + '个视频，请前往抖音后台查看！'

  # 小时选择递归函数
  def hourLoop(self, browser, hour_time):
    try:
      target_hour = browser.find_element_by_xpath('//div[@class="semi-scrolllist-item-wheel undefined-list-hour"]/div[@class="semi-scrolllist-list-outer"]/ul/li[contains(text(),"' + str(hour_time) + '")]')
      target_hour.click()
      self.sleep(1)
    except:
      self.sleep(1)
      self.hourLoop(browser, hour_time + 3)

  # 分钟选择递归函数
  def minuteLoop(self, browser, minute_time):
    try:
      target_minute = browser.find_element_by_xpath('//div[@class="semi-scrolllist-item-wheel undefined-list-minute"]/div[@class="semi-scrolllist-list-outer"]/ul/li[contains(text(),"' + str(minute_time) + '")]')
      target_minute.click()
      self.sleep(1)
    except:
      self.sleep(1)
      self.minuteLoop(browser, minute_time + 3)

  # 元素是否存在判断函数
  def isElementExist(self, browser, element):
    flag=True
    try:
      browser.find_element_by_css_selector(element)
      return flag
    except:
      flag=False
      return flag

  # 文件遍历函数
  def file_name(self, file_dir):   
    L={'file_name': [], 'url_name': [], 'full_file_name': []}  
    for root, dirs, files in os.walk(file_dir):
      for file in files:  
        if os.path.splitext(file)[1] == '.mp4' or os.path.splitext(file)[1] == '.webm':  
          L['url_name'].append(os.path.join(root, file))
          L['file_name'].append(os.path.splitext(file)[0])           
          L['full_file_name'].append(os.path.splitext(file)[0] + os.path.splitext(file)[1])         
    return L

  # 新建文件夹函数
  def makeDir(self, path):
    # 去除首位空格
    path=path.strip()
    # 去除尾部 \ 符号
    path=path.rstrip("\\")
    # 判断路径是否存在
    isExists=os.path.exists(path)
    # 判断结果
    if not isExists:
      # 如果不存在则创建目录
      os.makedirs(path) 
      return True
    else:
      return True

if __name__=="__main__":
  app = QApplication(sys.argv)
  ex = Upload()
  ex.show()
  sys.exit(app.exec_())
