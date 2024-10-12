import os
import subprocess

def convert_images_to_png(src_folder, dst_folder):
    # 确保目标文件夹存在
    if not os.path.exists(dst_folder):
        os.makedirs(dst_folder)

    # 支持的图片格式（包括 .raw 和 .nef）
    image_extensions = ('.jpg', '.jpeg', '.bmp', '.tiff', '.gif', '.png', '.raw', '.nef')

    # 遍历源文件夹中的所有文件
    for filename in os.listdir(src_folder):
        # 获取文件完整路径
        file_path = os.path.join(src_folder, filename)
        
        # 检查是否为文件以及是否是图片
        if os.path.isfile(file_path) and filename.lower().endswith(image_extensions):
            # 构建输出文件名和路径
            name, _ = os.path.splitext(filename)
            output_filename = f"{name}.png"
            output_file_path = os.path.join(dst_folder, output_filename)

            # 使用FFmpeg进行转换
            try:
                # 这里使用'-y'选项来覆盖已存在的文件
                subprocess.run(['ffmpeg', '-i', file_path, '-y', output_file_path], check=True)
                print(f"成功转换: {filename} -> {output_filename}")
            except subprocess.CalledProcessError as e:
                print(f"转换失败: {filename}, 错误: {e}")

# 定义源文件夹和目标文件夹
source_folder = 'E:/桌面/V圈/郑州市第29中学/2302/2024运动会'
destination_folder = 'E:/桌面/V圈/郑州市第29中学/2302/2024运动会/AAA.png直出'

# 调用函数
convert_images_to_png(source_folder, destination_folder)