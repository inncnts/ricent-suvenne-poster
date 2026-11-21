from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math
import os
import random

random.seed(21)
W = H = 1024

def font(size, serif=True, bold=False):
    candidates = [
        r"C:\Windows\Fonts\georgia.ttf",
        r"C:\Windows\Fonts\segoeui.ttf",
    ] if serif else [
        r"C:\Windows\Fonts\seguisb.ttf",
        r"C:\Windows\Fonts\segoeui.ttf",
    ]
    for path in candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                pass
    return ImageFont.load_default()

img = Image.new("RGB", (W, H), "#f3dca5")
p = img.load()
for y in range(H):
    t = y / H
    if y < 430:
        c1 = (96, 145, 183)
        c2 = (238, 184, 128)
    else:
        c1 = (228, 168, 108)
        c2 = (248, 220, 164)
    local = max(0, min(1, (t - 0.05) / 0.75))
    p[0, y] = tuple(int(c1[i] * (1-local) + c2[i] * local) for i in range(3))
    for x in range(1, W):
        p[x, y] = p[0, y]

d = ImageDraw.Draw(img, "RGBA")

# Sun and soft clouds
d.ellipse((760, 64, 914, 218), fill=(255, 238, 157, 220))
for cx, cy, r in [(160, 130, 55), (230, 115, 38), (675, 92, 43), (730, 105, 30)]:
    d.ellipse((cx-r, cy-r//2, cx+r, cy+r//2), fill=(255, 223, 181, 95))

# Far islands and sea
d.polygon([(0, 430), (0, 510), (96, 460), (170, 490), (230, 426), (310, 470),
           (390, 435), (465, 485), (560, 420), (650, 468), (750, 415),
           (850, 462), (1024, 402), (1024, 535), (0, 535)], fill=(55, 93, 108, 180))
d.polygon([(0, 470), (1024, 470), (1024, 650), (0, 650)], fill=(87, 145, 153, 150))
for y in range(482, 650, 18):
    alpha = 100 + (y-482)//3
    d.line((0, y, 1024, y), fill=(242, 214, 158, alpha), width=2)

# A huge fictional eclipse gate
d.ellipse((565, 118, 966, 519), fill=(84, 76, 72, 150))
d.ellipse((604, 157, 927, 480), fill=(244, 211, 149, 255))
d.ellipse((650, 203, 881, 434), fill=(70, 92, 96, 255))
d.ellipse((677, 230, 854, 407), fill=(235, 191, 111, 255))
for i in range(18):
    a = i * math.pi * 2 / 18
    x = 766 + math.cos(a)*158
    y = 319 + math.sin(a)*158
    d.ellipse((x-4, y-4, x+4, y+4), fill=(250, 218, 158, 240))

# Cliffside old town
d.polygon([(0, 520), (155, 485), (250, 525), (350, 470), (470, 520), (530, 610),
           (0, 650)], fill=(193, 134, 88, 255))
for i in range(12):
    x = 20 + i*38
    y = 520 + random.randint(-18, 20)
    w = random.randint(28, 48)
    h = random.randint(55, 120)
    d.rectangle((x, y-h, x+w, y+h//2), fill=random.choice([
        (218, 183, 133, 255), (238, 210, 161, 255),
        (187, 137, 95, 255), (226, 163, 112, 255)
    ]), outline=(130, 99, 75, 180), width=2)
    if i % 3 == 0:
        d.polygon([(x-5,y-h),(x+w+5,y-h),(x+w//2,y-h-24)], fill=(104,95,82,255))
    for xx in range(x+8, x+w-4, 14):
        d.rectangle((xx, y-h+18, xx+7, y-h+31), fill=(75,89,92,220))

# Clock tower
d.polygon([(450, 640), (470, 390), (520, 390), (540, 640)], fill=(223, 192, 143,255))
d.polygon([(470,390),(495,340),(520,390)], fill=(112,82,63,255))
d.rectangle((487,410,508,438), fill=(238,207,145,255), outline=(79,88,82,255), width=3)
d.ellipse((480,448,516,484), fill=(78,99,99,255))
d.line((498,466,498,452), fill=(242,213,160,255), width=3)
d.line((498,466,512,470), fill=(242,213,160,255), width=2)

# Grand plaza foreground
d.polygon([(0, 650), (1024, 650), (1024,1024), (0,1024)], fill=(211,172,116,255))
for i in range(16):
    y = 650 + i*i*2
    d.line((0,y,1024,y), fill=(133,112,79,50), width=2)
for x in range(-300,1300,110):
    d.line((512,650,x,1024), fill=(133,112,79,45), width=2)

# Central stairway
d.polygon([(430,1024),(594,1024),(667,650),(357,650)], fill=(230,205,155,255))
for y in range(690,1024,24):
    t=(y-690)/(1024-690)
    half=155-80*t
    d.line((512-half,y,512+half,y), fill=(126,107,80,110), width=3)

# Monument obelisk
d.polygon([(508, 645),(528,645),(527,430),(514,430)], fill=(91,94,86,255))
d.polygon([(514,430),(527,430),(520,400)], fill=(226,189,122,255))
d.ellipse((502,630,534,662), fill=(91,94,86,255))

# Cypress silhouettes
for x in (88, 128, 334, 742, 817, 890):
    h=random.randint(100,180)
    base=random.randint(590,640)
    d.ellipse((x-16,base-h//2,x+16,base+15), fill=(63,91,74,255))
    d.line((x,base,x,base-h), fill=(54,80,64,255), width=5)

# Bougainvillea
for cx,cy in [(160,535),(190,570),(760,510),(930,570),(690,585),(86,610)]:
    for k in range(38):
        ang=random.random()*math.pi*2
        rr=random.randint(8,48)
        x=cx+math.cos(ang)*rr
        y=cy+math.sin(ang)*rr*.7
        color=random.choice([(191,60,82,220),(226,92,94,230),(160,48,78,210),(244,132,126,210)])
        d.ellipse((x-5,y-5,x+5,y+5), fill=color)

# Travelers and cafe tables
def person(x,y,shirt):
    d.ellipse((x-8,y-18,x+8,y-2), fill=(94,64,50,255))
    d.polygon([(x-12,y-2),(x+12,y-2),(x+20,y+54),(x-18,y+54)], fill=shirt)
    d.ellipse((x-18,y+48,x+18,y+56), fill=(73,67,58,255))

person(230,735,(77,132,151,255))
person(300,775,(231,181,92,255))
person(850,750,(156,82,93,255))
for cx,cy in [(180,820),(332,840),(910,812)]:
    d.ellipse((cx-34,cy,cx+34,cy+10), fill=(92,76,58,255))
    d.ellipse((cx-42,cy+10,cx-8,cy+48), fill=(111,83,67,255))
    d.ellipse((cx+8,cy+10,cx+42,cy+48), fill=(111,83,67,255))
    d.rectangle((cx-3,cy+8,cx+3,cy+52), fill=(92,76,58,255))

# Birds
for bx,by in [(104,310),(132,300),(830,320),(862,308)]:
    d.arc((bx-18,by-8,bx,by+8),190,350,fill=(66,75,82,220),width=3)
    d.arc((bx,by-8,bx+18,by+8),190,350,fill=(66,75,82,220),width=3)

# Film grain and print texture
noise = Image.effect_noise((W,H),18).convert("L")
grain = Image.merge("RGB",(noise,noise,noise)).filter(ImageFilter.GaussianBlur(.35))
img = Image.blend(img, grain, 0.035)
d = ImageDraw.Draw(img, "RGBA")

# Poster typography
title_font = font(82, serif=True)
small_font = font(22, serif=False)
label_font = font(19, serif=False)

d.text((54, 48), "THE AZURE /ISLANDS", font=label_font, fill=(247,235,205,255))
d.text((54, 88), "AURELUNE", font=title_font, fill=(250,239,198,255), stroke_width=1, stroke_fill=(87,91,82,150))
d.text((58, 174), "WHERE THE TIDES REMEMBER THE MOON", font=label_font, fill=(250,239,198,255))
d.text((60, 944), "34° 18′ N  ·  THE PLACE THAT ONLY EXISTS AT SUNSET", font=small_font, fill=(91,78,62,255))

# Vintage border
d.rectangle((22,22,1002,1002),outline=(250,229,184,220),width=3)
d.rectangle((32,32,992,992),outline=(109,92,68,150),width=1)

os.makedirs("/output", exist_ok=True)
img.save("/output/entry.png", optimize=True)
