import asyncio
import datetime
from bilibili_api import video

print("使用办法：\n输入视频的bv号,将自动输出符合规范的Temple Song模板\n正常运行会输出类似“D:/xxx/xxxxx/Temple_Song_of_moe”的代码,这是正常情况\n")

async def main() -> None:
    v = video.Video(bvid=input("请输入bv号:"))# 实例化 Video 类

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

    print(f"{left}{times}\n{bbid}{bv}\n{song}{title}\n{btime}{time}\n{bcount}{left}{bilicount}{bv}{right}\n{image}{pic}\n{right}\n")
    input("Ctrl+C复制后按enter退出！")

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
