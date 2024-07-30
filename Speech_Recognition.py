import os
import speech_recognition as sr

def recognize_speech_from_audio(audio_file):
    # 创建一个语音识别对象
    recognizer = sr.Recognizer()
    
    with sr.AudioFile(audio_file) as source:
        # 读取音频文件
        audio_data = recognizer.record(source)
        # 尝试识别语音
        try:
            text = recognizer.recognize_google(audio_data, language='zh-CN')
            return text
        except sr.UnknownValueError:
            print(f"Google Speech Recognition could not understand audio: {audio_file}")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service for {audio_file}; {e}")

def rename_files_with_transcribed_text(directory):
    # 遍历指定目录下的所有文件
    for filename in os.listdir(directory):
        if filename.endswith('.wav'):
            file_path = os.path.join(directory, filename)
            if os.path.isfile(file_path):
                # 从音频文件中识别文本
                recognized_text = recognize_speech_from_audio(file_path)
                
                if recognized_text:
                    # 分离文件名和扩展名
                    base_name, extension = os.path.splitext(filename)
                    # 构建新的文件名
                    new_filename = f"{base_name}_{recognized_text}{extension}"
                    new_file_path = os.path.join(directory, new_filename)
                    
                    # 重命名文件
                    try:
                        os.rename(file_path, new_file_path)
                        print(f"Renamed '{filename}' to '{new_filename}'")
                    except Exception as e:
                        print(f"Error renaming '{filename}': {e}")

# 指定你要处理的目录
target_directory = 'au'
rename_files_with_transcribed_text(target_directory)