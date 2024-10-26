import random
from pypinyin import pinyin, Style
from pypinyin_dict.pinyin_data import kxhc1983
kxhc1983.load()

def convert_to_pinyin_with_tone(text):
    # 使用 pypinyin 库的 pinyin 方法，Style.TONE3 表示带数字的声调形式
    result = pinyin(text, style=Style.TONE3)
    # 将拼音列表中的拼音元素连接成一个字符串，并且在每个拼音之间加上空格
    pinyin_str = ' '.join([item[0] for item in result])
    return pinyin_str

def scramble_string(s, seed):
    """使用指定的种子打乱字符串"""
    # 将字符串转换为字符列表（以空格分隔）
    chars = s.split()
    
    # 使用种子初始化随机数生成器
    rng = random.Random(seed)
    
    # 创建一个列表来跟踪每个字符的新位置
    new_positions = list(range(len(chars)))
    
    # 打乱新位置列表
    rng.shuffle(new_positions)
    
    # 创建一个新的列表来保存打乱后的字符
    shuffled_chars = [''] * len(chars)
    
    # 将字符放到新的位置上
    for old_pos, new_pos in enumerate(new_positions):
        shuffled_chars[new_pos] = chars[old_pos]
    
    # 返回打乱后的字符串
    return ' '.join(shuffled_chars)

def unscramble_string(scrambled, seed):
    """使用相同的种子恢复原字符串"""
    # 将打乱的字符串转换为字符列表（以空格分隔）
    chars = scrambled.split()
    
    # 使用种子初始化随机数生成器
    rng = random.Random(seed)
    
    # 创建一个列表来跟踪每个字符的新位置
    new_positions = list(range(len(chars)))
    
    # 打乱新位置列表（这次是为了获得原始的位置）
    rng.shuffle(new_positions)
    
    # 创建一个新的列表来保存解密后的字符
    original_chars = [''] * len(chars)
    
    # 根据新位置列表将字符放回原处
    for new_pos, old_pos in enumerate(new_positions):
        original_chars[old_pos] = chars[new_pos]
    
    # 返回解密后的字符串
    return ' '.join(original_chars)

# 输入文本
text = "义务越剧牛鬼，难道不离谱嘛"
# 转换为拼音
original_string = convert_to_pinyin_with_tone(text)
print("Original Pinyin:", original_string)

# 指定的种子
seed_value = 114514

# 打乱字符串
scrambled = scramble_string(original_string, seed_value)
print("Scrambled:", scrambled)

# 通过相同的种子恢复原字符串
unscrambled = unscramble_string(scrambled, seed_value)
print("Unscrambled:", unscrambled)