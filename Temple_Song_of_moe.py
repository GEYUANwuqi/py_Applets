import asyncio
import datetime
from bilibili_api import video

async def main(BVID) -> None:
    v = video.Video(bvid=BVID)# 实例化 Video 类

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
    bbid="|bb_id = "
    song="|曲目 = "
    btime="|投稿日期 = "
    bcount= "|再生数量 = "
    bilicount="BilibiliCount|id= "
    image="|image link = "
    #模板

    module = (f"\n{left}{times}\n{bbid}{bv}\n{song}{title}\n{btime}{time}\n{bcount}{left}{bilicount}{bv}{right}\n{image}{pic}\n{right}\n")
    if run == 'True' and BVID == 'BV1vb411Y7A6':
        if bv == 'BV1vb411Y7A6' and pic == 'http://i0.hdslb.com/bfs/archive/d58b6de2016cf0251315a4030eccbbb527301098.jpg' and title == '洛天依，原创《夜间出租车》' and time == '19/2/21':
            pass
        else:
            print(f"Warning:当前软件已经过时，请更新软件！")
            input("按enter退出...")
            exit()
    else:
        print(module)
        input("Ctrl+C复制后按enter退出...")

if __name__ == "__main__":
    run = 'True'
    print('检查软件是否可以使用中...')
    BV = 'BV1vb411Y7A6'
    asyncio.run(main(BV))
    print("检查完毕!欢迎使用")
    print(f"\n使用办法：\n输入视频的bv号,将自动输出符合规范的Temple Song模板\n")
    run = 'False'
    BV = input("请输入视频的bv号：")
    asyncio.run(main(BV))
    
