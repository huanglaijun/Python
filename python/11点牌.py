import random

# 生成牌
poke_number_list = [i for i in range(1, 14)]
poke_color_list = ["黑桃", "梅花", "红桃", "方块"]
poke_list = [[i, j] for i in poke_color_list for j in poke_number_list] + [['小王', 13], ['大王', 14]]
random.shuffle(poke_list)

# 确定参加的人
print(f"欢迎来到11点游戏".center(100, '-'))
while True:
    count = input("请输入要参加游戏的人数：")
    if not count.isdecimal():
        print("必须输入纯数字")
        continue
    user_count = int(count)
    if user_count < 1:
        print("参加人数必须大于0")
        continue
    break

# 牌和玩家均确定后开始定义程序核心算法
total_user_score = {}


def ca_score(user, poke):
    # 向玩家发牌
    random_index = random.randint(0, len(poke) - 1)
    card = poke.pop(random_index)
    print(f"用户{user}".center(50, '-'))
    print("手中的牌是{}".format(card))
    # 统计分数
    user_score = 0
    value = 0.5 if card[1] > 10 else card[1]
    user_score += value
    return user_score


for i in range(1, user_count + 1):
    score = ca_score(i, poke_list)

    # 询问玩家是否继续要牌
    while True:
        choice = input("是否还要牌，请输入Y/N").upper()
        if choice not in {"Y", "N"}:
            print("只能输入Y/N")
            continue
        if choice == "N":
            print("用户{}的最终点数为{}".format(i, score))
            break

        # 选择继续发牌的逻辑
        score = ca_score(i, poke_list)

        # 判断点数是否大于11
        if score > 11:
            print("点数大于11，您被踢出游戏")
            score = 0
            break
        else:
            print("用户{}的点数为{}".format(i, score))
            continue
    total_user_score[f"用户{i}"] = score

# 打印最终得分情况
print(f"用户最终得分情况为".center(100, '*'))
# 对最终结果进行排序，选出获胜者
order_list = sorted(total_user_score.items(), key=lambda x: x[1], reverse=True)
print(f"排序的结果是{order_list}")
winner = order_list[0]
print(f"最终赢家是".center(50, '-'))
print("获胜者为{}得分为{}".format(winner[0], winner[1]))
