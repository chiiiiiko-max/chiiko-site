#!/usr/bin/env python3
"""作品画像に「© chiiko illust」の透かしを焼き込んだ拡大表示用JPEGを img/wm/ に生成"""
import os
from PIL import Image, ImageDraw, ImageFont

IMG = "/Users/user/Desktop/Claude/CiikoCorporation/chiiko-site/img"
OUT = os.path.join(IMG, "wm")
TEXT = "© chiiko illust"

targets = [
    "illust_summer.jpg", "illust_thankyou.jpg", "illust_calendar.jpg",
    "genga_drink.jpg", "genga_bath.jpg", "genga_mock1.jpg", "genga_mock2.jpg",
    "manga_monday.jpg", "manga_beautysearch.jpg",
]

font_path = "/System/Library/Fonts/Supplemental/Arial.ttf"

for name in targets:
    src = os.path.join(IMG, name)
    im = Image.open(src).convert("RGBA")
    w, h = im.size

    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    size = max(24, w // 14)
    font = ImageFont.truetype(font_path, size)

    # 斜めタイル用レイヤー（大きめに作って回転→中央合わせ）
    diag = int((w * w + h * h) ** 0.5)
    tile = Image.new("RGBA", (diag, diag), (0, 0, 0, 0))
    td = ImageDraw.Draw(tile)
    bbox = td.textbbox((0, 0), TEXT, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    step_x, step_y = tw + size * 3, th + size * 4
    yy = 0
    row = 0
    while yy < diag:
        xx = -(row % 2) * step_x // 2
        while xx < diag:
            td.text((xx, yy), TEXT, font=font, fill=(120, 116, 110, 60))
            xx += step_x
        yy += step_y
        row += 1
    tile = tile.rotate(30, expand=False)
    overlay.alpha_composite(tile, (-(diag - w) // 2, -(diag - h) // 2))

    # 右下に少し濃いめのクレジット
    small = ImageFont.truetype(font_path, max(18, w // 40))
    d = ImageDraw.Draw(overlay)
    sb = d.textbbox((0, 0), TEXT, font=small)
    sw, sh = sb[2] - sb[0], sb[3] - sb[1]
    d.text((w - sw - 20, h - sh - 20), TEXT, font=small, fill=(90, 86, 80, 150))

    out = Image.alpha_composite(im, overlay).convert("RGB")
    out.save(os.path.join(OUT, name), "JPEG", quality=82)
    print(name, "->", out.size)
