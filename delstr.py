import os
import shutil

def rename_files(directory):
    # 遍历指定目录下的所有文件
    for filename in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, filename)):
            # 分离文件名和扩展名
            base_name, extension = os.path.splitext(filename)
            
            # 找到第一个下划线的位置
            underscore_pos = base_name.find('_')
            if underscore_pos != -1:
                # 构建新的文件名（仅保留基名部分）
                new_base_name = base_name[:underscore_pos]
                new_filename = new_base_name + extension
                
                # 获取完整的源文件路径和目标文件路径
                src_file_path = os.path.join(directory, filename)
                dst_file_path = os.path.join(directory, new_filename)
                
                # 重命名文件
                try:
                    shutil.move(src_file_path, dst_file_path)
                    print(f"Renamed '{filename}' to '{new_filename}'")
                except Exception as e:
                    print(f"Error renaming '{filename}': {e}")

# 指定你要处理的目录
target_directory = '一次转换'
rename_files(target_directory)