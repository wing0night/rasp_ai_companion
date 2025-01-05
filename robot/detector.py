import time

from snowboy import snowboydecoder
from robot import config
from Conversation import Conversation

class Detector:
    def __init__(self):
        self.detector = snowboydecoder.HotwordDetector("static/zhimakaimen.pmdl", sensitivity=0.5)
        self.interrupted = False
        print("使用 snowboy 进行离线唤醒")

    def signal_handler(self, signal, frame):
        self.interrupted = True

    def interrupt_callback(self):
        return self.interrupted

    def detected_callback(self):
        print("唤醒词检测到，启动对话监听")
        conv = Conversation(device_index=0)  # 假设设备索引为0
        conv.listen()

    def initDetector(self, conv):
        # 设置唤醒词检测的回调函数
        self.detector.start(detected_callback=self.detected_callback,
                            interrupt_check=self.interrupt_callback,
                            sleep_time=0.03)










