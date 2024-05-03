import subprocess
import shutil
import os
import time
from PIL import Image
from fractions import Fraction

print("请定位到源码路径并使用cmd/IDLE等编辑器运行\n需要超分的文件请放在源码路径下\n已简化步骤,正常情况下疯狂回车即可\n视频超分请自行测试\n")

# 定义运行函数
def resize_image(input_path, output_path, new_width, new_height):
    img = Image.open(input_path)
    resized_img = img.resize((new_width, new_height))
    resized_img.save(output_path) # 定义分数函数

def float_to_fraction(decimal):
    return Fraction(decimal).limit_denominator() # 定义修改图片分辨率

Image.MAX_IMAGE_PIXELS = 1000000000 # 定义修改图片最大分辨率（如于修改报错可以适当提高此值

bat_file_path = "go.bat"  # bat脚本文件
module_dict = {
    "animex4": "realesrgan-x4plus-anime",
    "videox4": "realesr-animevideov3-x4",
    "ganx4": "realesrgan-x4plus",
    "videox2": "realesr-animevideov3-x2"}  # 模型列表
modules = input("请选择模型(animex4/ganx4/videox4/videox2/默认为animex4): ").lower() or "animex4"
module = module_dict.get(modules, None)  # 选择模型
pic_name = input("请输入文件名称(带后缀/默认为目录下的.png文件):") or [filename for filename in os.listdir() if filename.endswith('.png')][0]
out_pic_name = f"{os.path.splitext(pic_name)[0]}_{modules}.png"  # 文件名选择
width, height = Image.open(pic_name).size
wofh = float_to_fraction(width/height)
print(f"\n你选择的文件和模型为:{pic_name}/{module}","\n该图片分辨率为：{}x{}宽高比为{}\n请按照宽高比值设置超分的宽度以及高度↓↓↓".format(width, height,wofh)) # 分辨率输出
new_width = input("请输入要超分到的宽度(默认x4): ") or width*4
new_height = input("请输入要超分到的高度(默认x4): ") or height*4  # 超分选择

# 清空.bat文件的内容并写入新内容
with open(bat_file_path, "w") as f:
    variable = f"realesrgan-ncnn-vulkan.exe -i {pic_name} -o {out_pic_name} -n {module}"
    bat = variable
    f.write(f"{bat}")

# 运行更新后的.bat文件
print("\n正在运行超分脚本中,根据文件大小和显卡此过程通常需要3-30s(可以使用任务管理器查看显卡运行情况)...")
start_time = time.perf_counter()
process = subprocess.Popen([bat_file_path], shell=True, creationflags=subprocess.CREATE_NEW_CONSOLE)
while process.poll() is None:
    elapsed_time = round(float(time.perf_counter() - start_time),3)
    print(f"等待bat运行完毕中... ({elapsed_time}秒)", end="\r")
    time.sleep(0.01)
print(f"bat已运行完毕!本次消耗时间{elapsed_time}秒")

# 输出文件重采样
if new_width == width*4 and new_height == height*4:
    pass
else:
    resize_image(out_pic_name, out_pic_name, int(new_width), int(new_height))

# 源目录至指定目录的定义
y_file = out_pic_name
x_file = pic_name
current_dir = os.path.dirname(os.path.abspath(__file__))
target_folder = input("请输入存放照片的文件夹路径(默认为目录下的pic_out文件夹):") or os.path.join(current_dir, "pic_out")
if not os.path.exists(target_folder):
    os.makedirs(target_folder)

# 移动文件到目标文件夹
try:
    shutil.move(y_file, target_folder)
    shutil.move(x_file, target_folder)
except shutil.Error as e:
    print(e)
    print("存在文件重名,部分文件移动失败,请查看源码路径中的重复文件")

input("一键程序运行完毕,请查看文件夹内的文件(任意键退出)...")

