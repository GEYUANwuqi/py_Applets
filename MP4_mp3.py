import ffmpeg

def extract_audio(input_file, output_file):
    # 使用 ffmpeg 提取音频
    stream = ffmpeg.input(input_file)
    audio = stream.audio
    ffmpeg.output(audio, output_file).run(overwrite_output=True)

    print(f"提取音频成功：{output_file}")
    input("按任意键退出...")

# 获取输入视频路径和音频名称
input_file = input("输入视频路径：")
wav_name = input("输入音频名称：") + ".wav"
input_file = input_file.replace("\\", "/")
input_file = input_file.replace('"', '')
last_slash_index = input_file.rfind("/")
result = input_file[:last_slash_index]
output_file = f"{result}/{wav_name}"

# 调用函数提取音频
extract_audio(input_file, output_file)
