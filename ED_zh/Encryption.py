def string_to_utf8_binary(input_string):
    # 遍历输入字符串中的每个字符
    for char in input_string:
        # 将字符编码为UTF-8格式的字节串
        utf8_bytes = char.encode('utf-8')
        
        # 将字节串转换为整数列表
        int_list = [byte for byte in utf8_bytes]
        
        # 将整数列表中的每个整数转换为二进制字符串
        binary_list = [bin(byte)[2:].zfill(8) for byte in int_list]
        
        # 输出每个字符的UTF-8编码的十进制值和二进制值
        for i, byte in enumerate(int_list):
            print(f"Character: {char}, UTF-8 Decimal: {byte}, UTF-8 Binary: {binary_list[i]}")

# 示例调用
string_to_utf8_binary("上联：长长长长长长长，下联：长长长长长长长，横批：长长长长")