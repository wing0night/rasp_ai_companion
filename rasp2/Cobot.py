from pymycobot import MyCobot280
import serial
import time
import ast

# mc = MyCobot280('/dev/ttyAMA0', 1000000)

class MyCobot:
    def __init__(self, port, baudrate):
        self.MC = MyCobot280(port, baudrate)
    
    # send_angles函数可以同时控制多个关节
    # angle度数列表（List[float]），长度 6
    # speed速度（int），范围 0~100
    def send_angles(self, angles, speed):
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

class serialProcessor:
    def __init__(self, port, baudrate):
        # 配置串口参数
        self.ser = serial.Serial(
            port=port,  # 树莓派串口设备文件路径
            baudrate=baudrate,        # 波特率设置为9600
            parity=serial.PARITY_NONE,  # 校验位设置为无校验
            stopbits=serial.STOPBITS_ONE,  # 停止位设置为1位
            bytesize=serial.EIGHTBITS,    # 数据位设置为8位
            timeout=1                     # 读取超时设置为1秒
        )
        self.MA = MyCobot('/dev/ttyAMA0', 1000000)
    def listen(self):
        # 读取串口数据并处理
        while True:
            try:
                # 读取串口数据
                data = self.ser.readline().decode('utf-8').strip()
                
                if self.return_float_list_format(data):
                    # 如果数据格式正确，解析数据并控制机械臂
                    angles = self.return_float_list_format(data)
                    self.MC.send_angles(angles, 50)
                elif data=="get_coords_angles":
                    # 如果数据为"get_coords_angles"，获取机械臂当前角度和坐标信息
                    result = self.MC.get_angles_coords()
                    self.send_data(result) # 发送数据到另一个树莓派
                    
            except serial.SerialException as e:
                # 处理串口异常
                print(f"Serial Exception: {e}")
                break
            
            except KeyboardInterrupt:
                # 处理键盘中断异常
                print("Program terminated by user")
                break
            
            # 稍作延时，避免CPU占用过高
            time.sleep(0.1)
    def return_float_list_format(data_str):
        try:
            # 尝试使用ast.literal_eval解析字符串
            result = ast.literal_eval(data_str)
            
            # 检查解析结果是否为列表类型
            if isinstance(result, list):
                # 检查列表长度是否为6
                if len(result) == 6:
                    # 检查列表中的每个元素是否为浮点数
                    if all(isinstance(item, (int, float)) for item in result):
                        return result # 返回解析结果
                    else:
                        return False
                else:
                    return False
            else:
                return False
        except (ValueError, SyntaxError):
            # 如果解析失败，返回False
            return False
    def send_data(self, data):
        # 发送数据到另一个树莓派
        self.ser.write(str(data).encode('utf-8'))

if __name__ == '__main__':
    sp = serialProcessor('/dev/ttyAMA0', 9600) # 树莓派串口设备文件路径, 波特率设置为9600
    sp.listen()







