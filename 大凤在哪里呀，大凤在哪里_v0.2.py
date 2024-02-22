print('大青花鱼找不到她的好朋友大凤了，她只剩10发鱼雷了，你能帮帮大青花鱼么？')
print('游戏规则：','\n',' 你有10发鱼雷，你能在鱼雷发射完之前帮大青花鱼找到大凤么？','\n',' 每次只能发射一颗鱼雷，每颗鱼雷能打击一个目标区域','\n',' 如果命中大凤就算成功')

#判断游戏启动
idiot = 'n'
while idiot != 'y':
    print('你理解规则了吗？')
    idiot = input('理解了：y   完全不懂：n''\n')
    idiot = idiot.lower()
    if idiot == 'n':
        print('这么简单的规则怎么理解不了啊？杂鱼杂鱼！')
    elif idiot != 'y':
        print('不要整活，请输入y或者n')

#选择难度

#定义游戏内部函数
#显示海域函数
def show_area():
    print(''.join(ocean[0]),'\n',''.join(ocean[1]),'\n',''.join(ocean[2]),'\n',''.join(ocean[3]),'\n',''.join(ocean[4]),'\n',''.join(ocean[5]),'\n')
#鱼雷攻击目标点函数
def judge_point(torpedo):
    if len(torpedo) == 2 and torpedo[0] in ['A','B','C','D','E'] and torpedo[1] in ['1','2','3','4','5']:
        return True
    else:
        return False
#随机生成雪风
def yuki():
    yukikaze = []
    for i in range(1,6):
        for j in range(1,6):
            if ocean[i][j] == ' ≈≈≈≈ ':
                yukikaze.append([i,j])
    yukikaze_pos = random.randint(1, len(yukikaze))
    ocean[yukikaze[yukikaze_pos][0]][yukikaze[yukikaze_pos][1]] = ' 雪风 '

#游戏初始化
#初始弹药10
ammo = 10
#随机生成大凤
import random
dict_col = {1:'A',2:'B',3:'C',4:'D',5:'E'}
dict_lin = {'A':1,'B':2,'C':3,'D':4,'E':5}
Taiho_col = random.randint(1, 5)
Taiho_lin = random.randint(1, 5)
Taiho = [Taiho_col,Taiho_lin]
Taiho_pos = [dict_col[Taiho_col],str(Taiho_lin)]

#随机生成其他舰船
#Rule:'为了防止碰撞，重樱的舰船之间至少会保留一格的空间，也就是舰船周围的8个格子里不会有其他舰船'

#为舰船赋予体积

#显示舰船受伤/击沉

#特殊道具
#随机生成特殊道具

#使用特殊道具

#核弹'爆炸范围3*3'

#雷达扫描'范围4*4（进阶：但是有几率导致被扫到的舰船开始逃离）'

#空袭支援'对某一行/列进行攻击'

#生成5X5海域
colomn = ['      ','   A  ','   B  ','   C  ','   D  ','   E  ']
Line = ['      ','   1  ','   2  ','   3  ','   4  ','   5  ']
ocean = []
for i in range(6):
    temp = []
    for j in range(6):
        temp.append(' ≈≈≈≈ ')
    ocean.append(temp)
for i in range(0,6):
    ocean[0][i] = colomn[i]
for i in range(1,6):
    ocean[i][0] = Line[i]

show_area()
print(Taiho_pos)
hump = 0
hit = False
attacked = []
while ammo > 0:
    if hump == 5:
        print('哼！就知道捣乱，大青花鱼不跟你玩了啦')
        break
    torpedo = input('请输入要发射鱼雷的坐标，比如：A3(可以输入小写字母)：')
    t = torpedo[0]
    torpedo = ''.join([t.upper(),torpedo[1]])
    print('\n')
    if not judge_point(torpedo):
        print('不要乱搞，请输入正确的坐标')
        hump = hump + 1
    elif torpedo in attacked:
        hump = hump + 1
        print('那个位置已经炸过，不对寻找过了哦，请选一个其他位置')
    else:
        ammo = ammo - 1
        torpedo_col = dict_lin[torpedo[0]]
        torpedo_lin = int(torpedo[1])
        attacked.append(torpedo)
        if torpedo == ''.join(Taiho_pos):  #命中
            ocean[Taiho_lin][Taiho_col] = ' 大凤 '
            hit = True
            print('恭喜你，你帮大青花鱼找到了大凤！')
            break
        else:    #miss
            ocean[torpedo_lin][torpedo_col] = '  XX  '
            show_area()
            print('不好意思，你没有帮大青花鱼找到大凤，再来一次吧','\n','剩余鱼雷',ammo,'发''')
        if abs(torpedo_col - Taiho_col) <= 1 and abs(torpedo_lin - Taiho_lin) <= 1:
            print('猎物接近的预感呢')
        if abs(torpedo_col - Taiho_col) == 2 or abs(torpedo_lin - Taiho_lin) == 2:
            print('怎么找也找不到呀')
        if abs(torpedo_col - Taiho_col) >= 3 or abs(torpedo_lin - Taiho_lin) >= 3:
            print('好像不在这附近呢')
yuki()
if hump == 5:
    print('也许你并不真正拥有理解游戏规则的智能')
elif hit == False:
    ocean[Taiho_lin][Taiho_col] = ' 大凤 '
    show_area()
    print('大凤藏在',''.join(Taiho_pos),'\n','你最终没有帮大青花鱼找到大凤，菜就多练')
else:
    show_area()
    print('谢谢你帮助大青花鱼找到了她的朋友大凤，现在她可以和她的朋友一起愉快的玩耍了')