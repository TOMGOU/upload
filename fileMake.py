import os
def mkdir(path):
  # 去除首位空格
  path=path.strip()
  # 去除尾部 \ 符号
  path=path.rstrip("\\")

  # 判断路径是否存在
  isExists=os.path.exists(path)

  # 判断结果
  if not isExists:
    # 如果不存在则创建目录
    # 创建目录操作函数
    os.makedirs(path) 
    return True
  else:
    return True
 
# 定义要创建的目录
# mkpath = r'C:\demo\02_SUMMARY\29_automation\upload\test\..\demo'
# mkdir(mkpath)

delepath = r'C:/demo/02_SUMMARY/29_automation/douyin-of-automation/finished2020年8月20日，10佳球 #篮球.mp4'
print(os.path.exists(delepath))
# if os.path.exists(delepath):
  # os.remove(delepath)