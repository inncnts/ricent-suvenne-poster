import math
import os
import struct
import zlib

W = H = 1024
pixels = bytearray(W * H * 3)


def put(x, y, c):
    if 0 <= x < W and 0 <= y < H:
        i = (y * W + x) * 3
        pixels[i:i + 3] = bytes(c)


def rect(x0, y0, x1, y1, c):
    x0, x1 = max(0, x0), min(W, x1)
    y0, y1 = max(0, y0), min(H, y1)
    for y in range(y0, y1):
        row = (y * W + x0) * 3
        pixels[row:row + (x1 - x0) * 3] = bytes(c) * (x1 - x0)


def ellipse(cx, cy, rx, ry, c):
    for y in range(max(0, cy - ry), min(H, cy + ry)):
        for x in range(max(0, cx - rx), min(W, cx + rx)):
            if ((x-cx)/rx)**2 + ((y-cy)/ry)**2 <= 1:
                put(x, y, c)


def poly(points, c):
    ys = [p[1] for p in points]
    for y in range(max(0, min(ys)), min(H, max(ys) + 1)):
        xs = []
        for i in range(len(points)):
            x1, y1 = points[i]
            x2, y2 = points[(i + 1) % len(points)]
            if (y1 <= y < y2) or (y2 <= y < y1):
                xs.append(int(x1 + (y-y1)*(x2-x1)/(y2-y1)))
        if len(xs) >= 2:
            xs.sort()
            for i in range(0, len(xs), 2):
                if i + 1 < len(xs):
                    rect(xs[i], y, xs[i+1]+1, y+1, c)


def line(x0, y0, x1, y1, c, width=2):
    dx, dy = abs(x1-x0), abs(y1-y0)
    sx, sy = (1 if x0 < x1 else -1), (1 if y0 < y1 else -1)
    err = dx-dy
    while True:
        ellipse(x0, y0, width, width, c)
        if x0 == x1 and y0 == y1:
            break
        e2 = 2*err
        if e2 > -dy:
            err -= dy
            x0 += sx
        if e2 < dx:
            err += dx
            y0 += sy


# Atmospheric sky
for y in range(H):
    if y < 470:
        t = y/470
        c = (int(77+178*t), int(130+82*t), int(174+28*t))
    else:
        t = (y-470)/554
        c = (int(233-35*t), int(184-23*t), int(130-48*t))
    rect(0, y, W, y+1, c)

# Sun and clouds
ellipse(820, 150, 78, 78, (255, 235, 146))
for cx, cy, rx in [(150, 145, 58), (215, 130, 38), (690, 105, 48)]:
    ellipse(cx, cy, rx, 18, (255, 229, 190))

# Sea and distant islands
rect(0, 470, W, 650, (89, 149, 158))
poly([(0,510),(130,458),(230,500),(350,430),(470,490),(610,438),(760,502),(900,460),(1024,490),(1024,650),(0,650)], (61,96,105))
for y in range(500, 650, 16):
    rect(0, y, W, y+2, (235, 199, 145))

# Ring eclipse monument
ellipse(735, 330, 230, 230, (91,86,78))
ellipse(735, 330, 188, 188, (246,213,151))
ellipse(735, 330, 145, 145, (66,94,103))
ellipse(735, 330, 96, 96, (239,195,112))

# Old cliff town
poly([(0,620),(0,510),(90,500),(150,540),(230,470),(310,530),(390,500),(470,550),(530,620)], (194,142,98))
colors = [(224,190,145),(238,213,168),(185,137,96),(219,164,117)]
for i in range(11):
    x = 20+i*72
    base = 610-random0 if False else 620
    bw = 48
    bh = 58+(i*37)%90
    rect(x, base-bh, x+bw, base, colors[i%4])
    poly([(x-4,base-bh),(x+bw+4,base-bh),(x+bw//2,base-bh-24)], (107,91,74))
    rect(x+10, base-bh+20, x+18, base-bh+34, (83,102,105))
    rect(x+31, base-bh+20, x+39, base-bh+34, (83,102,105))

# Clock tower
rect(465, 395, 525, 640, (223,193,143))
poly([(465,395),(495,340),(525,395)], (105,86,70))
ellipse(495, 450, 20, 20, (74,92,94))
line(495,450,495,438,(242,214,162),2)
line(495,450,506,456,(242,214,162),2)

# Grand plaza
poly([(0,620),(1024,620),(1024,1024),(0,1024)], (217,180,122))
for i in range(12):
    y = 630+i*i*5
    line(0,y,1024,y,(137,112,78),1)
for x in range(-300,1300,110):
    line(512,620,x,1024,(137,112,78),1)

# Central stairs
poly([(420,1024),(604,1024),(680,620),(344,620)], (236,207,156))
for y in range(660,1024,24):
    t=(y-660)/364
    half=int(168-80*t)
    line(512-half,y,512+half,y,(127,108,80),2)

# Obelisk
poly([(508,650),(528,650),(527,430),(514,430)], (83,89,84))
poly([(514,430),(527,430),(520,398)], (224,186,119))

# Cypress trees
for x in (92,140,330,790,860,930):
    ellipse(x, 560+(x%40), 13, 76, (61,92,72))

# Bougainvillea
for cx, cy in [(145,540),(195,570),(690,560),(775,540),(930,580),(60,620)]:
    for k in range(24):
        a=(k*137.5)*math.pi/180
        r=(k*29)%55
        ellipse(int(cx+math.cos(a)*r), int(cy+math.sin(a)*r*.65), 5, 5,
                (190+(k%4)*10,55+(k%3)*12,85+(k%5)*8))

# Figures and cafe tables
def person(x,y,shirt):
    ellipse(x,y-12,8,8,(91,65,49))
    rect(x-10,y-4,x+10,y+42,shirt)
    line(x-14,y+42,x+14,y+42,(76,66,58),5)

person(225,760,(78,132,152))
person(300,790,(224,174,82))
person(850,770,(159,84,94))
for cx, cy in [(180,850),(330,870),(910,840)]:
    ellipse(cx,cy,38,7,(96,76,58))
    line(cx,cy,cx,cy+48,(96,76,58),4)
    ellipse(cx-30,cy+42,18,8,(96,76,58))
    ellipse(cx+30,cy+42,18,8,(96,76,58))

# Birds
for bx, by in [(110,300),(150,290),(850,330),(890,318)]:
    line(bx-16,by,bx-5,by-7,(63,75,82),2)
    line(bx-5,by-7,bx+8,by,(63,75,82),2)
    line(bx+8,by,bx+20,by-7,(63,75,82),2)

# Vintage border and subtitle
rect(20,20,1004,24,(250,230,184))
rect(20,1000,1004,1004,(250,230,184))
rect(20,20,24,1004,(250,230,184))
rect(1000,20,1004,1004,(250,230,184))

# 5x7 bitmap title
font = {
    "A":["10001","11011","10101","10101","11111","10101","10101"],
    "U":["10001","10001","10001","10001","10001","10001","01110"],
    "R":["11110","10001","10001","11110","10100","10010","10001"],
    "E":["11111","10000","10000","11110","10000","10000","11111"],
    "L":["10000","10000","10000","10000","10000","10000","11111"],
    "N":["10001","11001","11001","10101","10011","10011","10001"],
}
title="AURELUNE"
sx, sy, scale = 54, 78, 7
for ci,ch in enumerate(title):
    ox=sx+ci*43*scale//7
    for ry,row in enumerate(font[ch]):
        for rx,v in enumerate(row):
            if v=="1":
                rect(ox+rx*scale,sy+ry*scale,ox+(rx+1)*scale,sy+(ry+1)*scale,(250,239,198))

# Footer
rect(36,944,988,996,(225,194,137))
for y in range(956,984,14):
    line(46,y,978,y,(180,145,94),1)

os.makedirs("/output", exist_ok=True)
raw = bytearray()
for y in range(H):
    raw.append(0)
    raw += pixels[y*W*3:(y+1)*W*3]


def chunk(kind, data):
    return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data) & 0xffffffff)


png = b"\x89PNG\r\n\x1a\n"
png += chunk(b"IHDR", struct.pack(">IIBBBBB", W, H, 8, 2, 0, 0, 0))
png += chunk(b"IDAT", zlib.compress(bytes(raw), 9))
png += chunk(b"IEND", b"")
with open("/output/entry.png", "wb") as f:
    f.write(png)
