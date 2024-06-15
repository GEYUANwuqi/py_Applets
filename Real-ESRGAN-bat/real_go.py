import subprocess
import shutil
import os
import re
import time
import json
import glob
from fractions import Fraction
import platform


if platform.system() == "Windows":
    system =  "Windows"
    realesrgan_file = "realesrgan-ncnn-vulkan.exe"
    print("\n检测到当前系统为Windows,正在检查运行环境...")
    try:
        import ffmpeg
        from ffmpeg import probe
        from PIL import Image
    except ImportError:
        print("警告!检测到ffmpeg-python或pillow未安装,一键包可能不完整,请重新安装！")
    try:
        subprocess.run(["ffmpeg", "-version"], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT, check=True)
    except subprocess.CalledProcessError as e:
        print(f"ffmpeg文件不完整,一键包可能不完整,请重新安装!")
    os.environ["PATH"] += os.pathsep + os.path.join(os.getcwd(), "ffmpeg", "bin") # 将ffmpeg添加到系统变量中
elif platform.system() == 'Linux':
    system =  "Linux"
    realesrgan_file = "./realesrgan-ncnn-vulkan-linux"
    print("检测到当前系统为Linux,正在检查运行环境")
    try:
        import ffmpeg
        from ffmpeg import probe
    except ImportError:
        print("ffmpeg-python 未安装或未更新,请运行'pip install ffmpeg-python'以继续运行程序")
        exit()
    try:
        from PIL import Image
    except ImportError:
        print("Pillow 未安装,请运行'pip install Pillow'以继续运行程序")
        exit()
    result = subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True)
    if result.returncode != 0:
        print("当前环境中没有ffmpeg,请运行'sudo apt install ffmpeg'以继续运行程序")
        exit()
print("运行环境检查完毕!") # 检查运行环境


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
configs = config('config.json')

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
    f_format = configs['f_format']['format']
    ffmpeg_cmd = [
        'ffmpeg', 
        '-r', str(frame_rate),
        '-i', frames_dir + '/frame_%04d.' + f_format,  
        '-i', au_file,  
        '-map', '0:v:0',
        '-map', '1:a:0',
        '-c:a', configs['video']['ca'], 
        '-c:v', configs['video']['cv'], 
        '-b:v', configs['video']['bv'],
        '-pix_fmt', 'yuv420p', 
        output_file]
    subprocess.run(ffmpeg_cmd) # 定义分离合并视频帧函数

def nv_frame_to_video(frames_dir, audio_path, out_file, frame_rate):
    f_format = configs['f_format']['format']
    video_args = [
        '-r', str(frame_rate), 
        '-i', frames_dir + '/frame_%04d.' + f_format,
        ]
    if audio_path.lower() == "no":
        audio_args = [
            '-c:v', configs['no_video']['cv'], 
            '-b:v', configs['no_video']['bv'], 
            '-pix_fmt', 'yuv420p',
            '-an',]
    else:
        audio_args = [
            '-i', audio_path, 
            '-map', '0:v:0',
            '-map', '1:a:0',
            '-c:a', configs['no_video']['ca'],
            '-c:v', configs['no_video']['cv'], 
            '-b:v', configs['no_video']['bv'], 
            '-pix_fmt', 'yuv420p',]
    ffmpeg_cmd = ['ffmpeg'] + video_args + audio_args + [out_file]
    subprocess.run(ffmpeg_cmd) # 定义合成视频帧及音频函数

def float_to_fraction(decimal):
    return Fraction(decimal).limit_denominator() # 定义分数函数

def extract_video_frames(input_video,output_file):
    f_format = configs['f_format']['format']
    ffmpeg.input(input_video).output(os.path.join(output_file, 'frame_%04d.' + f_format)).run() # 定义提取视频帧函数

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
            print(f"删除文件 {file_path} 时出错: {e}")  # 定义删除视频帧文件函数

def files_to_num(folder_path):
    f_format = configs['f_format']['no']['format']
    for filename in os.listdir(folder_path):
        if filename.endswith('.' + f_format): 
            digits = re.findall(r'\d+', filename)
            if digits:
                new_filename = 'frame_' + ''.join(digits) + '.' + f_format
                old_path = os.path.join(folder_path, filename)
                new_path = os.path.join(folder_path, new_filename)
                os.rename(old_path, new_path) # 定义帧文件命名函数

def go_bat(input,output,model_bat):
    with open(bat_file_path, "w") as f:
        gpu_id = configs['gpuid']['id']
        variable = f"{realesrgan_file} -i {input} -o {output} -n {model_bat} -g {gpu_id}"
        f.write(f"{variable}")  # 定义写入bat函数_pic

def go_bat_video(input,output,model_bat,multiples):
    f_format = configs['f_format']['format']
    with open(bat_file_path, "w") as f:
        variable = f"{realesrgan_file} -i {input} -o {output} -n {model_bat} -s {multiples} -f {f_format}"
        f.write(f"{variable}") # 定义写入bat函数_video

def run_bat(bat_file):
    if system == "Windows":
        process = subprocess.Popen([bat_file], shell=True, creationflags=subprocess.CREATE_NEW_CONSOLE)
        while process.poll() is None:
            elapsed_time = round(float(time.perf_counter() - start_time),3)
            print(f"等待bat运行完毕中... ({elapsed_time}秒)", end="\r")
            time.sleep(0.01) # 定义运行bat函数
    elif system == "Linux":
        process = subprocess.run([bat_file], check=True, shell=True)


gpuid = configs['gpuid']['id']
Image.MAX_IMAGE_PIXELS = int(configs['image']['maxpix']) # 定义重采样图片最大分辨率(如遇修改时报错可以适当提高此值,默认6400万分辨率,即8000*8000的像素
video_name = "0" # 设定初始值
if system == "Windows":
    bat_file_path = "go.bat"  # Windows脚本文件
elif system == "Linux":
    bat_file_path = "./go.sh" # linux脚本文件


print(f"\nScript development by 伍昱yu物起(bili_uid:621240130)\nReal_ESRGAN(Repositories URL):https://github.com/xinntao/Real-ESRGAN")
print(
    "\n简易使用指南:"
    "\n1.animex4模型对二次元图片的超分有优化,ganx4模型用于通用超分,带video的模型专用于视频超分"
    "\n2.在输入文件名称时,无需输入文件后缀"
    "\n3.对于图片的超分这边提供了分辨率选项,但不建议将分辨率填写为原来图片的4倍以上,有4倍以上需求的可以进行二次超分"
    "\n4.在输入视频名称时输入“no”可以对video_frame文件夹内已有的原始帧进行超分并合成视频,这是对于有渲染帧超分需求(如mmd的制作)的特殊优化"
    "\n5.源码本身除去非正常使用外没有问题,如遇闪退报错请使用调试模式查看具体错误并Google解决"
    "\n6.“脚本使用说明.txt”文件中有详细使用说明,请仔细阅读\n"
    )


model_dict = str(configs['models'])[1:-1].replace(",", "\n")
print(f"模型列表:\n{model_dict}") # 模型列表
model_file = list(dict(configs['models']).values())
def model_search():
    existence_list = []
    model_files = os.listdir('models')
    for name in model_file:
        matches = [f for f in model_files if os.path.splitext(f)[0] == name]
        exists = len(matches) > 0
        existence_list.append(exists)
    return existence_list
for name, exists in zip(model_file, model_search()):
    if not exists:
        print(f"json文件中名为{name}的模型不存在,请查看models文件夹") # 检索模型


models = input("请选择模型(回车默认为animex4): ").lower() or "animex4"
model = configs['models'][models]  # 选择模型
if models == "videox2" :
    multiple = 2
elif models == "videox4":
    multiple = 4 # 视频帧超分方式选择(如需添加x3模型则需要在此处动手脚,修改方式参考这几行代码即可)

# 图片或视频的选择
if models == "animex4" or models == "ganx4" :
    file_name = input("请输入文件的名称: ")
    pic_name = glob.glob(f"{file_name}.*")[0]
    out_pic_name = f"{os.path.splitext(pic_name)[0]}_{models}.png"  # 文件名选择
    width, height = Image.open(pic_name).size
    wofh = float_to_fraction(width/height)
    print(f"\n你选择的文件和模型为:{pic_name}/{model}","\n该图片分辨率为:{}x{}宽高比为{}\n使用的显卡型号为GPU {}\n请按照宽高比值设置超分的宽度以及高度↓↓↓".format(width, height,wofh,gpuid)) # 分辨率输出
    new_width = input("请输入要超分到的宽度(回车默认x4): ") or width*4
    new_height = input("请输入要超分到的高度(回车默认x4): ") or height*4  # 超分选择
    go_bat(pic_name,out_pic_name,model)
else:
    tmp_video_frame_file = "video_frame"
    out_video_frame_file = "out_video_frame"
    create_directory_if_not_exists(tmp_video_frame_file)
    create_directory_if_not_exists(out_video_frame_file)
    video_name = input("请输入文件名称(如果已有视频帧和音频,请将视频帧以类似0001.png的方式命名并放到video_frame文件夹,音频放在源码路径下,之后输入no):")
    if video_name == "no":
        files_to_num(tmp_video_frame_file)
        out_video_name=str(input("请输入要合成出的视频文件名:") + ".mkv")
        no_video_frame=float(input("请输入要合成出的视频的帧率:"))
        audio_input = input("请输入要合成的视频中所用的音频文件名(输入no则不进行音频合成): ")
        if audio_input.lower() != 'no':
            no_video_au = str(glob.glob(f"{audio_input}.*")[0])
        else:
            no_video_au = 'no' 
        input(f"\n将要把{tmp_video_frame_file}中的帧超分并合成为视频,使用模型为{models},使用的显卡型号为GPU {gpuid},合成视频文件名为{out_video_name},帧率为{no_video_frame},合并入音频为{no_video_au}"
                f"\n注意!视频合成后会删除{tmp_video_frame_file}中全部的视频原始帧,如有需要请自行保存(确认后按回车继续运行)")
    else:
        video_name = glob.glob(f"{video_name}.*")[0]
        out_video_name = f"{os.path.splitext(video_name)[0]}_{models}.mkv"  # 文件名选择
        width, height = get_video_resolution(video_name)
        wofh = float_to_fraction(width/height)
        video_framerate = float(input("请输入视频帧率:"))
        print(f"\n你选择的文件和模型为:{video_name}/{model}",f"使用的显卡型号为GPU {gpuid}","\n该视频分辨率为:{}x{}宽高比为{}帧率为{}".format(width, height,wofh,video_framerate)) # 分辨率输出
        input("请确认并按回车继续运行...")
    go_bat_video(tmp_video_frame_file,out_video_frame_file,model,multiple)

# 运行更新后的.bat文件
print("\n正在运行超分脚本中,根据文件大小和数量及显卡性能,照片通常需要3-30s,视频需30s-40min(可以使用任务管理器查看CPU或显卡运行情况)...")
start_time = time.perf_counter()
if models == "animex4" or models == "ganx4" :
    run_bat(bat_file_path)
else:
    if video_name == "no":
        run_bat(bat_file_path)
        nv_frame_to_video(out_video_frame_file, no_video_au, out_video_name, no_video_frame) # 合成视频帧_no
    else:
        extract_video_frames(video_name, tmp_video_frame_file) # 切帧
        run_bat(bat_file_path)
        convert_frames_to_video(video_name,out_video_frame_file, out_video_name, video_framerate) # 合成视频帧

# 输出文件重采样/视频帧删除
if models == "animex4" or models == "ganx4":
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
if models == "animex4" or models == "ganx4":
    putout_folder = out_pic_name
    input_folder = pic_name
else:
    putout_folder = out_video_name
    input_folder = video_name
current_dir = os.path.dirname(os.path.abspath(__file__))
target_folder = input("请输入存放输出文件的文件夹路径(回车默认为目录下的putout文件夹):") or os.path.join(current_dir, "putout")
if not os.path.exists(target_folder):
    os.makedirs(target_folder)

# 移动文件到目标文件夹
try:
    if video_name == "no":
        shutil.move(putout_folder, target_folder)
    else:
        shutil.move(putout_folder, target_folder)
        shutil.move(input_folder, target_folder)
except shutil.Error as e:
    print(e)
    print("存在文件重名,部分文件移动失败,请查看源码路径中的重复文件")

input("一键程序运行完毕,请查看文件夹内的文件(任意键退出)...")