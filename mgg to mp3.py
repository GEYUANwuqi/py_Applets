from pydub import AudioSegment  # 导入 AudioSegment 模块
import os  # 导入 os 模块

# 定义函数：将 mp3 文件转换为 ogg 格式
def convert_to_ogg(mgg_file, ogg_file):
    sound = AudioSegment.from_mgg(mgg_file)  # 使用 pydub 从 mp3 文件创建音频段对象
    sound.export(ogg_file, format="ogg")  # 将音频段对象导出为 ogg 格式

# 定义函数：将 ogg 文件转换为 mp3 格式
def convert_to_mp3(ogg_file, mp3_file):
    sound = AudioSegment.from_ogg(ogg_file)  # 使用 pydub 从 ogg 文件创建音频段对象
    sound.export(mp3_file, format="mp3")  # 将音频段对象导出为 mp3 格式

# 定义主函数
def main(input_folder, output_folder):
    # 如果输出文件夹不存在，则创建它
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # 遍历输入文件夹中的文件
    for filename in os.listdir(input_folder):
        if filename.endswith(".mgg"):  # 如果文件以 .mp3 结尾
            # 将 mp3 转换为 ogg
            mgg_file = os.path.join(input_folder, filename)  # 构建 mp3 文件的完整路径
            ogg_file = os.path.join(output_folder, filename.replace(".mgg", ".ogg"))  # 构建 ogg 文件的完整路径
            convert_to_ogg(mp3_file, ogg_file)  # 调用转换函数

        elif filename.endswith(".ogg"):  # 如果文件以 .ogg 结尾
            # 将 ogg 转换为 mp3
            ogg_file = os.path.join(input_folder, filename)  # 构建 ogg 文件的完整路径
            mp3_file = os.path.join(output_folder, filename.replace(".ogg", ".mp3"))  # 构建 mp3 文件的完整路径
            convert_to_mp3(ogg_file, mp3_file)  # 调用转换函数

if __name__ == "__main__":  # 如果脚本直接被执行
    input_folder = r"D:\yuan\Music"
    output_folder = r"D:\yuan\Music\VipSongsDownload\output"
    main(input_folder, output_folder)  # 调用主函数进行转换
