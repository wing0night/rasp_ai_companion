import pyaudio
import webrtcvad
import numpy as np
import time
import re
from openai import OpenAI
import os
from mem0 import MemoryClient
from mem0 import Memory
from dotenv import load_dotenv
from Camera import Camera
import speech_recognition as sr
import wave

# 加载.env文件
load_dotenv()

class Conversation:
    def __init__(self, device_index):
        self.vad = webrtcvad.Vad(2)  # 使用模式2，适用于语音聊天
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paInt16,
                                  channels=1,
                                  rate=16000,
                                  input=True,
                                  input_device_index=device_index,
                                  frames_per_buffer=320)  # 320ms的帧大小
        self.is_speaking = False
        self.recording = []
        self.recognizer = sr.Recognizer() # 语音识别器
        self.mem0_client = MemoryClient(api_key=os.environ.get('MEM0_API_KEY'))
        self.openrouter_client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.environ.get('OPENROUTER_API_KEY'),
        )
        # 初始化摄像头
        self.camera = Camera(device_id=0)

    def listen(self):
        while True:
            data = self.stream.read(320)  # 读取320ms的音频数据
            if self.vad.is_speech(data, 16000):
                if not self.is_speaking:
                    print("开始说话")
                    self.is_speaking = True
                self.recording.append(data)
            else:
                if self.is_speaking:
                    print("停止说话")
                    self.is_speaking = False
                    self.chat(b''.join(self.recording))
                    self.recording = []
                    time.sleep(1)  # 等待1秒以避免连续触发

    def chat(self, audio_data):
        self.save_recording_as_wav(audio_data)
        audio_file = sr.AudioFile('user_input.wav')
        with audio_file as source:
            audio = self.recognizer.record(source)
        # 使用语音识别器将音频转换为文本
        try:
            text = self.recognizer.recognize_google(audio)
            print(f"识别到的文本：{text}")
            if "关机" in text:
                print("正在关闭...")
                self.stream.stop_stream()
                self.stream.close()
                self.p.terminate()
                exit()
        except sr.UnknownValueError:
            print("无法识别音频")
        except sr.RequestError as e:
            print(f"请求错误：{e}")
        # 同时拍摄图片并上传
        chat_img_url = self.get_and_upload_img()
        prompt = self.create_prompt(text, "AGV_arm")
        # 调用Gemini处理对话
        # 使用mem0处理记忆层
        completion = self.openrouter_client.chat.completions.create(
        model="google/gemini-2.0-flash-thinking-exp:free",
        messages=[
            {
            "role": "user",
            "content": [
                {
                "type": "text",
                "text": prompt,
                },
                {
                "type": "image_url",
                "image_url": {
                    "url": chat_img_url,
                }
                }
            ]
            }
        ]
        )
        print(completion.choices[0].message.content)
        return completion.choices[0].message.content
    def save_recording_as_wav(self, audio_data):
        # 创建 WAV 文件
        wf = wave.open("user_input.wav", 'wb')
        # 设置 WAV 文件的参数
        wf.setnchannels(1)  # 单声道
        wf.setsampwidth(self.p.get_sample_size(pyaudio.paInt16))  # 采样宽度
        wf.setframerate(16000)  # 采样率
        # 写入音频数据
        wf.writeframes(audio_data)
        # 关闭 WAV 文件
        wf.close()
        print(f"Audio saved to user_input.wav")
    
    # 调用client_mem0生成提示词
    def create_prompt(self, user_input, user_id):
        # search for memories related to the user's input
        memories = self.mem0_client.search(user_input, user_id="AGV_arm")
        context = "\n".join([m["memory"] for m in memories])
        
        # make user's input part of the memory
        self.mem0_client.add(user_input, user_id="AGV_arm")
        prompt = f"""You are EVA. The user is your sincere friend, and you are a helpful assistant. You have an arm and can help the user with tasks. You can add some icon to more precisely express your emotion. Such as 😊, 😢, 😡, 😱, 😍, etc.
        Memories:
        {context}
        User's name is {user_id}
        User's input: {user_input}
        """
        
    # 每次调用chat，都会同时进行图片拍摄和上传
    def get_and_upload_img(self):
        img_path = "image.png"
        print("Capturing image")
        self.camera.CaptureImg(img_path)
        print("Image captured")
        from data_mem import supabase_processor
        img_url = supabase_processor().upload_img()
        print("Image uploaded")
        return img_url
        

# 获取USB声卡的设备索引
def get_usb_device_index():
    p = pyaudio.PyAudio()
    info = p.get_host_api_info_by_index(0)
    numdevices = info.get('deviceCount')
    for i in range(0, numdevices):
        if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
            print("Input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0, i).get('name'))
            if "USB" in p.get_device_info_by_host_api_device_index(0, i).get('name'):
                return i
    print("没有找到USB声卡设备")
    return None

if __name__ == "__main__":
    device_index = get_usb_device_index()
    if device_index is None:
        exit()
    conv = Conversation(device_index)
    conv.listen()





