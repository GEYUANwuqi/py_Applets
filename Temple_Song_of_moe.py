from pip._internal import main
import asyncio
import datetime

print(f"使用办法：\n输入视频的bv号,将自动输出符合规范的Temple Song模板\n正常打开文件并检查更新完成后会输出类似“D:/xxx/xxxxx/文件名”的代码,这是正常情况\n该工具最新的更新地址在“https://zh.moegirl.org.cn/User:%E4%BC%8D%E6%98%B1%E7%89%A9%E8%B5%B7/tsbpy”\n")
print(f"自动检查更新中...\n(此过程大概需要10-20s)\n")
main(['install', 'bilibili_api'])
print(f"\n检查已完成\n若出现导致程序非正常运行的错误请检查错误信息\n(此工具大部分的错误信息都不影响程序正常运行)\n")
from bilibili_api import video

async def main() -> None:
    v = video.Video(bvid=input("\n请输入bv号:"))# 实例化 Video 类

    info = await v.get_info()# 获取信息
    timestamp = info['pubdate']  # 时间戳
    date_object = datetime.datetime.fromtimestamp(timestamp)  # 时间戳转换为日期时间对象
    time = date_object.strftime("%y/%m/%d")  # 时间格式化
    if len(time) >= 4 and time[3] == '0':
        time = time[:3] + time[4:]
    bv=info['bvid']#bv号
    pic=info['pic']#封面
    title=info['title']#标题
    left="{{"
    right="}}"

    times="Temple Song|color=transparent"
    bbid="|bb_id="
    song="|曲目 ="
    btime="|投稿日期 ="
    bcount= "|再生数量 ="
    bilicount="BilibiliCount|id="
    image="|image link ="
    #模板

    print(f"\n{left}{times}\n{bbid}{bv}\n{song}{title}\n{btime}{time}\n{bcount}{left}{bilicount}{bv}{right}\n{image}{pic}\n{right}\n")
    input("Ctrl+C复制后按enter退出...")

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
