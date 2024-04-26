import os
import soundfile as sf
import pyloudnorm as pyln

def normalize_mp3_files(directory_path, target_loudness=-5.0):
    # 遍历目录下的所有文件
    for filename in os.listdir(directory_path):
        # 检查文件是否为.mp3格式，并且不以 "normalized_" 开头
        if filename.endswith(".mp3") and not filename.startswith("normalized_"):
            # 构建文件路径
            file_path = os.path.join(directory_path, filename)
            print("处理文件:", file_path)
            
            # 加载音频数据
            data, rate = sf.read(file_path)
            
            # 测量音频的整体响度
            meter = pyln.Meter(rate)
            loudness = meter.integrated_loudness(data)
            
            # 根据目标响度标准化音频
            normalized_audio = pyln.normalize.loudness(data, loudness, target_loudness)
            
            # 保存标准化后的音频
            output_path = os.path.join(directory_path, "normalized_" + filename)
            sf.write(output_path, normalized_audio, rate, format='mp3')
            print("已保存标准化文件:", output_path)

# 指定目录路径
directory_path = "D:\yuan\Desktop\py项目\MP3"

# 标准化目录下所有不以 "normalized_" 开头的.mp3文件的响度为-5dB
normalize_mp3_files(directory_path, target_loudness=-5.0)
