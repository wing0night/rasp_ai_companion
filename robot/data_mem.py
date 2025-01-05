# 图片上传到supabese
import os
from supabase import create_client, Client
from dotenv import load_dotenv

# 加载.env文件
load_dotenv()

class supabase_processor(object):
    def __init__(self):
        self.url: str = os.environ.get("SUPABASE_URL")
        self.key: str = os.environ.get("ANON_KEY")
    def extract_max_num(files):
        # 提取文件名中的编号
        numbers = []
        for file in files:
            file_name = file["name"]
            if file_name.startswith("image") and file_name.endswith(".png"):
                try:
                    number = int(file_name[5:-4])  # 提取编号
                    numbers.append(number)
                except ValueError:
                    pass

        # 找到最大的编号
        max_number = max(numbers, default=0)
        return max_number
    def upload_img(self):
        supabase: Client = create_client(self.url, self.key)
        files = supabase.storage.from_(bucket_name).list()
        upload_index = self.extract_max_num(files)
        # 存储桶
        bucket_name: str = "images"
        # 要上传的图片文件路径
        file_path: str = "image.png"
        # 生成新的文件名
        new_file_name = f"image{upload_index + 1}.png"
        # 读取图片文件并上传
        with open(file_path, "rb") as file:
            response = supabase.storage.from_(bucket_name).upload(new_file_name, file)
        # 返回上传结果
        if response:
            print(f"Image uploaded successfully as {new_file_name}")
        else:
            print("Failed to upload image.")
        img_url = supabase.storage.from_(bucket_name).get_public_url(
        new_file_name
        )
        return img_url
        









