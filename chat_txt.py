def process_file(input_filename, output_filename):
    # 用于存储处理后的行
    processed_lines = []

    # 打开并读取输入文件
    with open(input_filename, 'r', encoding='utf-8') as file:
        for line in file:
            # 移除行中的所有空格
            line = line.replace(' ', '')

            # 寻找第一个 ':' 和最后一个 '['
            first_colon = line.find(':')
            last_bracket = line.rfind('[')

            # 如果在这行中找到了 ':' 和 '['
            if first_colon != -1 and last_bracket != -1:
                # 删除 ':' 和 '[' 之间的内容，但保留 ':'
                line = line[:first_colon+1] + line[last_bracket:]

            # 添加处理后的行到列表
            processed_lines.append(line)

    # 将处理后的行写入输出文件
    with open(output_filename, 'w', encoding='utf-8') as file:
        for line in processed_lines:
            file.write(line)

# 使用示例
input_filename = 'output.txt'  # 输入文件名
output_filename = 'output2.txt'  # 输出文件名

process_file(input_filename, output_filename)


filename = 'output2.txt'  # 假设这是你的文件名
chars_to_remove = ['[']  # 指定要删除的字符
output_filename = 'output3.txt'  # 输出文件名
with open(filename, 'r', encoding='utf-8') as file:
    content = file.read()
    
    # 删除指定的字符
for char in chars_to_remove:
    content = content.replace(char, '')
    
    # 写入新文件或覆盖原文件
if output_filename is None:
    output_filename = filename  # 覆盖原文件
with open(output_filename, 'w', encoding='utf-8') as file:
    file.write(content)

# 使用示例
