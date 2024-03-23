score1 = int(input("请输入成绩1："))
for i in range(999):
        if score1 > 100:
            score1 = int(input("请输入正确成绩1："))
        else:
            score2 = int(input("请输入成绩2："))
            for ii in range(999):
                if score2 > 100:
                    score2 = int(input("请输入正确成绩2："))
                else:
                    if score1 > 60 or score2 > 60:
                        print("好！")
                        break
                    else:
                        if score1 < 60 and score2 < 60:
                            print("不好！")
                            break
