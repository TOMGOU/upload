from moviepy.editor import VideoFileClip

def timeConvert(size):# 单位换算
  M, H = 60, 60**2
  if size < M:
      return str(size)+u'秒'
  if size < H:
      return u'%s分钟%s秒'%(int(size/M),int(size%M))
  else:
      hour = int(size/H)
      mine = int(size%H/M)
      second = int(size%H%M)
      tim_srt = u'%s小时%s分钟%s秒'%(hour,mine,second)
      return tim_srt

videoPath = r"C:\demo\02_SUMMARY\29_automation\upload\1.mp4"

clip = VideoFileClip(videoPath)
print(clip.duration)
file_time = timeConvert(clip.duration)
print(file_time)