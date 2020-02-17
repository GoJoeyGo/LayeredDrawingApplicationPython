import turtle
from PIL import Image, ImageEnhance,ImageDraw
penPositions = []
turtle.title("layered Drwaing Python")
def followMouse(x,y):
    turtle.Screen().onclick(None)
    turtle.penup()
    turtle.setpos(x,y)
    penPositions.append("Break")
    turtle.Screen().onclick(followMouse)
def followMouseDrag(x,y):
    turtle.ondrag(None)
    turtle.setpos(x,y)
    penPositions.append([x,-y])
    turtle.pd()
    turtle.ondrag(followMouseDrag)
def setMins(penPositions,padding):
    minX = minY = 10000000
    for xy in penPositions:
        if(str(xy)!="Break"):
            if(xy[0]<=minX): minX = xy[0]
            if(xy[1]<=minY): minY = xy[1]
    for xy in penPositions:
        if(str(xy)!="Break"):
            xy[0]=xy[0]-minX+padding
            xy[1]=xy[1]-minY+padding
    return penPositions
def findMax(penPositions):
    maxX = maxY = -10000000
    minX = 10000000
    for xy in penPositions:
        if(str(xy)!="Break"):
            if(xy[0]<=minX):minX = xy[0]
            if(xy[0]>=maxX):maxX = xy[0]
            if(xy[1]>=maxY):maxY = xy[1]
    return (int(maxX+minX),int(maxY+minX))
def drawStuff(im, arr,color):
    draw = ImageDraw.Draw(im)
    for index, item in enumerate(arr):
        if(item!="Break"):
            if(arr[index+1]!="Break"):
                x1= arr[index+1][0]
                y1= arr[index+1][1]
                draw.line((int(item[0]),int(item[1]),int(x1),int(y1)),color)
    im=smoothLine(im,color)
    return im
def smoothLine(im,color):
    draw = ImageDraw.Draw(im)
    for y in range(1, im.height-1):
        for x in range(1,im.width-1):
            b =[[str(im.getpixel((x, y)))==str(color),str(im.getpixel((x+1, y)))==str(color)],[str(im.getpixel((x, y+1)))==str(color),str(im.getpixel((x+1, y+1)))==str(color)]]
            if(b==[[1,0],[0,1]]):draw.point((x,y+1),color)
            if(b==[[0,1],[1,0]]):draw.point((x,y),color)
    return im
def draw():
    bgcolor = (0,0,0)
    color = (0,255,255)
    turtle.speed(0)
    turtle.bgcolor(bgcolor)
    turtle.color("#ff0000")
    turtle.shape("circle")
    turtle.pensize(2)
    turtle.shapesize(1)
    turtle.Screen().onclick(followMouse)
    turtle.ondrag(followMouseDrag)
    turtle.Screen().mainloop()
    penPositions.append("Break")
    penPositions.pop(0)
def makeImage(name,color1=(0,255,255),color2=(255,0,0),padding = 50, bgcolor=(0,0,0)):
    im = Image.new("RGB",findMax(setMins(penPositions,padding)),bgcolor)
    im = drawStuff(im, penPositions,color1)
    for x in range(250):
    	im = ImageEnhance.Sharpness(im).enhance(500)
    	im = ImageEnhance.Sharpness(im).enhance(-500)
    im = drawStuff(im, penPositions,color2)
    basewidth = im.width*4
    wpercent = ((basewidth)/float(im.size[0]))
    hsize = int((float(im.size[1])*float(wpercent)))
    im.resize((basewidth,hsize)).show()
    im.save(name)
draw()
makeImage("temp.png")
