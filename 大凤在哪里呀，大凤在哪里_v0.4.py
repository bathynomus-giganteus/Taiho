import random

#定义游戏内部函数

#横坐标字母数字互相转化
num_alp = {1:'A',2:'B',3:'C',4:'D',5:'E',6:'F',7:'G',8:'H',9:'I',10:'J',11:'K',12:'L',13:'M',14:'N',15:'O',16:'P',17:'Q',18:'R',19:'S',20:'T',21:'U',22:'V',23:'W',24:'X',25:'Y',26:'Z'}
alp_num = {num_alp[alp]:alp for alp in num_alp}

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
    print('你理解规则了吗？（输入log查看更新日志）')
    idiot = input('理解了：y   完全不懂：n''\n')
    idiot = idiot.lower()
    if idiot == 'n':
        print('这么简单的规则怎么理解不了啊？杂鱼杂鱼！')
    if idiot == 'log':
        print('更新日志v_0.4：')
        print('  底层架构完全改变，现在用一个list储存所有位置的信息，信息呈现机制也进行了修改')
        print('  添加了难度选择，添加了自定义关卡，目前暂时只能选择正方形关卡，最大15*15')
        print('  道具数量也可以自定义，舰船数量是自动生成的，暂时不支持修改')
        print('  虽然增加了道具，但目前还是卫星，暂时不会生成道具')
        print('  大凤距离提示改回三段提示，但是范围不一样')
    elif idiot != 'y':
        print('不要整活，请输入y或者n')

#游戏初始化
#选择难度
difficulty = ''    
generator = [['axis_range',5,15], ['ammo',10,100], ['bonus',1,3], ['item',0,10]]
generator_text = ['请输入海域宽度（5~15）：','初始鱼雷数量 10~100：','命中奖励鱼类数量 1~3：','特殊道具数量 0~10：']
difficulty_vocab = {1:'简单',2:'普通',3:'困难',4:'自定义'}
while difficulty not in ['1', '2', '3','4']:
    print('请选择难度：')
    print('1：简单（5X5海域，4艘大型舰船，10发鱼雷）')
    print('2：普通（7X7海域，6艘大型c舰船，15发鱼雷）')
    print('3：困难（9X9海域，8艘大型舰船，20发鱼雷）')
    print('4：自定义')
    difficulty = input()
    if difficulty not in ['1', '2', '3', '4']:
        print('请输入正确的难度')
difficulty = int(difficulty)
if difficulty == 4:    #建立两个list，通过一个for+一个while循环完成自定义关卡的设定
    for i in range(len(generator)):
        while isinstance(generator[i][0], str):    #只要输入值不符合条件，就不会被变为int，任然是str，while循环就不会停止
                print(generator_text[i])
                generator[i][0] = input()    #用generator接收输入值
                if not generator[i][0] in [str(j) for j in range(generator[i][1],generator[i][2]+1)]:    #从list抽取判定条件
                    print('请输入正确的值，范围：',generator[i][1],'~',generator[i][2])
                else:
                    generator[i][0] = int(generator[i][0])    #只有符合条件的值才会被变为int
    axis_range = generator[0][0]    #根据最后获得的generator，生成对应的必要变量
    ammo = generator[1][0]
    bonus = generator[2][0]
    item = generator[3][0]
    ship_num = ((axis_range - 1)//3 + 1)**2
    print('关卡设置完毕')
else:    #非自定义难度下直接通过difficulty生成对应的必要变量
    axis_range = difficulty*2 + 3 
    bonus = 1
    ammo = (difficulty+1)*5
    item = difficulty * 2
    ship_num = (difficulty+1)*2
print('当前难度：',difficulty_vocab[difficulty],'\n')


#生成海域
target = {}
#target = {id:[(a,b),c,d,e,f,g,h]}
#储存海域每个点位的某个相应值，索引为海域点位的id，指向的储存点位属性
#(a,b)储存点位的坐标
#c储存的属性，0代表' ≈≈≈≈ '空海域，1代表大型舰船，2代表小型舰船，3代表'  XX  '攻击过的位置，4代表道具，5代表空，但是由于周围有大型舰船而无法生成大型舰船的位置
#d储存点位的隐藏属性，0代表隐藏，无视a显示空海域，1代表非隐藏，按照正常显示，
#e存储物品的具体信息，舰船id和物品id
#剩余的f，g，h作为备用
a = 0
for i in range(1, axis_range+1):
    for j in range(1, axis_range+1):
        a += 1
        target[a] = [[i,j],0,0,0,0,0,0]
        #target[0]储存坐标，target[1]储存状态，target[2]储存隐藏属性，target[3]储存物品和舰船id

#测试用函数，输出整个target，检查用
def show_target():
    for i in range(1, len(target) + 1):
        print(target[i])

#随机生成舰船
#Rule:'为了防止碰撞，重樱的大型舰船之间至少会保留一格的空间，也就是舰船周围的8个格子里不会有其他大型舰船'
#生成大型舰船
all_ship = [' 信浓 ',' 武藏 ',' 加贺 ',' 赤城 ',' 翔鹤 ',' 瑞鹤 ',' 苍龙 ',' 飞龙 ',' 龙凤 ',' 金刚 ',' 比睿 ',' 榛名 ',' 雾岛 ',' 扶桑 ',' 山城 ',' 长门 ',' 陆奥 ',' 大和 ',' 天城 ',' 龙骧 ',' 凤翔 ',' 云龙 ',' 伊势 ',' 日向 ',' 葛城 ']
random.shuffle(all_ship)    #把舰名列表洗牌，然后从头输出，达到随机的效果
ship = {1:' 大凤 '}    #1号id的大型舰必定是大凤
for i in range(2, ship_num+1):    #随机选取几艘大型舰船
    ship[i] = all_ship[i]    #依次赋值，舰船id从1开始

#放置大型舰船
for i in range(1, ship_num+1):
    #重置上一个循环的available合法数组，将可生成大型舰船的位置id整合到这数组中
    #可参与生成的点位其四号位数值必须不为1或3，即不能已有大型舰船或者在已有大型舰船周边8格
    available = []    #建立数组储存合法的位置
    for a in range(1, len(target)+1):    #遍历所有位置
        if target[a][1] != 1 and target[a][1] != 5:    #如果该位置的属性值不为1（存在大型舰）或5（位于大型舰1格以内）
            available.append(a)    #视为合法位置并传到合法位置的数组中
    #随机生成一个大型舰船
    if len(available) <= 0:    #如果合法数组已经没有位置，强制结束
        break
    elif len(available) == 1:     #如果只有一个可能位置，无法生成随机数，直接传出该位置
        n = 1
    else:
        n = random.randint(0, len(available)-1)    #随机选取一个合法位置
    b = available[n]    #储存传出位置在target中的id
    #为生成大型舰船的点位赋值（4号位赋值舰船属性，5号位赋值舰船id）
    target[b][1] = 1    #对target中的位置进行赋值，为所选的合法位置赋值1，表示已经放置了大型舰
    target[b][3] = i
    #为所放置的大型舰周围格子赋值（赋值5，这样在下一循环中会被踢出合法数组，表示因周围有舰船而不能参与后续生成）
    for c in range(1, len(target)+1):
        if abs(target[c][0][0] - target[b][0][0]) <= 1 and abs(target[c][0][1] - target[b][0][1]) <= 1 and target[c][1] != 1:
            target[c][1] = 5

#生成小型舰船
all_small_ship =['  雷  ','  电  ','  晓  ','  响  ',' 阳炎 ',' 岛风 ',' 村雨 ',' 时雨 ',' 凌波 ',' 吹雪 ',' 夕立 ']
#逻辑类似大型舰船，无法参与生成的位置改为‘if target[a][1] != 1 and target[a][1] != 2’
#即即将放置的位置没有大型舰船或者小型舰船，但是小型舰船可以放置在大型舰船一格以内
random.shuffle(all_small_ship)
small_ship = {}
for i in range(1, ship_num+1):
    small_ship[i] = all_small_ship[i]
for i in range(1, len(small_ship)+1):
    available = []
    for a in range(1, len(target)+1):
        if target[a][1] != 1 and target[a][1] != 2:
            available.append(a)
    #随机生成一个小型舰船
    if len(available) <= 0:
        break
    elif len(available) == 1:
        n = 1
    else:
        n = random.randint(1, len(available))
    b = available[n-1]
    target[b][1] = 2
    target[b][3] = i
    #小型舰周围没有放置限制，所以比大型舰少一步

#击中舰船

#为舰船赋予体积？

#显示舰船受伤/击沉？

#特殊道具
#随机生成特殊道具
item_vocab = [' 核弹 ',' 雷达 ',' 空袭 ']
item_seq = []
for i in range(item):
    t = random.randint(1, 100)
    if t <= 50:
        item_seq.append(item_vocab[1])
    elif t <= 80:
        item_seq.append(item_vocab[0])
    else:
        item_seq.append(item_vocab[2])

#使用特殊道具

#核弹'爆炸范围3*3'

#海伦娜的雷达扫描'范围4*4'

#斯蒂芬·波特的空袭引导'对某一行/列进行攻击'

#生成显示海域
#生成xy轴
x_axis = ['      '] + ['  ' + num_alp[i] + '   ' for i in range(1,21)]
y_axis = ['      '] + ['  ' + str(i) + '  ' for i in range(1,10)] + ['  ' + str(i) + ' ' for i in range(10,21)]
ocean = []    #生成海域显示矩阵，由于要存储xy轴，所以比target大一圈
for i in range(axis_range + 1):
    temp = []
    for j in range(axis_range + 1):
        temp.append('')    #直接先填满''
    ocean.append(temp)    #注意ocean的横坐标在后，纵坐标在前
for i in range(0,axis_range + 1):    #填入X,Y轴
    ocean[0][i] = x_axis[i]
for i in range(1,axis_range + 1):
    ocean[i][0] = y_axis[i]

#定义函数输出海域
def show_area():
    for z in range(1, len(target) + 1):    #对所有位置进行遍历
        y = target[z][0][1]    #抓取横纵坐标（注意ocean是纵坐标在前）
        x = target[z][0][0]
        if target[z][2] == 0:    #如果隐藏属性值为1，说明该海域暂不显示，强制显示波浪
            ocean[y][x] = ' ≈≈≈≈ '
        elif target[z][1] == 0 or target[z][1] == 5:    #空海域显示波浪
            ocean[y][x] = ' ≈≈≈≈ '
        elif target[z][1] == 1:    #如果是大型舰船，显示大型舰船船名
            ocean[y][x] = ship[target[z][3]]
        elif target[z][1] == 2:    #如果是小型舰船，显示小型舰船船名
            ocean[y][x] = small_ship[target[z][3]]
        elif target[z][1] == 3:    #空海域但是已经炸过了，需要显示（后续可能还需要显示扫描过的空海域）
            ocean[y][x] = '  XX  '
        elif target[z][1] == 4:    #如果是道具，显示道具
            ocean[y][x] = item[target[z][1]]
    for w in range(axis_range+1):    #将显示矩阵整合输出
        print(''.join(ocean[w]))
    print('\n')

#显示真实海域，除了绕过隐藏属性值判定，其他和上一个函数和完全一样
#这样便可以在不影响属性值的情况下直接观察海域情况
def show_real_area():
    for z in range(1, len(target) + 1):
        y = target[z][0][1]
        x = target[z][0][0]
        if target[z][1] == 0 or target[z][1] == 5:
            ocean[y][x] = ' ≈≈≈≈ '
        elif target[z][1] == 1:
            ocean[y][x] = ship[target[z][3]]
        elif target[z][1] == 2:
            ocean[y][x] = small_ship[target[z][3]]
        elif target[z][1] == 3:
            ocean[y][x] = '  XX  '
        elif target[z][1] == 4:
            ocean[y][x] = item[target[z][1]]
    for w in range(axis_range+1):
        print(''.join(ocean[w]))
    print('\n')

#鱼雷攻击目标点函数
def judge_point(torpedo):    #输入坐标需为长度为2或3的str，且范围不能超过当前坐标范围，如果长度为3，需将后两位组合
    if len(torpedo) == 2 and torpedo[0] in [num_alp[i] for i in range(1,axis_range+1)] and torpedo[1] in [str(i) for i in range(1,axis_range+1)]:
        return True
    elif len(torpedo) == 3 and torpedo[0] in [num_alp[i] for i in range(1,axis_range+1)] and torpedo[1] + torpedo[2] in [str(i) for i in range(1,axis_range+1)]:
        return True
    else:
        return False
    
#抓取大凤坐标
for a in range(1, len(target)+1):
    if target[a][1] == 1 and target[a][3] == 1:
        Taiho_x = target[a][0][0]
        Taiho_y = target[a][0][1]

show_area()
hump = 0    #五次输错之后结束游戏
hit = False    #判断击中大凤，游戏结束
attacked = []    #储存已攻击过的坐标
print('剩余鱼雷',ammo,'发')
while ammo > 0:
    if hump >= 5:    #五次输错之后结束游戏
        print('哼！就知道捣乱，大青花鱼不跟你玩了啦')
        break
    print('当前难度：',difficulty_vocab[difficulty], '特殊道具：无')    #当前轮次开始的提示
    torpedo = input('请输入要发射鱼雷的坐标，比如：A3(可以输入小写字母)：').upper()
    if torpedo == 'CHEAT':    #加入了个作弊小代码，方便测试
        show_real_area()
    elif not judge_point(torpedo):    #如果输入坐标不符合规范，重新要求输入
        print('不要想了，没有什么作弊代码，请输入正确的坐标')
        hump += 1
    elif torpedo in attacked:    #已经炸过的位置不能再炸
        hump += 1
        print('那个位置已经炸过，不对寻找过了哦，请选一个其他位置')
    else:
        attacked.append(torpedo)    #存储已经炸过的位置，仅供判定用，所以只存储最初始的输入字符串
        torpedo = list(torpedo)    #str转为list
        if len(torpedo) == 3:    #如果输入字符串长度为3，需将后两位组合成一个数字
            torpedo[1] = torpedo[1] + torpedo[2]
            torpedo.pop()
        print('\n')
        ammo -= 1
        #torpedo_x =    
        #torpedo_y = 
        for a in range(1, len(target)+1):    #遍历所有的位置
            if target[a][0][0] == alp_num[torpedo[0]] and target[a][0][1] == int(torpedo[1]):    #寻找横纵坐标与输入坐标相符的位置
                break    #找到炸点，停止遍历
        if target[a][1] == 0 or target[a][1] == 5:    #未命中
            target[a][2] = 1    #取消该点的隐藏
            target[a][1] = 3    #将该点转化为空但是被炸过的点
            show_area()
            print('不好意思，你没有帮大青花鱼找到大凤，再来一次吧','\n','剩余鱼雷',ammo,'发','\n')
        elif target[a][1] == 1:    #如果命中的位置是大型舰船
            if target[a][3] == 1:    #如果舰船id是1（是大凤）
                hit = True
                break    #炸到大凤游戏直接结束
            else:    #如果舰船id不是1（命中了，但不是大凤）
                target[a][2] = 1    #取消该点的隐藏，不需再赋值，直接显示大型舰舰名
                show_area()
                ammo += bonus
                print('你找到了一艘舰船，但是貌似并不是大凤......奖励你一些鱼雷，再试试吧','\n','剩余鱼雷',ammo,'发','\n')
        elif target[a][1] == 2:    #命中小型舰船
            target[a][2] = 1    #取消该点的隐藏，不需再赋值，直接显示小型舰舰名
            show_area()
            ammo += bonus
            print('你找到了一艘舰船，但是貌似并不是大凤......奖励你一些鱼雷，再试试吧','\n','剩余鱼雷',ammo,'发','\n')
        elif target[a][1] == 4:    #命中道具
            target[a][2] = 1    #取消该点的隐藏，不需再赋值，直接显示道具名
            show_area()
            ammo += bonus
            print('你找到了一件特殊道具，但是非常抱歉，暂时还没有什么作用，作为补偿，给你三发鱼雷吧','\n','剩余鱼雷',ammo,'发','\n')
    #大凤距离的提示
    if abs(alp_num[torpedo[0]] - Taiho_x) <= 2 and abs(int(torpedo[1]) - Taiho_y) <= 2:
        print('猎物接近的味道呢')
    elif abs(alp_num[torpedo[0]] - Taiho_x) >= 5 or abs(int(torpedo[1]) - Taiho_y) >= 5:
        print('貌似不在这附近')
    else:
        print('到底在哪里呢')

#随机生成雪风
small_ship[ship_num + 1] = ' 雪风 '
available = []
for a in range(1, len(target)+1):
    if target[a][1] == 0 or target[a][1] == 5:
        available.append(a)
#随机生成一个小型舰船
if len(available) == 1:
    n = 1
elif len(available) >= 2:
    n = random.randint(1, len(available))
b = available[n-1]
target[b][1] = 2
target[b][3] = ship_num + 1

show_real_area()    #显示真实海域
if hump == 5:
    print('也许你并不真正拥有理解游戏规则的智能')
elif hit == True:
    print('恭喜你，你帮大青花鱼找到了大凤！','\n''谢谢你帮助大青花鱼找到了她的朋友大凤，现在她可以和她的朋友一起愉快的玩耍了')
else:
    print('你最终没有帮大青花鱼找到大凤，菜就多练')