def merge_bytes(input_str):
    result = []
    for char in input_str:
        utf8_bytes = char.encode('utf-8')
        if len(utf8_bytes) < 4:
            utf8_bytes += b'\x00' * (4 - len(utf8_bytes))
        decimal_values = [byte for byte in utf8_bytes]
        binary_values = ['{:08b}'.format(byte) for byte in utf8_bytes]
        result.append((char, decimal_values, ''.join(binary_values)))
    return result

input_str = "Ω 豈 😀 BEL"
output = merge_bytes(input_str)
for char, decimal_values, binary_values in output:
    print(f"Character: {char}, Decimal: {decimal_values}, Binary: {binary_values}")
