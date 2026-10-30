#!/usr/bin/env python3
"""Make a 1200x630 blog / social cover image.

Usage: python3 tools/make_cover.py <topic> "<post title>" <out.jpg>

topic = one of the files in img/blog-bg/ without .jpg:
probate, foreclosure, subject-to, divorce, bankruptcy, eviction,
tired-landlord, vacant-land, mobile-home, general

The card: topic photo in the background under a navy overlay, a green topic
label, the post title, James's photo in a circle, and the phone number.
"""
import os
import sys
import textwrap

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTS = os.path.join(ROOT, "tools", "fonts")
W, H = 1200, 630
NAVY = (15, 42, 71)
GREEN = (34, 139, 76)
PHONE = "(904) 750-3565"
LABELS = {
    "probate": "PROBATE", "foreclosure": "FORECLOSURE", "subject-to": "SUBJECT-TO",
    "divorce": "DIVORCE", "bankruptcy": "BANKRUPTCY", "eviction": "EVICTIONS",
    "tired-landlord": "TIRED LANDLORDS", "vacant-land": "VACANT LAND",
    "mobile-home": "MOBILE HOMES", "general": "SELL YOUR HOUSE FAST",
}


def font(name, size):
    return ImageFont.truetype(os.path.join(FONTS, name), size)


def cover_crop(im, w, h):
    r = max(w / im.width, h / im.height)
    im = im.resize((round(im.width * r), round(im.height * r)), Image.LANCZOS)
    x, y = (im.width - w) // 2, (im.height - h) // 2
    return im.crop((x, y, x + w, y + h))


def main(topic, title, out):
    bg_path = os.path.join(ROOT, "img", "blog-bg", f"{topic}.jpg")
    if not os.path.exists(bg_path):
        bg_path = os.path.join(ROOT, "img", "blog-bg", "general.jpg")
    bg = cover_crop(Image.open(bg_path).convert("RGB"), W, H).filter(ImageFilter.GaussianBlur(1.5))

    # navy overlay, darker on the left where the text sits
    ov = Image.new("RGBA", (W, H))
    d = ImageDraw.Draw(ov)
    for x in range(W):
        a = int(235 - 95 * (x / W))
        d.line([(x, 0), (x, H)], fill=NAVY + (a,))
    img = Image.alpha_composite(bg.convert("RGBA"), ov)
    d = ImageDraw.Draw(img)

    # topic label
    lab = LABELS.get(topic, LABELS["general"])
    f_lab = font("Inter-ExtraBold.otf", 26)
    tw = d.textlength(lab, font=f_lab)
    d.rounded_rectangle([60, 56, 60 + tw + 36, 56 + 48], radius=10, fill=GREEN)
    d.text((78, 64), lab, font=f_lab, fill="white")

    # title, shrink to fit 4 lines in the left 760px
    for size in (64, 58, 52, 46, 42):
        f_t = font("Inter-ExtraBold.otf", size)
        chars = max(10, int(740 / (size * 0.55)))
        lines = textwrap.wrap(title, chars)
        if len(lines) <= 4 and all(d.textlength(l, font=f_t) <= 760 for l in lines):
            break
    y = 140
    for l in lines[:4]:
        d.text((60, y), l, font=f_t, fill="white")
        y += int(size * 1.18)

    # footer
    f_ft = font("Inter-SemiBold.otf", 30)
    d.text((60, H - 84), f"Jax Cash Buyers  ·  {PHONE}", font=f_ft, fill=(220, 235, 245))

    # James in a circle, bottom right
    face = Image.open(os.path.join(ROOT, "img", "james-stallworth.jpg")).convert("RGB")
    s = 250
    face = cover_crop(face, s, s)
    mask = Image.new("L", (s, s), 0)
    ImageDraw.Draw(mask).ellipse([0, 0, s, s], fill=255)
    cx, cy = W - s - 70, H - s - 95
    d.ellipse([cx - 7, cy - 7, cx + s + 7, cy + s + 7], fill="white")
    img.paste(face, (cx, cy), mask)
    f_nm = font("Inter-SemiBold.otf", 24)
    nm = "James Stallworth, Owner"
    d.text((cx + s / 2 - d.textlength(nm, font=f_nm) / 2, cy + s + 16), nm, font=f_nm, fill="white")

    img.convert("RGB").save(out, quality=86, optimize=True)


if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2], sys.argv[3])
