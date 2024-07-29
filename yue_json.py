import os
import re

def find_parameters_in_string(json_content, file_name):
    # 使用正则表达式匹配 "parameters" 的值
    pattern = r'"parameters"\s*:\s*\[(".*?")\]'
    matches = re.findall(pattern, json_content)
    
    # 添加文件名前缀
    prefixed_matches = [f"{file_name}: {match}" for match in matches]
    
    return prefixed_matches

def process_files_in_folder(folder_path):
    all_parameters = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                parameters = find_parameters_in_string(content, filename)
                all_parameters.extend(parameters)
    
    return all_parameters

def write_to_file(output_file, parameters):
    with open(output_file, 'w', encoding='utf-8') as file:
        for param in parameters:
            file.write(param + '\n')

if __name__ == '__main__':
    folder_path = 'data'
    output_file = 'output.txt'
    
    all_parameters = process_files_in_folder(folder_path)
    write_to_file(output_file, all_parameters)