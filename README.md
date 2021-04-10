# 研招网调剂余额工具  
## 1、功能  
查询研招网特定专业的调剂余额信息，抽取其中一小时内发布的信息，并使用163邮箱的SMTP服务实现邮件推送  
--使用QQ邮箱接收可以在微信中查看邮件  
--在win或linux上部署每小时执行的定时任务，不错过任何一条该专业的调剂信息  
--全日制名额和非全日制名额分开显示  

## 2、部署

### 操作系统
win或linux

### python
python 3.x， 需要3.7及以下（3.8中smtplib.SMTP_SSL无法使用）  
推荐使用anaconda：https://mirrors.tuna.tsinghua.edu.cn/anaconda/archive/  
第三方库：  
--beautifulsoup4（解析网页中表格）
--selenium（控制浏览器）

### chrome和driver
chrome：https://www.google.cn/chrome/  
driver：http://npm.taobao.org/mirrors/chromedriver/  
注意chrome和driver版本需要匹配

### 修改个人参数


