# score1 = int(input("请输入成绩1："))
#
# while True:
#    if score1 > 100:
#        score1 = int(input("请输入正确成绩1："))
#    else:
#        score2 = int(input("请输入成绩2："))
#
#        while True:
#            if score2 > 100:
#                score2 = int(input("请输入正确成绩2："))
#            else:
#                if score1 > 60 or score2 > 60:
#                    print("好！")
#                    exit()  # 结束程序
#                else:
#                    if score1 < 60 and score2 < 60:
#                        print("不好！")
#                       exit()  # 结束程序
# 以上为gpt初版的代码

while True:
    try:
        score1 = int(input("请输入成绩1："))
        if score1 > 100 or score1 < 0:
            raise ValueError("请输入正确成绩1")

        while True:
            try:
                score2 = int(input("请输入成绩2："))
                if score2 > 100 or score2 < 0:
                    raise ValueError("请输入正确成绩2")

                if score1 >= 60 or score2 >= 60:
                    print("好！")
                    exit()
                else:
                    if score1 <= 60 and score2 <= 60:
                        print("不好！")
                        exit()
            except ValueError as ve2:
                print(ve2)
    except ValueError as ve1:
        print(ve1)
