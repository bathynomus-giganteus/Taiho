print('大青花鱼找不到她的好朋友大凤了，她只剩10发鱼雷了，你能帮帮大青花鱼么？')
print('游戏规则：','\n',' 你有10发鱼雷，你能在鱼雷发射完之前帮大青花鱼找到大凤么？','\n',' 每次只能发射一颗鱼雷，每颗鱼雷能打击一个目标区域','\n',' 如果命中大凤就算成功')


#判断游戏启动
idiot = 'n'
while idiot != 'y':
    print('你理解规则了吗？')
    idiot = input('理解了：y   完全不懂：n''\n')
    if idiot == 'n':
        print('这么简单的规则怎么理解不了啊？杂鱼杂鱼！')
    elif idiot != 'y':
        print('不要整活，请输入y或者n')
#定义游戏内部函数
#显示海域函数
def show_area():
    print('',''.join(colomn),'\n',''.join(Line1),'\n',''.join(Line2),'\n',''.join(Line3),'\n',''.join(Line4),'\n',''.join(Line5),'\n')
#鱼雷攻击目标点函数
def judge_point(torpedo):
    if len(torpedo) == 2 and torpedo[0] in ['A','B','C','D','E'] and torpedo[1] in ['1','2','3','4','5']:
        return True
    else:
        return False
#随机生成大凤
import random

col = ['A','B','C','D','E']
a = random.randint(1, 5)
b = random.randint(1, 5)
Taiho = [col[a-1],str(b)]


#游戏初始化
#初始弹药10
ammo = 10
#生成5X5海域
colomn = ['     ','   A  ','   B  ','   C  ','   D  ','   E  ']
Line1 = ['  1  ',' ≈≈≈≈ ',' ≈≈≈≈ ',' ≈≈≈≈ ',' ≈≈≈≈ ',' ≈≈≈≈ ']
Line2 = ['  2  ',' ≈≈≈≈ ',' ≈≈≈≈ ',' ≈≈≈≈ ',' ≈≈≈≈ ',' ≈≈≈≈ ']
Line3 = ['  3  ',' ≈≈≈≈ ',' ≈≈≈≈ ',' ≈≈≈≈ ',' ≈≈≈≈ ',' ≈≈≈≈ ']
Line4 = ['  4  ',' ≈≈≈≈ ',' ≈≈≈≈ ',' ≈≈≈≈ ',' ≈≈≈≈ ',' ≈≈≈≈ ']
Line5 = ['  5  ',' ≈≈≈≈ ',' ≈≈≈≈ ',' ≈≈≈≈ ',' ≈≈≈≈ ',' ≈≈≈≈ ']
dict_Line = {1:Line1,2:Line2,3:Line3,4:Line4,5:Line5}
dict_alpha = {'A':1,'B':2,'C':3,'D':4,'E':5}
show_area()
hump = 0
attacked = []
while ammo > 0:
    if hump == 5:
        print('哼！就知道捣乱，大青花鱼不跟你玩了啦')
        break
    torpedo = input('请输入要发射鱼雷的坐标，比如：A3：')
    print('\n')
    if not judge_point(torpedo):
        print('不要乱搞，请输入正确的坐标')
        hump = hump + 1
    elif torpedo in attacked:
        print('那个位置已经炸过，不对寻找过了哦，请选一个其他位置')
    else:
        ammo = ammo - 1
        attacked.append(torpedo)
        if torpedo == ''.join(Taiho):  #命中
            dict_Line[b][a] = ' 大凤 '
            show_area()
            print('恭喜你，你帮大青花鱼找到了大凤！')
            break
        else:    #miss
            dict_Line[int(torpedo[1])][dict_alpha[torpedo[0]]] = '  XX  '
            show_area()
            print('不好意思，你没有帮大青花鱼找到大凤，再来一次吧','\n','剩余鱼雷',ammo,'发''')
        if abs(dict_alpha[torpedo[0]] - b) == 1 and abs(int(torpedo[1])) - a == 1:
            print('猎物接近的预感呢')
        if abs(dict_alpha[torpedo[0]] - b) >= 3 and abs(int(torpedo[1])) - a >= 3:
            print('怎么找也找不到呀')
if hump == 5:
    print('也许你并不真正拥有理解游戏规则的智能')
elif ammo == 0:
    print('你最终没有帮大青花鱼找到大凤，菜就多练')
else:
    print('谢谢你帮助大青花鱼找到了她的朋友大凤，现在她可以和她的朋友一起愉快的玩耍了')