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

decimal_values_list = []
for decimal_values in output:
    decimal_values_list.extend(decimal_values)
decimal_values_str = ''.join(decimal_values_list)
print(decimal_values_str)

for binary_values in output:
    binary_values_str = "" + binary_values
print(binary_values_str)


