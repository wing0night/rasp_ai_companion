from pymycobot import MyAgv
import time

# MA = MyAgv('/dev/ttyS0', 115200)

# 定义MyAgv类
class MyAgv:
    def __init__(self, serial_port, baudrate):
        self.MA = MyAgv(serial_port, baudrate)
    # 将AGV移动封装起来
    def AGV_move(self, action, speed, time):
        if action == "Go ahead":
            # go_speed – (int) 1 ~ 127 is forward.The smaller the value, the smaller the speed
            # timeout - (int): default 5 s.
            self.MA.go_ahead(speed, time)
        elif action == "Retreat":
            self.MA.retreat(speed, time)
        elif action == "Pan left":
            # pan_left_speed – (int) 1 ~ 127.The smaller the value, the smaller the speed
            # timeout - (int): default 5 s.
            self.MA.pan_left(speed, time)
        elif action == "Pan right":
            # pan_left_speed – (int) 1 ~ 127.The smaller the value, the smaller the speed
            # timeout - (int): default 5 s.
            self.MA.pan_right(speed, time)





