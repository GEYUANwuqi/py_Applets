import subprocess
import shutil
import os
import re
import time
import json
import glob
from fractions import Fraction
import ffmpeg
from PIL import Image 
cwd = os.getcwd()
ffmpeg_path = os.path.join(cwd, "ffmpeg", "bin", "ffmpeg.exe")
ffprobe_path = os.path.join(cwd, "ffmpeg", "bin", "ffprobe.exe")

# 定义运行函数
def run_script_in_folder():
    folder_path = os.path.dirname(os.path.abspath(__file__))
    os.chdir(folder_path)
    files_in_folder = os.listdir()
    if __file__ in files_in_folder:
        subprocess.call(['python', __file__]) # 定义文件夹内运行函数

run_script_in_folder() # 指定当前文件夹运行

def config(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file) # 定义读取配置函数

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
    configs = config('config.json')
    ffmpeg_cmd = [
        'ffmpeg', 
        '-r', str(frame_rate),
        '-i', frames_dir + '/frame_%04d.png',  
        '-i', au_file,  
        '-map', '0:v:0',
        '-map', '1:a:0',
        '-c:a', configs['video']['ca'], 
        '-c:v', configs['video']['cv'], 
        '-b:v', configs['video']['bv'],
        '-r', str(frame_rate), 
        '-pix_fmt', 'yuv420p', 
        output_file]
    subprocess.run(ffmpeg_cmd) # 定义分离合并视频帧函数

def no_frame_to_video(frames_dir, audio_path, out_file, frame_rate):
    configs = config('config.json')
    ffmpeg_cmd = [
        'ffmpeg', 
        '-r', str(frame_rate),
        '-i', frames_dir + '/frame_%04d.png',  
        '-i', audio_path,  
        '-map', '0:v:0',
        '-map', '1:a:0',
        '-c:a', configs['video']['ca'], 
        '-c:v', configs['video']['cv'], 
        '-b:v', configs['video']['bv'],
        '-r', str(frame_rate), 
        '-pix_fmt', 'yuv420p', 
        out_file]
    subprocess.run(ffmpeg_cmd) # 定义合成视频帧及音频函数

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
                print(f"警告: {file_path} 不是一个文件,无法删除.")
        except Exception as e:
            print(f"删除文件 {file_path} 时出错: {e}") # 定义删除视频帧文件函数

def rename_files_to_digits(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith('.png'): 
            digits = re.findall(r'\d+', filename)
            if digits:
                new_filename = 'frame_' + ''.join(digits) + '.png'
                old_path = os.path.join(folder_path, filename)
                new_path = os.path.join(folder_path, new_filename)
                os.rename(old_path, new_path) # 定义帧文件命名函数

def go_bat(input,output,module_bat):
    with open(bat_file_path, "w") as f:
        variable = f"realesrgan-ncnn-vulkan.exe -i {input} -o {output} -n {module_bat}"
        bat = variable
        f.write(f"{bat}")  # 定义写入bat函数_pic

def go_bat_video(input,output,module_bat,multiples):
    with open(bat_file_path, "w") as f:
        variable = f"realesrgan-ncnn-vulkan.exe -i {input} -o {output} -n {module_bat} -s {multiples} -f png"
        bat = variable
        f.write(f"{bat}") # 定义写入bat函数_video

def run_bat(bat_file):
    process = subprocess.Popen([bat_file], shell=True, creationflags=subprocess.CREATE_NEW_CONSOLE)
    while process.poll() is None:
        elapsed_time = round(float(time.perf_counter() - start_time),3)
        print(f"等待bat运行完毕中... ({elapsed_time}秒)", end="\r")
        time.sleep(0.01) # 定义运行bat函数

configs = config('config.json')
Image.MAX_IMAGE_PIXELS = int(configs['image']['maxpix']) # 定义重采样图片最大分辨率(如遇修改时报错可以适当提高此值,默认6400万分辨率,即8000*8000的像素
video_name = "0" # 设定初始值

print(f"\nScript development by 伍昱yu物起(bili_uid:621240130)\nReal_ESRGAN(Repositories URL):https://github.com/xinntao/Real-ESRGAN")
print("\n简易使用指南:\n1.animex4模型对二次元图片的超分有优化,ganx4模型用于通用超分,videox2和videox4专用于视频超分\n2.在输入文件名称时,如果为默认的.png/.mp4可以直接回车跳过\n3.对于图片的超分这边提供了分辨率选项,但不建议将分辨率填写为原来图片的4倍以上,有4倍以上需求的可以进行二次超分\n4.在输入视频名称时输入“no”可以对video_frame文件夹内已有的原始帧进行超分并合成视频,这是对于有渲染帧超分需求(如mmd的制作)的特殊优化\n5.源码本身除去非正常使用外没有问题,如遇闪退报错请使用调试模式查看具体错误并Google解决\n6.“使用说明.txt”文件中有详细使用说明,请仔细阅读\n")

bat_file_path = "go.bat"  # bat脚本文件
module_dict = {
    "animex4": "realesrgan-x4plus-anime",
    "videox4": "realesr-animevideov3-x4",
    "ganx4": "realesrgan-x4plus",
    "videox2": "realesr-animevideov3-x2"}  # 模型列表
modules = input("请选择模型(animex4/ganx4/videox4/videox2/默认为animex4): ").lower() or "animex4"
module = module_dict.get(modules, None)  # 选择模型
if modules == "videox2" :
    multiple = 2
elif modules == "videox4":
    multiple = 4 # 视频帧超分方式选择

# 图片或视频的选择
if modules == "animex4" or modules == "ganx4" :
    pic_name = glob.glob(f"{input("请输入文件的名称: ")}.*")[0]
    out_pic_name = f"{os.path.splitext(pic_name)[0]}_{modules}.png"  # 文件名选择
    width, height = Image.open(pic_name).size
    wofh = float_to_fraction(width/height)
    print(f"\n你选择的文件和模型为:{pic_name}/{module}","\n该图片分辨率为:{}x{}宽高比为{}\n请按照宽高比值设置超分的宽度以及高度↓↓↓".format(width, height,wofh)) # 分辨率输出
    new_width = input("请输入要超分到的宽度(回车默认x4): ") or width*4
    new_height = input("请输入要超分到的高度(回车默认x4): ") or height*4  # 超分选择
    go_bat(pic_name,out_pic_name,module)
else:
    tmp_video_frame_file = "video_frame"
    out_video_frame_file = "out_video_frame"
    create_directory_if_not_exists(tmp_video_frame_file)
    create_directory_if_not_exists(out_video_frame_file)
    video_name = glob.glob(f"{input("请输入文件名称(如果已有视频帧和音频,请将视频帧以类似0001.png的方式命名并放到video_frame文件夹,音频放在源码路径下,之后输入no):")}.*")[0]
    if video_name == "no":
        rename_files_to_digits(tmp_video_frame_file)
        out_video_name=str(input("请输入要合成出的视频文件名:") + ".mp4")
        no_video_frame=float(input("请输入要合成出的视频的帧率:"))
        no_video_au=str(glob.glob(f"{input("请输入要合成的视频中所用的音频文件名(带后缀):")}.*")[0])
        input(f"将要把{tmp_video_frame_file}中的帧合成为视频,使用模型为{modules},合成视频文件名为{out_video_name},帧率为{no_video_frame},合并入音频为{no_video_au}\n注意!视频合成后会删除{tmp_video_frame_file}中全部的视频原始帧,如有需要请自行保存(确认后按回车继续运行)")
    else:
        out_video_name = f"{os.path.splitext(video_name)[0]}_{modules}.mp4"  # 文件名选择
        width, height = get_video_resolution(video_name)
        wofh = float_to_fraction(width/height)
        video_framerate = float(input("请输入视频帧率:"))
        print(f"\n你选择的文件和模型为:{video_name}/{module}","\n该视频分辨率为:{}x{}宽高比为{}帧率为{}".format(width, height,wofh,video_framerate)) # 分辨率输出
        right=input("请确认并按回车继续运行...")
    go_bat_video(tmp_video_frame_file,out_video_frame_file,module,multiple)

# 运行更新后的.bat文件
print("\n正在运行超分脚本中,根据文件大小和数量及显卡性能,照片通常需要3-30s,视频需30s-40min(可以使用任务管理器查看CPU或显卡运行情况)...")
start_time = time.perf_counter()
if modules == "animex4" or modules == "ganx4" :
    run_bat(bat_file_path)
else:
    if video_name == "no":
        run_bat(bat_file_path)
        no_frame_to_video(out_video_frame_file, no_video_au, out_video_name, no_video_frame) # 合成视频帧_no
    else:
        extract_video_frames(video_name, tmp_video_frame_file) # 切帧
        run_bat(bat_file_path)
        convert_frames_to_video(video_name,out_video_frame_file, out_video_name, video_framerate) # 合成视频帧

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
target_folder = input("请输入存放输出文件的文件夹路径(回车默认为目录下的putout文件夹):") or os.path.join(current_dir, "putout")
if not os.path.exists(target_folder):
    os.makedirs(target_folder)

# 移动文件到目标文件夹
try:
    if video_name == "no":
        shutil.move(y_file, target_folder)
    else:
        shutil.move(y_file, target_folder)
        shutil.move(x_file, target_folder)
except shutil.Error as e:
    print(e)
    print("存在文件重名,部分文件移动失败,请查看源码路径中的重复文件")

input("一键程序运行完毕,请查看文件夹内的文件(任意键退出)...")
