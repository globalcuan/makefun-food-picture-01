"""A warm, steaming bowl of ramen in a flat illustration.
Golden noodles, rich broth, and rising steam make a freshly served scene."""
import math
import os
import struct
import zlib

W = H = 1600
pixels = bytearray(W * H * 3)


def paint_background():
    fill((0, 0, W, H), (54, 31, 39))
    fill((0, 280, W, 470), (62, 37, 43))
    fill((0, 540, W, 755), (67, 40, 44))
    fill((0, 770, W, H), (42, 27, 34))
    fill((0, 1240, W, H), (47, 29, 35))


def fill(box, color):
    x0, y0, x1, y1 = [int(v) for v in box]
    x0, x1 = max(0, x0), min(W, x1)
    y0, y1 = max(0, y0), min(H, y1)
    row = bytes(color) * max(0, x1 - x0)
    for y in range(y0, y1):
        p = (y * W + x0) * 3
        pixels[p:p + len(row)] = row


def ellipse(cx, cy, rx, ry, color):
    y0, y1 = max(0, int(cy - ry - 1)), min(H, int(cy + ry + 2))
    for y in range(y0, y1):
        dy = (y + .5 - cy) / ry
        if abs(dy) <= 1:
            dx = rx * math.sqrt(max(0, 1 - dy * dy))
            xa, xb = max(0, int(cx - dx)), min(W, int(cx + dx + 1))
            if xb > xa:
                p = (y * W + xa) * 3
                row = bytes(color) * (xb - xa)
                pixels[p:p + len(row)] = row


def polygon(points, color):
    ymin = max(0, int(min(y for x, y in points)))
    ymax = min(H, int(max(y for x, y in points)) + 1)
    for y in range(ymin, ymax):
        scan = y + .5
        xs = []
        for i, (x1, y1) in enumerate(points):
            x2, y2 = points[(i + 1) % len(points)]
            if (y1 <= scan < y2) or (y2 <= scan < y1):
                xs.append(x1 + (scan - y1) * (x2 - x1) / (y2 - y1))
        xs.sort()
        for a, b in zip(xs[::2], xs[1::2]):
            xa, xb = max(0, int(a)), min(W, int(b) + 1)
            if xb > xa:
                p = (y * W + xa) * 3
                pixels[p:p + (xb - xa) * 3] = bytes(color) * (xb - xa)


def stroke(points, color, width):
    r = width / 2
    for (x1, y1), (x2, y2) in zip(points, points[1:]):
        xmin, xmax = max(0, int(min(x1, x2) - r - 1)), min(W, int(max(x1, x2) + r + 2))
        ymin, ymax = max(0, int(min(y1, y2) - r - 1)), min(H, int(max(y1, y2) + r + 2))
        vx, vy = x2 - x1, y2 - y1
        den = vx * vx + vy * vy or 1
        for y in range(ymin, ymax):
            py = y + .5
            for x in range(xmin, xmax):
                px = x + .5
                t = max(0.0, min(1.0, ((px - x1) * vx + (py - y1) * vy) / den))
                dx, dy = px - (x1 + t * vx), py - (y1 + t * vy)
                if dx * dx + dy * dy <= r * r:
                    p = (y * W + x) * 3
                    pixels[p:p + 3] = bytes(color)
    for x, y in points:
        ellipse(x, y, r, r, color)


def curve(fn, x0, x1, steps=80):
    return [(x0 + (x1 - x0) * i / steps, fn(x0 + (x1 - x0) * i / steps)) for i in range(steps + 1)]


def arc(cx, cy, rx, ry, a0, a1, color, width):
    pts = []
    for i in range(81):
        a = a0 + (a1 - a0) * i / 80
        pts.append((cx + rx * math.cos(a), cy + ry * math.sin(a)))
    stroke(pts, color, width)


def draw():
    paint_background()
    # Back nori, leaning from the far side of the bowl.
    polygon([(515, 770), (755, 735), (790, 1000), (555, 1015)], (29, 76, 55))
    polygon([(545, 790), (736, 765), (754, 974), (574, 990)], (36, 91, 63))
    for i in range(9):
        stroke([(558 + i * 20, 812), (580 + i * 18, 965)], (46, 105, 72), 3)
    # Bowl shadow and curved trapezoid body.
    ellipse(800, 1243, 500, 72, (31, 23, 31))
    polygon([(395, 875), (1205, 875), (1125, 1250), (1030, 1330), (570, 1330), (475, 1250)], (139, 39, 47))
    polygon([(425, 900), (1175, 900), (1102, 1225), (1015, 1292), (585, 1292), (498, 1225)], (163, 45, 51))
    # Broad lacquer highlights and foot.
    arc(800, 980, 390, 320, 1.98, 2.62, (199, 72, 68), 17)
    arc(800, 1000, 375, 335, 2.08, 2.55, (212, 91, 78), 7)
    ellipse(800, 1318, 245, 35, (112, 32, 42))
    ellipse(800, 1307, 220, 22, (179, 54, 56))
    # Cream rim, then the broth visible within it.
    ellipse(800, 886, 415, 115, (236, 211, 169))
    ellipse(800, 883, 385, 91, (221, 130, 48))
    ellipse(800, 882, 366, 76, (238, 153, 55))
    arc(800, 883, 350, 63, 3.22, 5.95, (247, 178, 75), 8)
    # Broth swirl, broad soft gloss, and pale oil droplets.
    arc(775, 882, 172, 37, 3.45, 6.15, (255, 194, 93), 8)
    arc(950, 888, 94, 26, .25, 3.0, (255, 183, 76), 6)
    arc(712, 870, 218, 48, 3.48, 6.08, (250, 178, 77), 25)
    arc(712, 870, 218, 48, 3.58, 5.98, (255, 204, 110), 11)
    for x, y, rx, ry in [
        (620, 865, 13, 8), (700, 918, 9, 6), (850, 851, 12, 7),
        (1010, 870, 14, 8), (930, 915, 8, 5), (765, 858, 7, 5),
        (1080, 900, 9, 6), (570, 887, 10, 6), (660, 845, 8, 5),
        (790, 925, 11, 6), (890, 870, 7, 5), (1040, 846, 9, 6),
        (735, 875, 6, 4), (975, 895, 10, 6), (1110, 872, 7, 5),
    ]:
        ellipse(x, y, rx, ry, (255, 217, 145))
    # Dense overlapping noodle layers spread over nearly the entire broth.
    for j in range(34):
        base = 807 + j * 4.2
        half_width = 335 * math.sqrt(max(.05, 1 - ((base - 883) / 74) ** 2))
        left = 800 - half_width + 7
        right = 800 + half_width - 7
        pts = []
        for k in range(121):
            x = left + (right - left) * k / 120
            phase = j * .57
            y = base + 12 * math.sin((x - left) / 24 + phase) + 4 * math.sin((x - left) / 10.5 + j)
            pts.append((x, y))
        stroke(pts, (255, 216, 133) if j % 3 else (247, 196, 103), 8)
    # Tiny pale sesame sprinkle scattered over the noodles.
    sesame = [
        (566, 850), (590, 879), (608, 913), (632, 838), (650, 891),
        (673, 859), (690, 926), (712, 883), (728, 819), (751, 906),
        (773, 864), (790, 937), (808, 844), (825, 892), (846, 916),
        (865, 857), (882, 934), (903, 879), (921, 834), (940, 910),
        (958, 862), (980, 928), (998, 889), (1017, 841), (1034, 913),
        (1053, 872), (1070, 899), (1091, 852), (1110, 887), (637, 925),
        (700, 838), (760, 881), (839, 831), (916, 921), (1000, 858),
    ]
    for i, (x, y) in enumerate(sesame):
        ellipse(x, y, 2 + i % 2, 2, (255, 236, 190))
    # Chashu slices with spiral centers.
    for cx, cy in [(640, 827), (990, 822)]:
        ellipse(cx, cy, 70, 48, (191, 119, 103))
        ellipse(cx, cy, 58, 38, (218, 155, 128))
        arc(cx, cy, 29, 20, -.4, 5.2, (149, 77, 73), 7)
        ellipse(cx - 5, cy - 2, 9, 7, (159, 81, 72))
    # Halved eggs with white and amber yolks.
    for cx, cy in [(735, 848), (890, 831)]:
        ellipse(cx, cy, 53, 40, (250, 239, 211))
        ellipse(cx, cy, 24, 23, (244, 165, 55))
        ellipse(cx - 5, cy - 6, 8, 7, (255, 207, 90))
    # Lifted noodle bundle looping from the chopstick tips.
    for j in range(8):
        xbase = 1032 + j * 11
        pts = []
        for k in range(101):
            t = k / 100
            x = xbase - 125 * t + 29 * math.sin(t * 2 * math.pi + j * .43)
            y = 493 + 310 * t + 11 * math.sin(t * 4 * math.pi + j * .55)
            pts.append((x, y))
        stroke(pts, (255, 218, 142) if j % 2 else (246, 194, 104), 8)
    # Chopsticks, tapered warm wood, entering from upper right.
    polygon([(1194, 250), (1216, 246), (976, 847), (959, 840)], (133, 77, 46))
    polygon([(1232, 265), (1251, 277), (1000, 862), (982, 852)], (164, 97, 54))
    stroke([(1201, 264), (974, 837)], (195, 126, 73), 4)
    # Scattered green onion rings.
    for cx, cy, r in [(770,790,13),(815,799,11),(860,786,14),(905,801,10),(740,810,9),(830,825,12),(950,798,11),(785,837,9),(925,843,13),(875,818,8),(690,795,8)]:
        ellipse(cx, cy, r, r, (57, 151, 70))
        ellipse(cx, cy, r * .48, r * .48, (238, 213, 141))
    # Pale bean sprouts.
    for x, y, bend in [(710,780,26),(735,774,-22),(900,775,20),(930,782,-18),(820,775,23),(975,786,-25)]:
        stroke([(x, y+25), (x+bend*.5, y+8), (x+bend, y-13)], (247, 232, 195), 7)
        ellipse(x+bend, y-13, 5, 5, (255, 241, 205))
    # Three soft, pale steam ribbons; layered strokes give gentle rounded edges.
    for cx, top, bottom, phase in [(655, 210, 670, 0.0), (806, 155, 675, 1.5), (958, 225, 670, 3.0)]:
        pts = []
        for i in range(101):
            t = i / 100
            y = bottom - (bottom-top)*t
            x = cx + 32*math.sin(t*2*math.pi + phase) + 8*math.sin(t*4*math.pi + phase*.5)
            pts.append((x, y))
        stroke(pts, (151, 137, 130), 27)
        stroke(pts, (190, 178, 164), 15)


def png_bytes(rgb, width, height):
    def chunk(kind, data):
        body = kind + data
        return struct.pack('>I', len(data)) + body + struct.pack('>I', zlib.crc32(body) & 0xffffffff)
    raw = bytearray()
    stride = width * 3
    for y in range(height):
        raw.append(0)
        raw.extend(rgb[y * stride:(y + 1) * stride])
    return (b'\x89PNG\r\n\x1a\n' +
            chunk(b'IHDR', struct.pack('>IIBBBBB', width, height, 8, 2, 0, 0, 0)) +
            chunk(b'IDAT', zlib.compress(bytes(raw), 9)) + chunk(b'IEND', b''))


def downsample():
    out = bytearray(800 * 800 * 3)
    for y in range(800):
        sy = y * 2
        for x in range(800):
            si = (sy * W + x * 2) * 3
            di = (y * 800 + x) * 3
            for c in range(3):
                out[di+c] = (pixels[si+c] + pixels[si+3+c] + pixels[si+W*3+c] + pixels[si+W*3+3+c] + 2) // 4
    return out


def main():
    draw()
    folder = os.environ.get('MAKEFUN_OUTPUT_DIR', '/output')
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, 'entry.png')
    with open(path, 'wb') as f:
        f.write(png_bytes(downsample(), 800, 800))


if __name__ == '__main__':
    main()
