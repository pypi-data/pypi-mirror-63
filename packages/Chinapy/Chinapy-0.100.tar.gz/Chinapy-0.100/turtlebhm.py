from pypro.turtlebhh import*
#自动画圆环软件
def yhrj():
    a = input("你想画几个圆的圆环？\n")
    b = input("圆的半径是多少？")
    lh(a,b)
#自动画随机多边形软件
def sjdbx():
    gs = input("你要画几个随机多边形？")
    gs = int(gs)
    for i in range(gs):
        sjhlx(random.randint(20,60),random.randint(4,12))



