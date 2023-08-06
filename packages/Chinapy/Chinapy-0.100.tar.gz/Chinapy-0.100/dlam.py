import turtle as t
import math


# 计算长度、角度 t1:画笔对象  r:半径  angle:扇形（圆形）的角度
def myarc(t1, r, angle):
    arc_length = 2 * math.pi * r * angle / 360  # angle角度的扇形的弧长
    n = int(arc_length / 3) + 1  # 线段条数
    step_length = arc_length / n  # 每条线段的长度
    step_angle = angle / n  # 每条线段的角度
    mypolyline(t1, n, step_length, step_angle)


# 画弧线 t1:画笔对象  n:线段条数  length:每条线段长度  angle:每条线段的角度
def mypolyline(t1, n, length, angle):
    for index in range(n):
        t1.fd(length)
        t1.lt(angle)


# 设置画布大小，背景色
t.screensize(500, 500, "white")
# 画笔宽度
t.pensize(2)
# 画笔颜色
t.pencolor("black")
# 画笔移动速度 [1-10]
t.speed(10)

# 头部
t.fillcolor("#57a3c7")
t.begin_fill()
t.circle(100)
t.end_fill()

# 白芯
t.fillcolor("#fff")
t.begin_fill()
t.circle(85)
t.end_fill()

# 左眼睛
t.penup()
t.goto(-22, 130)
t.pendown()
step = 1
t.setheading(0)
t.fillcolor("#fff")
t.begin_fill()
for i in range(2):
    for j in range(60):
        if j < 30:
            step += 0.02
        else:
            step -= 0.02
        t.forward(step)
        t.left(3)
t.end_fill()
t.penup()
t.goto(-17, 150)
t.pendown()
# 左眼仁
step = 1
t.setheading(0)
t.fillcolor("#000")
t.begin_fill()
for i in range(2):
    for j in range(30):
        if j < 15:
            step += 0.0001
        else:
            step -= 0.0001
        t.forward(step)
        t.left(8)
t.end_fill()
# 左眼仁-白板
t.penup()
t.goto(-15, 160)
t.pendown()
t.fillcolor("#fff")
t.begin_fill()
t.circle(4)
t.end_fill()
# 右眼睛
t.penup()
t.goto(24, 130)
t.pendown()
step = 1
t.setheading(0)
t.fillcolor("#fff")
t.begin_fill()
for i in range(2):
    for j in range(60):
        if j < 30:
            step += 0.02
        else:
            step -= 0.02
        t.forward(step)
        t.left(3)
t.end_fill()
# 右眼仁
t.penup()
t.goto(17, 150)
t.pendown()
step = 1
t.setheading(0)
t.fillcolor("#000")
t.begin_fill()
for i in range(2):
    for j in range(30):
        if j < 15:
            step += 0.0001
        else:
            step -= 0.0001
        t.forward(step)
        t.left(8)
t.end_fill()
# 右眼仁-白板
t.penup()
t.goto(19, 160)
t.pendown()
t.fillcolor("#fff")
t.begin_fill()
t.circle(4)
t.end_fill()
# 鼻子
t.setheading(0)
t.penup()
t.goto(2, 115)
t.pendown()
t.fillcolor("#b74255")
t.begin_fill()
t.circle(13)
t.end_fill()
t.pensize(0)
t.penup()
t.goto(2, 115)
t.pendown()
t.fillcolor("#7e3048")
t.begin_fill()
t.circle(8)
t.end_fill()
t.penup()
t.goto(-1, 125)
t.pendown()
t.fillcolor("#fff")
t.begin_fill()
t.circle(5)
t.end_fill()
# 嘴巴
t.penup()
t.goto(-60, 80)
t.pendown()
step = 1
t.setheading(270)
t.fillcolor("#7e3048")
t.begin_fill()
myarc(t, 60, 190)
# 画弧线
t.setheading(180)
t.forward(120)
t.end_fill()
# 舌头
t.penup()
t.goto(2, 60)
t.setheading(120)
t.fillcolor("#ce665b")
t.pendown()
t.begin_fill()
myarc(t, 25, 170)
t.penup()
t.goto(45, 40)
t.setheading(70)
t.pendown()
myarc(t, 25, 170)
t.penup()
t.pencolor("#ce665b")
t.goto(-44, 40)
t.setheading(305)
t.pendown()
myarc(t, 53, 125)
t.end_fill()
t.pencolor("black")
# 左边胡子
t.pensize(3)
t.penup()
t.goto(-35, 120)
t.setheading(165)
t.pendown()
t.forward(50)
t.penup()
t.goto(-35, 110)
t.setheading(175)
t.pendown()
t.forward(50)
t.penup()
t.goto(-35, 100)
t.setheading(185)
t.pendown()
t.forward(50)
# 右边胡子
t.penup()
t.goto(35, 120)
t.setheading(7)
t.pendown()
t.forward(50)
t.penup()
t.goto(35, 110)
t.setheading(0)
t.pendown()
t.forward(50)
t.penup()
t.goto(35, 100)
t.setheading(353)
t.pendown()
t.forward(50)
# 身子-左腿
t.pensize(2)
t.pencolor("#57a3c5")
t.penup()
t.goto(-70, 35)
t.setheading(265)
t.fillcolor("#57a3c5")
t.begin_fill()
t.pendown()
for y in range(50):
    if y > 10:
        t.pencolor("black")
    if y < 35:
        t.left(0.3)
    else:
        t.right(0.3)
    t.forward(3)
t.setheading(0)
t.forward(60)
t.setheading(70)
t.forward(25)
t.setheading(90)
t.forward(90)
t.setheading(160)
t.forward(78)
t.end_fill()
# 左胳膊
t.fillcolor("#57a3c5")
t.begin_fill()
t.penup()
t.goto(-72, 32)
t.setheading(200)
t.pendown()
for y1 in range(90):
    t.forward(1)
    t.left(0.3)
t.setheading(300)
t.forward(35)
t.setheading(30)
t.forward(65)
t.setheading(88)
for y2 in range(2):
    if y2 == 1:
        t.pencolor("#57a3c5")
    t.forward(20)
t.end_fill()
# 左手
t.pencolor("black")
t.penup()
t.goto(-100, -25)
t.pendown()
t.fillcolor("#fff")
t.begin_fill()
t.circle(25)
t.end_fill()
# 身子-右腿
t.penup()
t.goto(70, 33)
t.setheading(275)
t.fillcolor("#57a3c5")
t.begin_fill()
t.pendown()
for y in range(50):
    if y < 35:
        t.right(0.3)
    else:
        t.left(0.3)
    t.forward(3)
t.setheading(180)
t.forward(60)
t.setheading(110)
t.forward(25)
t.setheading(90)
t.forward(90)
t.setheading(20)
t.forward(76)
t.end_fill()
# # 右胳膊
t.fillcolor("#57a3c5")
t.begin_fill()
t.penup()
t.goto(70, 28)
t.setheading(35)
t.pendown()
for y1 in range(30):
    t.forward(1.5)
    t.left(0.3)
t.setheading(330)
t.forward(35)
t.setheading(240)
for y2 in range(91):
    t.forward(1)
    t.right(0.3)
t.end_fill()
# # 右手
t.penup()
t.goto(110, 70)
t.pendown()
t.fillcolor("#fff")
t.begin_fill()
t.circle(25)
t.end_fill()
# 左脚
t.penup()
t.goto(-66, -100)
t.pendown()
t.fillcolor("#fff")
t.begin_fill()
t.setheading(190)
for x in range(50):
    t.forward(1)
    t.left(3)
for x1 in range(70):
    t.forward(1)
    t.left(0.8)
for x2 in range(22):
    t.forward(1)
    t.left(5)
t.setheading(190)
for x3 in range(20):
    t.forward(1)
    t.left(0.02)
for x4 in range(50):
    t.forward(1)
    t.right(1)
t.end_fill()
# 右脚
t.penup()
t.goto(66, -100)
t.pendown()
t.fillcolor("#fff")
t.begin_fill()
t.setheading(350)
for x in range(50):
    t.forward(1)
    t.right(3)
for x1 in range(70):
    t.forward(1)
    t.right(0.8)
for x2 in range(22):
    t.forward(1)
    t.right(5)
t.setheading(350)
for x3 in range(20):
    t.forward(1)
    t.right(0.02)
for x4 in range(50):
    t.forward(1)
    t.left(1)
t.end_fill()
# 肚子
t.penup()
t.setheading(0)
t.goto(0, -95)
t.pendown()
t.fillcolor("#fff")
t.begin_fill()
t.circle(50)
t.end_fill()
t.penup()
t.goto(-40, -45)
t.setheading(270)
t.pendown()
t.circle(40, 180)
t.setheading(180)
t.forward(80)
# 铃铛绳
t.fillcolor("#b13954")
t.begin_fill()
t.penup()
t.goto(-82, 27)
t.setheading(327)
t.pendown()
for z in range(170):
    t.forward(1)
    if z < 80:
        t.left(0.3)
    else:
        t.left(0.6)
for z1 in range(12):
    t.forward(1)
    t.left(10)
t.setheading(220)
for z2 in range(162):
    t.forward(1)
    if z2 < 70:
        t.right(0.5)
    elif z2 < 100:
        t.right(0.8)
    else:
        t.right(0.2)
for z3 in range(20):
    t.forward(1)
    t.left(9.5)
t.end_fill()
# 铃铛
t.penup()
t.goto(0, 10)
t.setheading(0)
t.pendown()
t.fillcolor("#e1b959")
t.begin_fill()
t.circle(-17)
t.end_fill()
t.penup()
t.goto(2, -3)
t.pendown()
t.fillcolor("#4c442f")
t.begin_fill()
t.circle(-5)
t.end_fill()
t.penup()
t.goto(2, -8)
t.pendown()
t.setheading(275)
for k in range(15):
    t.forward(1)
    t.right(0.2)
t.penup()
t.goto(-18, -10)
t.pendown()
t.setheading(30)

# 隐藏画笔
t.hideturtle()
# 窗口不自动关闭
t.mainloop()
