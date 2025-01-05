# 对机器人的各个状态做定制

from plugin.LED import LED



class LifeCircle(object):
    """_summary_
    机器人的生命周期控制类

    Args:
        object (_type_): _description_
    """
    def __init__(self, conversation):
        self.LED = LED()
        
    def on_init(self):
        # 初始化行为
        self.LED.blue_light()
    
    






