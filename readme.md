## EVA情感陪伴机器人树莓派版

参考wukong智能音箱，搭建了一个运行在树莓派上的AI情感陪伴系统

但是对代码逻辑进行了简化。结构也不像wukong那样规范，相比之下多了很多硬编码的内容

实现的功能：snowboy唤醒；唤醒后接收音频流，使用VAD语音活动检测算法判断是否完成接收；完成音频接收后调用Camera的函数，进行拍摄，并将图片上传到supabase；用户input经过mem0拉取的记忆处理生成完整的prompt；使用Conversation类中的chat方法调用AI模型gemini-2.0-flash-thinking-exp:free处理文本和图片，并同时将user_input转化为文本上传到mem0管理记忆层；循环这个过程

## 代码结构

```
│  .env
│  .env.example
│  .gitignore
│  EVA.py
│  list.txt
│  readme.md
│  requirements.txt
│  VERSION
│  
├─plugin
│      LED.py
│      readme.md
│      
├─rasp2
│      Cobot.py
│      readme.md
│      
├─robot
│  │  AGV.py
│  │  Camera.py
│  │  Cobot.py
│  │  config.py
│  │  constant.py
│  │  Conversation.py
│  │  data_mem.py
│  │  detector.py
│  │  lifecircle.py
│  │  readme.md
│  │  utils.py
│  │  
│  ├─img_readme
│  │      image-1.png
│  │      image.png
│  │      
│  └─__pycache__
│          Camera.cpython-311.pyc
│          
├─snowboy
│  │  snowboydecoder.py
│  │  snowboydetect.py
│  │  __init__.py
│  │  
│  └─resources
│          common.res
│          ding.wav
│          dong.wav
│          
├─static
│      beep_hi.wav
│      beep_lo.wav
│      camera.wav
│      default.yml
│      off.wav
│      on.wav
│      zhimakaimen.pmdl
│      
└─test
    │  image.png
    │  supabase_test.py
    │  
    └─__pycache__
            supabase.cpython-311.pyc
```

可以在Conversation类中测试摄像头、录音设备、数据库传输、AI对话等功能。但是树莓派翻墙还没做好，AI对话和supabase传输还不能使用




