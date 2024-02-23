import random

#定义游戏内部函数

#横坐标字母数字互相转化
num_alp = {1:'A',2:'B',3:'C',4:'D',5:'E'}
alp_num = {'A':1,'B':2,'C':3,'D':4,'E':5}

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

#舰船生成函数
def generate_ship():
    if len(vocab_target_dict) <= 1:
        n = 1
    else:
        n = random.randint(1, len(vocab_target_dict))
    return vocab_target_dict[n-1]

#游戏启动
print('大青花鱼找不到她的好朋友大凤了，她只剩10发鱼雷了，你能帮帮大青花鱼么？')
print('游戏规则：')
print('  你有10发鱼雷，你能在鱼雷发射完之前帮大青花鱼找到大凤么？')
print('  每次只能发射一颗鱼雷，每颗鱼雷能打击一个目标区域')
print('  为了防止碰撞，重樱的大型舰船之间至少会保留一格的空间，也就是舰船周围的8个格子里不会有其他大型舰船')
print('  如果命中大凤就算成功')

#判断游戏初始化
idiot = 'n'
while idiot != 'y':
    print('你理解规则了吗？（输入update查看更新日志）')
    idiot = input('理解了：y   完全不懂：n''\n')
    idiot = idiot.lower()
    if idiot == 'n':
        print('这么简单的规则怎么理解不了啊？杂鱼杂鱼！')
    if idiot == 'update':
        print('更新日志：')
        print('  舰船生成逻辑改变，添加了除了大凤以外的舰船，大型舰船周围的8格不会有其他大型舰船')
        print('  大青花鱼的提示改变，现在仅在周围8格范围内会提示"猎物靠近"')
        print('  其他情况均提示"不在这里"（只针对大凤，不会提示其他舰船）')
        print('  有非常高概率生成雪风，你能在炸到大凤之前炸到雪风么')
    elif idiot != 'y':
        print('不要整活，请输入y或者n')

#选择难度
difficulty = 1
#while difficulty not in ['1', '2', '3', '4']:
    #print('请选择难度：')
    #print('1：简单（5X5海域，4艘大型舰船，10发鱼雷）')
    #print('2：普通（7X7海域，5艘大型舰船，15发鱼雷）')
    #print('3：困难（10X10海域，8艘大型舰船，20发鱼雷）')
    #print('4：自定义')
    #difficulty = input()
    #if difficulty not in ['1', '2', '3', '4']:
        #print('请输入正确的难度')
#difficulty = int(difficulty)


#游戏初始化

#初始弹药10
ammo = 10

#生成5X5显示海域
x_axis_range = 5
y_axis_range = 5
x_axis = ['      ','   A  ','   B  ','   C  ','   D  ','   E  ']
y_axis = ['      ','   1  ','   2  ','   3  ','   4  ','   5  ']
ocean = []
for i in range(y_axis_range + 1):
    temp = []
    for j in range(x_axis_range + 1):
        temp.append(' ≈≈≈≈ ')    #空海域填满' ≈≈≈≈ '
    ocean.append(temp)
for i in range(0,y_axis_range + 1):    #显示X,Y轴
    ocean[0][i] = x_axis[i]
for i in range(1,x_axis_range + 1):
    ocean[i][0] = y_axis[i]

#生成5*5舰船海域
target = []    #储存海域每个点位的某个相应值（是否有东西，舰船，还是特殊道具）
for i in range(x_axis_range):
    temp = []
    for j in range(y_axis_range):
        temp.append(0)
    target.append(temp)    #遍历海域，为每个点位赋值，默认赋0
target_dict = {}
vocab_target_dict = []
for i in range(x_axis_range):
    temp = []
    for j in range(y_axis_range):
        target_dict[i+1,j+1] = target[i][j]    #生成对海域每个点的索引，[x,y]对应target[x][y]
        vocab_target_dict.append([i+1,j+1])    #将海域坐标塞进一个大list，用于随机生成

#随机生成舰船
#Rule:'为了防止碰撞，重樱的大型舰船之间至少会保留一格的空间，也就是舰船周围的8个格子里不会有其他大型舰船'
all_ship = [' 信浓 ',' 武藏 ',' 加贺 ',' 赤城 ',' 翔鹤 ',' 瑞鹤 ']
random.shuffle(all_ship)
ship = {0:' 大凤 '}
for i in range(1, difficulty + 3):    #随机选取三艘大型舰船
    ship[i] = all_ship[i]
ship_pos = []
for i in range(0, len(ship)):
    ship_pos.append(generate_ship())    #随机生成一艘舰船位置
    #print('ship_pos=', ship_pos)     #test用
    l = len(vocab_target_dict)    
    for j in range(l):
        q = l-(j+1)    #倒序检索（由于pop之后len(vocab_target_dict)会有变化）
        if abs(vocab_target_dict[q][0] - ship_pos[i][0]) <= 1 and abs(vocab_target_dict[q][1] - ship_pos[i][1]) <= 1:
            vocab_target_dict.pop(q)    #删除的生成舰船及周围1格内最多9格元素
            #print('vocab_target_dict=', vocab_target_dict) #test


#为舰船赋予体积

#显示舰船受伤/击沉

#特殊道具
#随机生成特殊道具

#使用特殊道具

#核弹'爆炸范围3*3'

#雷达扫描'范围4*4（进阶：但是有几率导致被扫到的舰船开始逃离）'

#空袭支援'对某一行/列进行攻击'


show_area()
hump = 0    #五次输错之后结束游戏
hit = False    #判断击中大凤，游戏结束
attacked = []    #储存已攻击过的坐标
while ammo > 0:
    if hump >= 5:    #五次输错之后结束游戏
        print('哼！就知道捣乱，大青花鱼不跟你玩了啦')
        break
    torpedo = input('请输入要发射鱼雷的坐标，比如：A3(可以输入小写字母)：').upper()
    print('\n')
    if not judge_point(torpedo):
        print('不要乱搞，请输入正确的坐标')
        hump += 1
    elif torpedo in attacked:
        hump += 1
        print('那个位置已经炸过，不对寻找过了哦，请选一个其他位置')
    else:
        ammo -= 1
        torpedo_x = alp_num[torpedo[0]]
        torpedo_y = int(torpedo[1])
        torpedo_pos = [torpedo_x, torpedo_y]
        attacked.append(torpedo)    #储存已攻击过的坐标
        if torpedo_pos == ship_pos[0]:  #命中
            for i in range(len(ship_pos)):
                ocean[ship_pos[i][1]][ship_pos[i][0]] = ship[i]
            hit = True
            print('恭喜你，你帮大青花鱼找到了大凤！','\n')
            break
        elif torpedo_pos in ship_pos:    #命中其他舰船
            for i in range(1,len(ship_pos)):
                if torpedo_pos == ship_pos[i]:
                    ocean[torpedo_y][torpedo_x] = ship[i]
            show_area()
            ammo += 1
            print('你找到了一艘舰船，但是貌似并不是大凤......奖励你一发鱼雷，再试试吧','\n','剩余鱼雷',ammo,'发')
        else:    #miss
            ocean[torpedo_y][torpedo_x] = '  XX  '
            show_area()
            print('不好意思，你没有帮大青花鱼找到大凤，再来一次吧','\n','剩余鱼雷',ammo,'发')
        if abs(torpedo_y - ship_pos[0][1]) <= 1 and abs(torpedo_x - ship_pos[0][0]) <= 1:
            print('猎物接近的预感呢')
        if abs(torpedo_y - ship_pos[0][1]) >= 2 or abs(torpedo_x - ship_pos[0][0]) >= 2:
            print('好像不在这附近呢')
yuki()
if hump == 5:
    print('也许你并不真正拥有理解游戏规则的智能')
elif hit == False:
    for i in range(len(ship_pos)):
        ocean[ship_pos[i][1]][ship_pos[i][0]] = ship[i]
    show_area()
    print('大凤藏在',[num_alp[ship_pos[0][0]],ship_pos[0][1]],'\n','你最终没有帮大青花鱼找到大凤，菜就多练')
else:
    show_area()
    print('谢谢你帮助大青花鱼找到了她的朋友大凤，现在她可以和她的朋友一起愉快的玩耍了')
