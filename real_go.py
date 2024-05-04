import subprocess
import shutil
import os
import time
import ffmpeg
from PIL import Image
from fractions import Fraction

# 定义运行函数
def run_script_in_folder():
    folder_path = os.path.dirname(os.path.abspath(__file__))
    os.chdir(folder_path)
    files_in_folder = os.listdir()
    if __file__ in files_in_folder:
        subprocess.call(['python', __file__]) # 定义文件夹内运行函数

run_script_in_folder() # 指定当前文件夹运行

def resize_image(input_path, output_path, new_width, new_height):
    img = Image.open(input_path)
    resized_img = img.resize((new_width, new_height))
    resized_img.save(output_path) # 定义重采样图片函数

def get_video_resolution(video_path):
    probe = ffmpeg.probe(video_path)
    video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
    width = video_stream.get('width')
    height = video_stream.get('height')
    return width, height # 定义视频分辨率函数

def convert_frames_to_video(au_file, frames_dir, output_file, frame_rate):
    ffmpeg_cmd = [
        'ffmpeg', 
        '-r', str(frame_rate),
        '-i', frames_dir + '/frame_%04d.png',  
        '-i', au_file,  
        '-map', '0:v:0',
        '-map', '1:a:0',
        '-c:a', 'copy', 
        '-c:v', 'libx265', 
        '-b:v', '30M',
        '-r', str(frame_rate), 
        '-pix_fmt', 'yuv420p', 
        output_file]
    subprocess.run(ffmpeg_cmd) # 定义合并视频帧函数

def float_to_fraction(decimal):
    return Fraction(decimal).limit_denominator() # 定义分数函数

def extract_video_frames(input_video,output_file):
    ffmpeg.input(input_video).output(os.path.join(output_file, 'frame_%04d.png')).run() # 定义提取视频帧函数

def create_directory_if_not_exists(directory_path):
    if not os.path.isdir(directory_path):
        os.makedirs(directory_path) # 定义新建文件夹函数

def delete_files_in_folder(folder_path):
    file_names = os.listdir(folder_path)
    for file_name in file_names:
        file_path = os.path.join(folder_path, file_name)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
            else:
                print(f"警告: {file_path} 不是一个文件，无法删除。")
        except Exception as e:
            print(f"删除文件 {file_path} 时出错: {e}") # 定义删除视频帧文件函数

Image.MAX_IMAGE_PIXELS = 1000000000 # 定义重采样图片最大分辨率（如于修改报错可以适当提高此值,默认10亿分辨率

print("需要超分的文件请放在源码路径下\n已简化步骤,正常情况下疯狂回车即可\n")

bat_file_path = "go.bat"  # bat脚本文件
module_dict = {
    "animex4": "realesrgan-x4plus-anime",
    "videox4": "realesr-animevideov3-x4",
    "ganx4": "realesrgan-x4plus",
    "videox2": "realesr-animevideov3-x2"}  # 模型列表
modules = input("请选择模型(animex4/ganx4/videox4/videox2/默认为animex4): ").lower() or "animex4"
module = module_dict.get(modules, None)  # 选择模型

# 图片或视频的选择
if modules == "animex4" or modules == "ganx4" :
    pic_name = input("请输入文件名称(带后缀/默认为目录下的.png文件):") or [filename for filename in os.listdir() if filename.endswith('.png')][0]
    out_pic_name = f"{os.path.splitext(pic_name)[0]}_{modules}.png"  # 文件名选择
    width, height = Image.open(pic_name).size
    wofh = float_to_fraction(width/height)
    print(f"\n你选择的文件和模型为:{pic_name}/{module}","\n该图片分辨率为:{}x{}宽高比为{}\n请按照宽高比值设置超分的宽度以及高度↓↓↓".format(width, height,wofh)) # 分辨率输出
    new_width = input("请输入要超分到的宽度(默认x4): ") or width*4
    new_height = input("请输入要超分到的高度(默认x4): ") or height*4  # 超分选择
    with open(bat_file_path, "w") as f:
        variable = f"realesrgan-ncnn-vulkan.exe -i {pic_name} -o {out_pic_name} -n {module}"
        bat = variable
        f.write(f"{bat}") # 清空.bat文件的内容并写入新内容
else:
    video_name = input("请输入文件名称(带后缀/默认为目录下的.mp4文件):") or [filename for filename in os.listdir() if filename.endswith('.mp4')][0]
    out_video_name = f"{os.path.splitext(video_name)[0]}_{modules}.mp4"  # 文件名选择
    width, height = get_video_resolution(video_name)
    wofh = float_to_fraction(width/height)
    video_framerate = float(input("请输入视频帧率："))
    print(f"\n你选择的文件和模型为:{video_name}/{module}","\n该视频分辨率为:{}x{}宽高比为{}帧率为{}".format(width, height,wofh,video_framerate)) # 分辨率输出
    right=input("请确认并按回车继续运行...")
    tmp_video_frame_file = "video_frame"
    out_video_frame_file = "out_video_frame"
    create_directory_if_not_exists(tmp_video_frame_file)
    create_directory_if_not_exists(out_video_frame_file)
    with open(bat_file_path, "w") as f:
        variable = f"realesrgan-ncnn-vulkan.exe -i {tmp_video_frame_file} -o {out_video_frame_file} -n {module} -s 2 -f png"
        bat = variable
        f.write(f"{bat}") # 清空.bat文件的内容并写入新内容

# 运行更新后的.bat文件
print("\n正在运行超分脚本中,根据文件大小和数量及显卡性能此过程通常需要3-30s(可以使用任务管理器查看CPU或显卡运行情况)...")
start_time = time.perf_counter()
if modules == "animex4" or modules == "ganx4" :
    pass
else:
    extract_video_frames(video_name, tmp_video_frame_file)
process = subprocess.Popen([bat_file_path], shell=True, creationflags=subprocess.CREATE_NEW_CONSOLE)
while process.poll() is None:
    elapsed_time = round(float(time.perf_counter() - start_time),3)
    print(f"等待bat运行完毕中... ({elapsed_time}秒)", end="\r")
    time.sleep(0.01)
if modules == "animex4" or modules == "ganx4":
    pass
else:
    convert_frames_to_video(video_name,out_video_frame_file, out_video_name, video_framerate)

# 输出文件重采样/视频帧删除
if modules == "animex4" or modules == "ganx4":
    if new_width == width*4 and new_height == height*4:
        pass
    else:
        resize_image(out_pic_name, out_pic_name, int(new_width), int(new_height))
else:
    delete_files_in_folder(tmp_video_frame_file)
    delete_files_in_folder(out_video_frame_file)

elapsed_time = round(float(time.perf_counter() - start_time),3)
print(f"bat已运行完毕!本次消耗时间{elapsed_time}秒")

# 源目录至指定目录的定义
if modules == "animex4" or modules == "ganx4":
    y_file = out_pic_name
    x_file = pic_name
else:
    y_file = out_video_name
    x_file = video_name
current_dir = os.path.dirname(os.path.abspath(__file__))
target_folder = input("请输入存放文件的文件夹路径(默认为目录下的putout文件夹):") or os.path.join(current_dir, "putout")
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