
from robot.data_mem import supabase_processor
from robot import detector
from robot.Conversation import Conversation
from robot.detector import Detector

class EVA(object):
    """_summary_
    EVA机器人的主类

    Args:
        object (_type_): _description_
    """
    def __init__(self):
        self.detector = None
        self.img_mem = supabase_processor()
        print(
            """
********************************************************
*          EVA - 基于树莓派的情感陪伴机器人          *
*          (c) 2025 王晨翼 <wcy0590@gmail.com>                     *
*     https://github.com/wing0night        *
********************************************************
""")
        print("初始化中...")
        self.detector = None
        # self.camera = 
        print("初始化完成！")
        self.conv = Conversation()  # 假设设备索引为0
        self.detector = Detector()
    def run(self):
        self.init()
        self.conv.init()
        try:
            # 初始化离线唤醒
            detector.initDetector(self.conv)
        except AttributeError:
            print("初始化离线唤醒功能失败")
            pass


if __name__ == '__main__':
    eva = EVA()
    eva.run()

