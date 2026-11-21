#!/usr/bin/env python3
"""Render the front page of THE WORLD, Saturday 21 November 2026.

Pure Python 3.13 standard library only. Draws the page into an RGB
buffer with a built-in 5x7 bitmap font and encodes a deterministic PNG
(zlib level 9, no ancillary chunks, no timestamps) to poster.png.
"""
import struct
import zlib

W, H = 1024, 1024
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 20, 20)
DARKRED = (160, 10, 10)
GREY = (90, 90, 90)
LIGHTGREY = (200, 200, 200)

# ---------------------------------------------------------------- font ----
# 5x7 bitmap font. Each glyph: 7 rows of 5 characters, '#' = ink.
FONT = {
'A': [".###.", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"],
'B': ["####.", "#...#", "#...#", "####.", "#...#", "#...#", "####."],
'C': [".####", "#....", "#....", "#....", "#....", "#....", ".####"],
'D': ["####.", "#...#", "#...#", "#...#", "#...#", "#...#", "####."],
'E': ["#####", "#....", "#....", "####.", "#....", "#....", "#####"],
'F': ["#####", "#....", "#....", "####.", "#....", "#....", "#...."],
'G': [".####", "#....", "#....", "#.###", "#...#", "#...#", ".###."],
'H': ["#...#", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"],
'I': ["#####", "..#..", "..#..", "..#..", "..#..", "..#..", "#####"],
'J': ["..###", "...#.", "...#.", "...#.", "...#.", "#..#.", ".##.."],
'K': ["#...#", "#..#.", "#.#..", "##...", "#.#..", "#..#.", "#...#"],
'L': ["#....", "#....", "#....", "#....", "#....", "#....", "#####"],
'M': ["#...#", "##.##", "#.#.#", "#.#.#", "#...#", "#...#", "#...#"],
'N': ["#...#", "##..#", "##..#", "#.#.#", "#..##", "#..##", "#...#"],
'O': [".###.", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."],
'P': ["####.", "#...#", "#...#", "####.", "#....", "#....", "#...."],
'Q': [".###.", "#...#", "#...#", "#...#", "#.#.#", "#..#.", ".##.#"],
'R': ["####.", "#...#", "#...#", "####.", "#.#..", "#..#.", "#...#"],
'S': [".####", "#....", "#....", ".###.", "....#", "....#", "####."],
'T': ["#####", "..#..", "..#..", "..#..", "..#..", "..#..", "..#.."],
'U': ["#...#", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."],
'V': ["#...#", "#...#", "#...#", "#...#", "#...#", ".#.#.", "..#.."],
'W': ["#...#", "#...#", "#...#", "#.#.#", "#.#.#", "##.##", "#...#"],
'X': ["#...#", "#...#", ".#.#.", "..#..", ".#.#.", "#...#", "#...#"],
'Y': ["#...#", "#...#", ".#.#.", "..#..", "..#..", "..#..", "..#.."],
'Z': ["#####", "....#", "...#.", "..#..", ".#...", "#....", "#####"],
'0': [".###.", "#..##", "#.#.#", "##..#", "#...#", "#...#", ".###."],
'1': ["..#..", ".##..", "..#..", "..#..", "..#..", "..#..", ".###."],
'2': [".###.", "#...#", "....#", "...#.", "..#..", ".#...", "#####"],
'3': ["####.", "....#", "....#", ".###.", "....#", "....#", "####."],
'4': ["...#.", "..##.", ".#.#.", "#..#.", "#####", "...#.", "...#."],
'5': ["#####", "#....", "####.", "....#", "....#", "#...#", ".###."],
'6': [".###.", "#....", "#....", "####.", "#...#", "#...#", ".###."],
'7': ["#####", "....#", "...#.", "...#.", "..#..", "..#..", "..#.."],
'8': [".###.", "#...#", "#...#", ".###.", "#...#", "#...#", ".###."],
'9': [".###.", "#...#", "#...#", ".####", "....#", "....#", ".###."],
'a': [".....", ".....", ".###.", "....#", ".####", "#...#", ".####"],
'b': ["#....", "#....", "####.", "#...#", "#...#", "#...#", "####."],
'c': [".....", ".....", ".####", "#....", "#....", "#....", ".####"],
'd': ["....#", "....#", ".####", "#...#", "#...#", "#...#", ".####"],
'e': [".....", ".....", ".###.", "#...#", "#####", "#....", ".###."],
'f': ["..##.", ".#..#", ".#...", "###..", ".#...", ".#...", ".#..."],
'g': [".....", ".....", ".####", "#...#", "#...#", ".####", "....#", ".###."][:7],
'h': ["#....", "#....", "####.", "#...#", "#...#", "#...#", "#...#"],
'i': ["..#..", ".....", ".##..", "..#..", "..#..", "..#..", ".###."],
'j': ["...#.", ".....", "..##.", "...#.", "...#.", "...#.", "...#.", "##..."][:7],
'k': ["#....", "#....", "#..#.", "#.#..", "##...", "#.#..", "#..#."],
'l': [".##..", "..#..", "..#..", "..#..", "..#..", "..#..", ".###."],
'm': [".....", ".....", "##.#.", "#.#.#", "#.#.#", "#.#.#", "#.#.#"],
'n': [".....", ".....", "####.", "#...#", "#...#", "#...#", "#...#"],
'o': [".....", ".....", ".###.", "#...#", "#...#", "#...#", ".###."],
'p': [".....", ".....", "####.", "#...#", "#...#", "####.", "#...."],
'q': [".....", ".....", ".####", "#...#", "#...#", ".####", "....#"],
'r': [".....", ".....", "#.##.", "##..#", "#....", "#....", "#...."],
's': [".....", ".....", ".####", "#....", ".###.", "....#", "####."],
't': [".#...", ".#...", "###..", ".#...", ".#...", ".#...", "..##."],
'u': [".....", ".....", "#...#", "#...#", "#...#", "#..##", ".##.#"],
'v': [".....", ".....", "#...#", "#...#", "#...#", ".#.#.", "..#.."],
'w': [".....", ".....", "#...#", "#.#.#", "#.#.#", "#.#.#", ".#.#."],
'x': [".....", ".....", "#...#", ".#.#.", "..#..", ".#.#.", "#...#"],
'y': [".....", ".....", "#...#", "#...#", "#...#", ".####", "....#"],
'z': [".....", ".....", "#####", "...#.", "..#..", ".#...", "#####"],
' ': [".....", ".....", ".....", ".....", ".....", ".....", "....."],
'.': [".....", ".....", ".....", ".....", ".....", ".##..", ".##.."],
',': [".....", ".....", ".....", ".....", ".##..", ".##..", ".#..."],
':': [".....", ".##..", ".##..", ".....", ".##..", ".##..", "....."],
';': [".....", ".##..", ".##..", ".....", ".##..", ".##..", ".#..."],
'!': ["..#..", "..#..", "..#..", "..#..", "..#..", ".....", "..#.."],
'?': [".###.", "#...#", "....#", "...#.", "..#..", ".....", "..#.."],
'-': [".....", ".....", ".....", ".###.", ".....", ".....", "....."],
'\u2013': [".....", ".....", ".....", "#####", ".....", ".....", "....."],
'\u2014': [".....", ".....", ".....", "#####", ".....", ".....", "....."],
'"': [".#.#.", ".#.#.", ".#.#.", ".....", ".....", ".....", "....."],
"'": ["..#..", "..#..", ".#...", ".....", ".....", ".....", "....."],
'\u2019': ["..#..", "..#..", ".#...", ".....", ".....", ".....", "....."],
'(': ["...#.", "..#..", ".#...", ".#...", ".#...", "..#..", "...#."],
')': [".#...", "..#..", "...#.", "...#.", "...#.", "..#..", ".#..."],
'%': ["##..#", "##.#.", "...#.", "..#..", ".#...", "#.##.", "#..##"],
'$': ["..#..", ".####", "#.#..", ".###.", "..#.#", "####.", "..#.."],
'&': [".##..", "#..#.", "#..#.", ".#...", "#.#.#", "#..#.", ".##.#"],
'/': ["....#", "....#", "...#.", "..#..", ".#...", "#....", "#...."],
'+': [".....", "..#..", "..#..", "#####", "..#..", "..#..", "....."],
'=': [".....", ".....", "#####", ".....", "#####", ".....", "....."],
'*': [".....", "#...#", ".#.#.", "..#..", ".#.#.", "#...#", "....."],
'#': [".#.#.", ".#.#.", "#####", ".#.#.", "#####", ".#.#.", ".#.#."],
'@': [".###.", "#...#", "#.###", "#.#.#", "#.###", "#....", ".###."],
'_': [".....", ".....", ".....", ".....", ".....", ".....", "#####"],
'[': [".###.", ".#...", ".#...", ".#...", ".#...", ".#...", ".###."],
']': [".###.", "...#.", "...#.", "...#.", "...#.", "...#.", ".###."],
'<': ["...#.", "..#..", ".#...", "#....", ".#...", "..#..", "...#."],
'>': [".#...", "..#..", "...#.", "....#", "...#.", "..#..", ".#..."],
'\\': ["#....", "#....", ".#...", "..#..", "...#.", "....#", "....#"],
'|': ["..#..", "..#..", "..#..", "..#..", "..#..", "..#..", "..#.."],
'~': [".....", ".....", ".##.#", "#.#..", ".....", ".....", "....."],
'^': ["..#..", ".#.#.", ".....", ".....", ".....", ".....", "....."],
'`': ["..#..", "..#..", ".#...", ".....", ".....", ".....", "....."],
}
BLANK = ["....."] * 7

# Fix the two glyphs that were sliced above (kept at 7 rows explicitly).
FONT['g'] = [".....", ".....", ".####", "#...#", "#...#", ".####", "....#"]
FONT['j'] = ["...#.", ".....", "..##.", "...#.", "...#.", "...#.", "##..."]


# -------------------------------------------------------------- canvas ----
class Canvas:
    def __init__(self, w, h, bg=WHITE):
        self.w, self.h = w, h
        self.px = bytearray(bg * (w * h))

    def set(self, x, y, color):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i], self.px[i + 1], self.px[i + 2] = color

    def rect(self, x, y, w, h, color):
        for yy in range(y, y + h):
            for xx in range(x, x + w):
                self.set(xx, yy, color)

    def line(self, x0, y0, x1, y1, color):
        dx, dy = abs(x1 - x0), abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy
        while True:
            self.set(x0, y0, color)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy

    def disc(self, cx, cy, r, color):
        for yy in range(cy - r, cy + r + 1):
            for xx in range(cx - r, cx + r + 1):
                if (xx - cx) ** 2 + (yy - cy) ** 2 <= r * r:
                    self.set(xx, yy, color)

    def text(self, x, y, s, scale, color):
        """Draw text left-aligned at (x, y); returns pixel width used."""
        cx = x
        for ch in s:
            glyph = FONT.get(ch, BLANK)
            for row in range(7):
                bits = glyph[row]
                for col in range(5):
                    if bits[col] == '#':
                        self.rect(cx + col * scale, y + row * scale,
                                  scale, scale, color)
            cx += 6 * scale
        return cx - x - scale if s else 0


def text_width(s, scale):
    return len(s) * 6 * scale - scale if s else 0


def wrap(text, max_w, scale):
    """Greedy word wrap; returns list of lines, each fitting max_w px."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = word if not cur else cur + " " + word
        if text_width(trial, scale) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


# ------------------------------------------------------------ png encode ---
def png_bytes(cv):
    def chunk(tag, data):
        c = struct.pack(">I", len(data)) + tag + data
        return c + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)

    ihdr = struct.pack(">IIBBBBB", cv.w, cv.h, 8, 2, 0, 0, 0)
    raw = bytearray()
    stride = cv.w * 3
    for y in range(cv.h):
        raw.append(0)
        raw += cv.px[y * stride:(y + 1) * stride]
    idat = zlib.compress(bytes(raw), 9)
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr)
            + chunk(b"IDAT", idat) + chunk(b"IEND", b""))


# --------------------------------------------------------------- content ---
LEAD_HEAD = "RUSSIA'S BIGGEST STRIKE HITS KYIV \u2014 AND LANDS IN POLAND"
LEAD_BODY = ("Russia fired more than 400 drones and 110 missiles at Ukraine "
             "overnight; at least eight killed in Kyiv; bridges and railway "
             "stations damaged; two Russian missiles and a suspected drone "
             "came down in Poland; Polish PM Tusk calls it a deliberate "
             "provocation.")

STORIES = [
    ("MARKETS", "AI ROUT DRAGS MARKETS INTO CORRECTION",
     "US stocks plunged Friday as an AI and chip sell-off pushed the S&P 500 "
     "down 3.7% into correction; Nasdaq fell 5.28%, erasing its 2026 gains; "
     "Nikkei down 5.06%."),
    ("CLIMATE", "CLIMATE TALKS RUN PAST DEADLINE",
     "COP31 in Antalya, Turkey, in overtime as nearly 200 nations fail to "
     "agree on fossil fuels."),
    ("TECH", "FBI DATABASE HACKED AS US OUTAGES SPREAD",
     "FBI criminal database reportedly hacked; US computer outages continue."),
    ("HEALTH", "PILL MAKES PANCREATIC TUMOURS VANISH IN TRIAL",
     "Trial pill daraxonrasib made tumours undetectable on scans in one in "
     "12 patients."),
    ("WORLD", "UK AND EU SIGN BIGGEST POST-BREXIT DEAL",
     "Three agreements in Brussels on food exports, carbon markets and youth "
     "mobility."),
    ("WORLD", "GEN Z PROTESTS SPREAD ACROSS 25 COUNTRIES",
     "Youth-led protests across Europe."),
    ("WORLD", "QUAKE OF 6.9 SHAKES PERUVIAN ANDES",
     "Magnitude 6.9 earthquake in the Andes of Peru."),
    ("WORLD", "TRUMP WEIGHS NEW STRIKES ON IRAN",
     "President Trump weighing another round of extensive strikes on Iran as "
     "Israel presses for action."),
    ("WORLD", "PALISADES FIRE ARSONIST CONVICTED",
     "Man convicted of starting the deadly Palisades fire in Los Angeles."),
]

MARKETS = ("S&P 500 6,910.39 -3.70% | Nasdaq 22,617.73 -5.28% | Nikkei "
           "56,436.65 -5.06% | FTSE 100 10,346.34 -1.02% | DAX 24,802.78 "
           "-2.60% | Brent $89.95 -2.21% | Gold $3,515.4 -4.62% | Bitcoin "
           "falls toward $62K as crypto liquidations top $2B.")


def draw_page(cv):
    M = 32                      # margin
    CW = W - 2 * M              # 960 content width

    # --- masthead ------------------------------------------------------
    cv.rect(0, 0, W, 80, BLACK)
    title = "THE WORLD"
    cv.text((W - text_width(title, 6)) // 2, 19, title, 6, WHITE)
    cv.rect(0, 80, W, 4, RED)

    # --- date line -----------------------------------------------------
    date = "SATURDAY, 21 NOVEMBER 2026"
    cv.text((W - text_width(date, 2)) // 2, 94, date, 2, BLACK)
    cv.text(M, 99, "EST. 2026", 1, GREY)
    price = "PRICE $2.00"
    cv.text(W - M - text_width(price, 1), 99, price, 1, GREY)
    cv.rect(0, 118, W, 2, BLACK)

    # --- lead story ----------------------------------------------------
    cv.text(M, 132, "WORLD \u2014 TOP STORY", 2, RED)
    y = 158
    for line in wrap(LEAD_HEAD, CW, 4):
        cv.text(M, y, line, 4, BLACK)
        y += 36
    cv.rect(M, y + 4, CW, 1, LIGHTGREY)
    y += 16
    for line in wrap(LEAD_BODY, CW, 2):
        cv.text(M, y, line, 2, BLACK)
        y += 18

    # --- graphic panel: Kyiv skyline under missile streaks -------------
    px, py, pw, ph = M, 334, CW, 96
    cv.rect(px, py, pw, ph, BLACK)
    cv.text(px + 16, py + 12, "KYIV UNDER FIRE", 2, WHITE)
    cv.rect(px + 16, py + 32, 150, 3, RED)
    # skyline silhouettes (fixed, deterministic)
    buildings = [(0, 62, 34), (70, 42, 58), (122, 56, 30), (188, 46, 64),
                 (244, 62, 40), (316, 52, 74), (378, 46, 44), (434, 62, 56),
                 (506, 42, 32), (558, 56, 66), (624, 46, 42), (680, 62, 60),
                 (752, 52, 36), (814, 46, 68), (870, 56, 44), (936, 24, 52)]
    for bx, bw, bh in buildings:
        cv.rect(px + bx, py + ph - bh, bw, bh, (58, 58, 58))
    # lit windows: fixed pattern
    for wx, wy in [(20, 392), (90, 380), (150, 400), (210, 372), (270, 398),
                   (340, 368), (400, 392), (460, 380), (530, 400), (580, 372),
                   (650, 396), (700, 380), (770, 400), (830, 372), (890, 394),
                   (950, 384)]:
        cv.rect(px + wx, wy, 4, 4, (255, 214, 90))
    # missile streaks falling from the top right
    streaks = [(700, 340, 640, 398), (760, 338, 712, 392), (830, 342, 788, 396),
               (890, 340, 856, 388), (940, 344, 912, 388)]
    for x0, y0, x1, y1 in streaks:
        cv.line(x0, y0, x1, y1, (255, 70, 60))
        cv.line(x0 + 1, y0, x1 + 1, y1, (255, 70, 60))
        cv.disc(x1, y1, 3, (255, 150, 40))
    cv.disc(640, 398, 6, (255, 90, 40))
    cv.disc(788, 396, 5, (255, 90, 40))

    # --- rule above the grid -------------------------------------------
    cv.rect(0, 446, W, 3, BLACK)

    # --- story grid: 3 columns x 3 rows --------------------------------
    col_w = 304
    col_x = [M, 344, 656]
    row_y = [462, 610, 758]
    for cx in (336, 648):
        cv.rect(cx, 462, 1, 428, LIGHTGREY)
    for idx, (kicker, head, body) in enumerate(STORIES):
        x = col_x[idx % 3]
        y = row_y[idx // 3]
        cv.text(x, y, kicker, 1, RED)
        y += 14
        for line in wrap(head, col_w, 2):
            cv.text(x, y, line, 2, BLACK)
            y += 18
        y += 6
        for line in wrap(body, col_w, 1):
            cv.text(x, y, line, 1, BLACK)
            y += 10

    # --- markets strip --------------------------------------------------
    cv.rect(0, 896, W, 3, BLACK)
    cv.rect(0, 900, W, H - 900, BLACK)
    cv.text(M, 916, "MARKETS", 1, (255, 90, 80))
    y = 936
    for line in wrap(MARKETS, CW, 1):
        cv.text(M, y, line, 1, WHITE)
        y += 12
    cv.text(M, 992, "THE WORLD \u2014 SATURDAY, 21 NOVEMBER 2026",
            1, (150, 150, 150))


def main():
    cv = Canvas(W, H)
    draw_page(cv)
    data = png_bytes(cv)
    with open("poster.png", "wb") as f:
        f.write(data)
    print("poster.png: %dx%d, %d bytes" % (W, H, len(data)))


if __name__ == "__main__":
    main()
