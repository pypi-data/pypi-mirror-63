import turtle
import random
#画正的正方形螺旋，bs代表边数的拼音
def zzfx(bs):
    tutu = turtle.Turtle()
    for i in range(bs):
        tutu.forward(i)
        tutu.left(90)
#画斜的正方形螺旋，bs代表边数的拼音，jd代表角度的拼音
def xzfx(bs,jd):
    tutu = turtle.Turtle()
    for i in range(bs):
        tutu.forward(i)
        tutu.left(jd)
#画连在一起的圆环，gs是圆环数量的缩写，dx是大小的缩写（半径）
def lh(gs,dx):
    gs = int(gs)
    dx = int(dx)
    tutu = turtle.Turtle()
    jd = 360 / gs
    for i in range(gs):
        tutu.circle(dx)
        tutu.left(jd)
#画N边形，bx是边形的拼音，bc是边长的拼音
def hnbx(bx,bc):
    tutu = turtle.Turtle()
    jd = 360 / bx
    for i in range(bx):
        tutu.forward(bc)
        tutu.left(jd)
#画任意边数螺旋，bs是边数的缩写，bx是边形的缩写
def hlx(bs,bx):
    tutu = turtle.Turtle()
    jd = 360 / bx
    for i in range(bs):
        tutu.forward(i)
        tutu.left(jd)
#画随机位置的任意边数螺旋，bs是边数的缩写，bx是边形的缩写
def sjhlx(bs,bx):
    sj1 = random.randint(-200,200)
    sj2 = random.randint(-300,300)
    tutu = turtle.Turtle()
    tutu.goto(0,0)
    tutu.penup()
    tutu.goto(sj2,sj1)
    tutu.pendown()
    jd = 360 / bx
    for i in range(bs):
        tutu.forward(i+1)
        tutu.left(jd)
    tutu.hideturtle()
    tutu.speed(10)



    
    
    
    

