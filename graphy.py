from graphics import *
from math import *
import tkinter as tk

def is_inside(pointer,space):
    ll = space.getP1()
    ur = space.getP2()
    return ll.getX() < pointer.getX() < ur.getX() and ll.getY() < pointer.getY() < ur.getY()

class graphing:
    def __init__(self,expr,zoom,accuracy):
        self.expr = expr
        self.zoom = zoom
        self.accuracy = accuracy
        self.length = 1000
        self.breath = 1000
        self.size = 20 * self.zoom
        self.unit = 20
        self.position_of_mark = self.zoom * self.unit/2

        self.ox = self.length/2               # x - origin
        self.oy = self.breath/2               # y - origin

        self.cnx = self.ox - self.ox * self.zoom        #corrected negative x-axis
        self.cpx = self.ox + self.ox * self.zoom        #corrected positve x-axis

        self.cny = self.oy - self.oy * self.zoom        #corrected positve y-axis
        self.cpy = self.oy + self.oy * self.zoom        #corrected positve y-axis

        self.leastCount = 0.1 * self.zoom / self.accuracy
        
        self.making()
        

    def mark_points(self,div,plot):
        for i in range(int((self.cnx-self.ox)/self.unit)+1,int((self.cpx-self.ox)/self.unit),div):
            if(-10<=i<=10):
                mk = Text(Point(self.ox+i*self.unit,self.oy+self.position_of_mark),str(i))
            elif(i>0):
                mk = Text(Point(self.ox+i*self.unit+(self.unit/2),self.oy+self.position_of_mark),str(i))
            elif(i<0):
                mk = Text(Point(self.ox+i*self.unit-(self.unit/2),self.oy+self.position_of_mark),str(i))
            mk.draw(plot)
            if(i==0):
                mk.undraw()

        for i in range(int((self.cny-self.oy)/self.unit)+1,int((self.cpy-self.oy)/self.unit),div):
            if(-10<i<10):
                mk = Text(Point(self.ox+self.position_of_mark,self.oy+i*self.unit),str(i))
            elif(i>0):
                mk = Text(Point(self.ox+self.position_of_mark,self.oy+i*self.unit+10),str(i))
            elif(i<0):
                mk = Text(Point(self.ox+self.position_of_mark,self.oy+i*self.unit-10),str(i))
            mk.draw(plot)
            if(i==0):
                mk.undraw()



    def making(self):
        #putting graph sheet
        self.graph = GraphWin("graph",self.length,self.breath)
        img = Image (Point(self.ox,self.oy),"./images/011.png")
        img.draw(self.graph)
        self.graph.setCoords(self.cnx,self.cny,self.cpx,self.cpy)
        
        #making axes
        p1 = Point(self.ox , self.cpy)
        p2 = Point(self.ox , self.cny)
        p3 = Point(self.cnx , self.oy)
        p4 = Point(self.cpx , self.oy)
        XAxis=Line(p3,p4)
        YAxis = Line(p1 , p2)
        XAxis.draw(self.graph)
        YAxis.draw(self.graph)
        
        #marking scale
        if(self.zoom>=1):
            self.mark_points(int(self.zoom),self.graph)
        else:
            self.mark_points(1,self.graph)
    
        #drawing graph
        x = (self.cnx-self.ox)/self.unit
        while(x<self.cpx-self.ox):
            try:
                pt2 = Point(self.ox+x*self.unit,self.oy+eval(self.expr)*self.unit)
                break
            except (ValueError, TypeError):
                x += self.leastCount
                continue
        pt2 = Point(self.ox+x*self.unit,self.oy+eval(self.expr)*self.unit)
        while(x<=(self.cpx-self.ox)/self.unit):
            try:                                            #checking for non-existance of graph with try and except
                x1 = self.ox+x*self.unit                    #x-coordinate of the current point
                y1 = self.oy+eval(self.expr)*self.unit      #y-coordinate of the current point
                pt = Point(x1,y1)                           #current point
    
                pt.draw(self.graph)
            except (ValueError, TypeError):
                x += self.leastCount
                continue
            ln = Line(pt,pt2) 
            ln.draw(self.graph)
            if((pt2.y-self.oy)*(pt.y-self.oy)< 0):
                if((pt.y-self.oy)< 0 ):
                    ln.undraw()
            if((pt.x-pt2.x)>10)or((pt.x-pt2.x)<-10):
                ln.undraw()

            x += self.leastCount
            pt2 = pt
            if(pt.y<0)or(pt.y>10*self.length):
                pt.undraw()
                ln.undraw()
        self.buttons()
        self.operate()
    
    def operate(self):
        #checking the mouse point and instructing the correct action
        pointer = self.graph.getMouse()
        if is_inside(pointer,self.zin):
            self.zoom_in()
        elif is_inside(pointer,self.zout):
            self.zoom_out()
        else:
            self.graph.close()
    
    def zoom_out(self):
        if(self.zoom<1):
            self.zoom = 1/((1/(self.zoom)-1)) 
        else:
            self.zoom += 1
        self.graph.close()
        self.__init__(self.expr,self.zoom,self.accuracy)
    def zoom_in(self):
        if(self.zoom>1):
            self.zoom -=1
        else:
            self.zoom = 1/((1/(self.zoom)+1)) 
        self.graph.close()
        self.__init__(self.expr,self.zoom,self.accuracy)
        
    def buttons(self):
        #creating button spaces
        self.zin = Rectangle(Point(self.cnx,(self.cpy-self.size)),Point(self.cnx+self.size,(self.cpy)))  
        self.zout = Rectangle(Point(self.cnx,(self.cpy-self.size*2)), Point(self.cnx+self.size, (self.cpy-self.size)))  
        self.zin.setFill("skyblue")
        self.zout.setFill("green")
        self.zin.draw(self.graph)
        self.zout.draw(self.graph)
        t1=Text(Point(self.cnx+self.size/2,(self.cpy-self.size/2)),"+")
        t1.draw(self.graph)
        t2=Text(Point(self.cnx+self.size/2,(self.cpy-self.size*1.5)),"-")
        t2.draw(self.graph)
        
        #(self.graph).bind("+",zoom_in)
        #(self.graph).bind("-",zoom_out)

if __name__ == "__main__":
    expr = input("Y = ")
#    zoom = 1/float(input("zoom= "))
    accuracy = float(input("accuracy = "))    
    gr1=graphing(expr,1,accuracy)

#1 make graph window outside the making loop
#2 import tkinter as tk
#3 writing zoom in, zoom out function
#4 change zoom input methods