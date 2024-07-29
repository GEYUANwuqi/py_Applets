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
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")

def main():
    input_file = 'demo.wav'
    
    # 从音频文件中识别文本
    recognized_text = recognize_speech_from_audio(input_file)
    
    print(recognized_text)

    if recognized_text:
        # 添加识别的文本到文件名
        base_name, extension = os.path.splitext(os.path.basename(input_file))
        new_filename = f"{base_name}_{recognized_text}{extension}"
        os.rename(input_file, new_filename)

if __name__ == '__main__':
    main()