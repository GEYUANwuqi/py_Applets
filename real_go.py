import subprocess
import shutil
import os
import time

print("请定位到源码路径并使用cmd/IDLE等编辑器运行\n需要超分的文件请放在源码路径下\n已简化步骤,正常情况下疯狂回车即可\n")

# 定义运行函数
bat_file_path = "go.bat"  # bat脚本文件
module_dict = {
    "animex4": "realesrgan-x4plus-anime",
    "videox4": "realesr-animevideov3-x4",
    "ganx4": "realesrgan-x4plus",
    "videox2": "realesr-animevideov3-x2"}  # 模型列表
modules = input("请选择模型(animex4/ganx4/videox4/videox2/默认为animex4): ").lower() or "animex4"
module = module_dict.get(modules, None)  # 选择模型
png_files = [filename for filename in os.listdir() if filename.endswith('.png')][0]
pic_name = input("请输入文件名称(带后缀/默认为目录下的.png文件):") or f"{png_files}"
out_pic_name = f"{os.path.splitext(pic_name)[0]}_{modules}.png"  # 文件名选择

# 清空.bat文件的内容并写入新内容
with open(bat_file_path, "w") as f:
    variable = f"realesrgan-ncnn-vulkan.exe -i {pic_name} -o {out_pic_name} -n {module}"
    bat = variable
    # 写入.bat文件的新内容
    f.write(f"{bat}")

# 运行更新后的.bat文件
print("\n正在运行超分脚本中,根据文件大小和显卡此过程通常需要3-20s(可以使用任务管理器查看显卡运行情况)...")
start_time = time.perf_counter()
process = subprocess.Popen([bat_file_path], shell=True, creationflags=subprocess.CREATE_NEW_CONSOLE)
while process.poll() is None:
    elapsed_time = round(float(time.perf_counter() - start_time),3)
    print(f"等待bat运行完毕中... ({elapsed_time}秒)", end="\r")
    time.sleep(0.01)
print(f"bat已运行完毕!本次消耗时间{elapsed_time}秒")

# 源目录——级目录
y_file = out_pic_name
x_file = pic_name
current_dir = os.path.dirname(os.path.abspath(__file__))
target_folder = input("\n请输入存放照片的文件夹路径(默认为目录下的pic_out文件夹):") or os.path.join(current_dir, "pic_out")
if not os.path.exists(target_folder):
    os.makedirs(target_folder)

# 移动文件到目标文件夹
shutil.move(y_file, target_folder)
shutil.move(x_file, target_folder)

input("一键程序运行完毕,请查看文件夹内的文件(任意键退出)...")
