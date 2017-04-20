from tkinter import *
import math
import os
import serial
import sys
import time
import threading
import unicodedata

class autogo:
    def window(self):
        win = Tk()
        self.exitflag = 0
        self.ang = 0
        self.flinesub = 0
        self.lo = 0
        self.adjust = 0
        self.disbit = 0
        self.readbuf = "a".encode("ascii")
        self.nowangle = StringVar()
        self.nowdistance = StringVar()
        self.aimangle = StringVar()
        self.aimdistance = StringVar()
        self.sernumber = StringVar()
        self.gra = Canvas(win, width=400, height=200, bg="white")
        self.tip = StringVar()
        self.ser = ""
        self.info = ""

        win.title("自动帆板控制系统")
        fra = Frame(win)
        text = Label(win, text="## 参赛选手：金翼飞 && 丰德浪 && 赵琦 ##", fg="blue")
        lab1 = Label(fra, text="监测角度：")
        nowang = Label(fra, textvariable=self.nowangle, fg="red")
        lab2 = Label(fra, text="监测距离：")
        nowdis = Label(fra, textvariable=self.nowdistance, fg="green")
        lab3 = Label(fra, text="目标角度(°)：")
        aimang = Entry(fra, textvariable=self.aimangle)
        lab4 = Label(fra, text="目标距离(cm)：")
        aimdis = Entry(fra, textvariable=self.aimdistance)
        lab5 = Label(fra, text="串口序号：COM")
        sernum = Entry(fra, textvariable=self.sernumber)
        exitbutton = Button(fra, text = "安全退出系统", command = self.safeexit)
        runbutton = Button(fra, text = "开始逼近并监测目标", command = self.run)
        lab6 = Label(fra, text="运行状态：")
        labtip = Label(fra, textvariable = self.tip, fg = "red")
        self.gra.create_line(200, 50, 200, 175, width = 2, tags = "tline")
        self.gra.create_line(200, 50, 200, 175,width=5, fill="red", tags="fline")
        self.gra.create_oval(195, 45, 205, 55, tags = "orig", fill = "black")
        self.gra.create_text(35, 10, text = "实时角度：", tags = "arganglab")
        self.gra.create_text(35, 25, text = "加速误差：", tags = "adjsub")
        self.gra.create_text(35, 40, text = "实时距离：", tags = "dislab")
        self.gra.create_text(35, 55, text = "距离误差：", tags = "dissub")

        text.pack()
        lab1.grid(row=1, column=1, sticky=W)
        nowang.grid(row=1, column=2)
        lab2.grid(row=1, column=3)
        nowdis.grid(row=1, column=4)
        lab3.grid(row=2, column=1, sticky=W)
        aimang.grid(row=2, column=2)
        lab4.grid(row=3, column=1, sticky=W)
        aimdis.grid(row=3, column=2)
        lab5.grid(row=2, column=3)
        sernum.grid(row=2, column=4)
        exitbutton.grid(row = 3, column = 3)
        runbutton.grid(row=3, column=4)
        lab6.grid(row=4, column=1, sticky=W)
        labtip.grid(row = 4, column = 2)
        fra.pack()
        self.gra.pack()

        win.mainloop()

    def run(self):
        try:
            self.ser.close()
        except:
            check = 1
        check = 1
        self.adjust = 0
        if (not self.sernumber.get().isdigit()):
            check = 0
            self.sernumber.set("串行端口错误!")
            self.tip.set("你需要检查你的输入")
        if (not self.aimangle.get().isdigit()):
            check = 0
            self.aimangle.set("角度错误!")
            self.tip.set("你需要检查你的输入")
        if (not self.aimdistance.get().isdigit()):
            check = 0
            self.aimdistance.set("距离错误!")
            self.tip.set("你需要检查你的输入")
        if (check):
            try:
                self.ser = serial.Serial('com' + self.sernumber.get(), 19200)
                t2 = threading.Thread(target=self.rec)
                t2.start()
            except WindowsError:
                check = 0
                self.sernumber.set("串行端口错误!")
                self.tip.set("串口被占用或不存在")
            if (check):
                if(not eval(self.aimdistance.get())):
                    aim = 0
                else:
                    aim = eval(self.aimdistance.get())
                iloop = int(aim * 34) - int(self.disbit)
                if(iloop > 0):
                    for i in range(1, iloop + 1):
                        self.ser.write("F".encode("ascii"))
                        self.disbit += 1
                        time.sleep(0.15)
                if(iloop < 0):
                    for i in range(1, abs(iloop + 1)):
                        self.ser.write("B".encode("ascii"))
                        self.disbit -= 1
                        time.sleep(0.15)
                try:
                    t3 = threading.Thread(target=self.adj)
                    t3.start()
                except:
                    self.tip.set("监控调整进程启动失败")



    def rec(self):
        while (not self.exitflag):
            if(self.exitflag):
                break
            self.receive()

    def receive(self):
        self.readbuf = self.ser.read()
        if (self.readbuf is b'\n'):
            self.lo += 1
            info = self.info.split('\t')
            try:
                x = eval(info[0])
                y = eval(info[1])
                z = eval(info[2])
            except:
                no = 1
            self.adjust = 1
            self.display(-y, z)
            self.info = ""
        else:
            self.info += self.readbuf.decode("ascii")

    def safeexit(self):
        if (self.disbit > 0):
            for i in range(1, abs(self.disbit + 1)):
                self.ser.write("B".encode("ascii"))
                time.sleep(0.15)
        self.exitflag = 1
        time.sleep(1)
        try:
            self.ser.close()
        except:
            no = 1
        exit(0)

    def display(self,y,z):
        at = math.atan(y/z)
        ang = 90+at*180/3.1415926+11.5
        if(ang >= 120):
            ang = -(180 - ang)
            at = ((ang-90)*3.1415926/180)
        self.gra.delete("argang", "orig", "dis")
        
        self.flinesub += ang
        self.gra.create_text(80, 40, text = str(round(self.disbit / 34, 2)), tags = "dis")
        self.gra.create_text(80, 10, text=str(round(ang, 2)), tags="argang", fill="green")
        self.gra.create_oval(195, 45, 205, 55, tags="orig", fill = "black")
        if(self.lo==5):
            self.flinesub =  self.flinesub / 5
            at = ((self.flinesub-90)*3.1415926/180)
            adjsub = abs(eval(self.aimangle.get())-self.flinesub)
            adjfill = "red"
            if (adjsub <= 30):
                adjfill = "orange"
            if(adjsub <= 10):
                adjfill = "green"
            self.gra.delete("fline", "adj", "win")
            self.nowangle.set(str(round(self.flinesub,2)) + "°")
            self.gra.create_text(85, 25, text=str(round(adjsub, 2)) + "°", tags="adj", fill=adjfill)
            self.gra.create_line(200, 50, 200 + 125 * math.sin(at + 3.1415926 / 2),
                                 50 + 125 * math.cos(at + 3.1415926 / 2), width=5,
                                 fill="red", tags="fline")
            if(adjsub <= 10):
                self.gra.create_text(100, 175, text="你说我们棒不棒！？", tags="win", fill="green")
            self.lo = 0
            self.flinesub = 0
        self.ang = ang

    def adj(self):
        while(not self.exitflag):
            if(self.exitflag):
                break
            if (self.adjust):
                ang = round(eval(self.aimangle.get()) - self.ang, 0)
                if (ang > 0):
                    self.ser.write("A".encode("ascii"))
                if (ang < 0):
                    self.ser.write("S".encode("ascii"))
                time.sleep(0.03)

go = autogo()
global exitflag
exitflay = 0
t1 = threading.Thread(target = go.window)
t1.start()
