from pymycobot import MyCobot280

# mc = MyCobot280('/dev/ttyAMA0', 1000000)

class MyCobot:
    def __init__(self, port, baudrate):
        self.MC = MyCobot280(port, baudrate)
    
    # send_angles函数可以同时控制多个关节
    # angle度数列表（List[float]），长度 6
    # speed速度（int），范围 0~100
    def move(self, angles, speed):
        # 共6自由度，index取值为1~6
        self.MC.send_angles(angles, speed)
    
    # coords：：坐标列表，值[x,y,z,rx,ry,rz]，长度6
    # speed (int)：1 ~ 100
    # mode：(int) 0 - 非线性，1 - 直线运动
    def send_coords(self, coords, speed):
        self.MC.send_coords(coords, speed)
    
    # 返回值： 一个长度为12的列表，前六位为角度信息，后六位为坐标信息。
    # 坐标列表[x,y,z,rx,ry,rz]
    def get_angles_coords(self):
        return self.MC.get_angles_coords()
    
    def pause(self):
        self.MC.pause()




