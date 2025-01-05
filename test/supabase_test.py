import os
from supabase import create_client, Client
from dotenv import load_dotenv

# 加载.env文件
load_dotenv()

# 初始化Supabase客户端
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("ANON_KEY")
supabase: Client = create_client(url, key)

# user = supabase.auth.sign_in_with_password({ "email": os.environ.get("SUPABASE_ACCOUNT_EMAIL"), "password": os.environ.get("SUPABASE_ACCOUNT_SECRET_KEY") })

bucket_name: str = "images"
# new_file = getUserFile()

# 要上传的图片文件路径
file_path: str = "image.png"

# 获取存储桶中所有文件
files = supabase.storage.from_(bucket_name).list()

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

# 生成新的文件名
new_file_name = f"image{max_number + 1}.png"

# 读取图片文件并上传
with open(file_path, "rb") as file:
    response = supabase.storage.from_(bucket_name).upload(new_file_name, file)

if response:
    print(f"Image uploaded successfully as {new_file_name}")
else:
    print("Failed to upload image.")

img_url = supabase.storage.from_("images").get_public_url(
  "image1.png"
)
print(img_url)



