import turtle
from PIL import Image, ImageEnhance, ImageDraw
newPenUp = " "
penPos = []
turtle.title("layered Drawing Python")
def draw(bgcolor=(0, 0, 0), pensize=2, color="#ff0000", shape="circle"):
    turtle.bgcolor(bgcolor)
    turtle.color(color)
    turtle.shape(shape)
    turtle.pensize(pensize)
    turtle.Screen().onclick(followMouse)
    turtle.ondrag(followMouseDrag)
    turtle.speed(0)
    turtle.Screen().mainloop()
    penPos.append(newPenUp)
    penPos.pop(0)
def drawStuff(im, arr, color):
    draw = ImageDraw.Draw(im)
    for index, item in enumerate(arr):
        if((item != newPenUp) and (arr[index+1] != newPenUp)):
            a, b = item[0], arr[index+1][0]
            c, d = item[1], arr[index+1][1]
            draw.line(([a, c, b, d]), color)
    for y in range(im.height-1):
        for x in range(im.width-1):
            a, b = str(im.getpixel((x, y))) == str(color), str(im.getpixel((x+1, y))) == str(color)
            c, d = str(im.getpixel((x, y+1))) == str(color), str(im.getpixel((x+1, y+1))) == str(color)
            arr = [[a, b], [c, d]]
            if(arr == [[1, 0], [0, 1]]):
                draw.point((x, y+1), color)
            if(arr == [[0, 1], [1, 0]]):
                draw.point((x, y), color)
    return im
def followMouse(x, y):
    turtle.Screen().onclick(None)
    turtle.penup()
    turtle.setpos(x, y)
    penPos.append(newPenUp)
    turtle.Screen().onclick(followMouse)
def followMouseDrag(x, y):
    turtle.ondrag(None)
    turtle.setpos(x, y)
    penPos.append([int(x), -int(y)])
    turtle.pd()
    turtle.ondrag(followMouseDrag)
def setImagePos(penPos, padding):
    minX = minY = 10000000
    maxX = maxY = -10000000
    for xy in penPos:
        if(str(xy) != newPenUp):
            x = xy[0]
            y = xy[1]
            minX = x if x <= minX else minX
            minY = y if y <= minY else minY
    for xy in penPos:
        if(str(xy) != newPenUp):
            xy[0] = xy[0]-minX+padding
            xy[1] = xy[1]-minY+padding
            x = xy[0]
            y = xy[1]
            maxY = y if y >= maxY else maxY
            maxX = x if x >= maxX else maxX
    maxX+=padding+padding
    maxY+=padding+padding
    return (maxX, maxY)
def makeImage(name, color1=(0, 255, 255), color2=(255, 0, 0), padding=50, bgcolor=(0, 0, 0)):
    imSize = setImagePos(penPos, padding)
    im = Image.new("RGB", imSize, bgcolor)
    im = drawStuff(im, penPos, color1)
    for x in range(250):
        im = ImageEnhance.Sharpness(im).enhance(10)
        im = ImageEnhance.Sharpness(im).enhance(-10)
    im = drawStuff(im, penPos, color2)
    basewidth = im.width*4
    wpercent = ((basewidth)/float(im.size[0]))
    hsize = int((float(im.size[1])*float(wpercent)))
    im.resize((basewidth, hsize)).show()
    im = ImageEnhance.Sharpness(im).enhance(10)
    im.resize((basewidth, hsize)).show()
    im.save(name)
draw()
makeImage("temp.png",(0, 255, 255),(0, 0, 255))
