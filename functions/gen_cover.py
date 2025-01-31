from PIL import Image, ImageDraw, ImageFont

from constants import FONT


def add_corners(im, rad):
    circle = Image.new("L", (rad * 2, rad * 2), 0)
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, rad * 2, rad * 2), fill=255)
    alpha = Image.new("L", im.size, 255)
    w, h = im.size
    alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
    alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
    alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
    alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (w - rad, h - rad))
    im.putalpha(alpha)
    return im


def split_text(text: str) -> str:
    words = text.replace("_", " ").split()
    if len(text) < 50:
        letters = 17
    elif len(text) < 80:
        letters = 21
    else:
        letters = 26
    text_splitted = ""
    row = ""
    for word in words:
        if len(row + word) + 1 <= letters:
            row += f"{word} "
            text_splitted += f"{word} "
        else:
            row += f"\n{word} "
            text_splitted += f"\n{word} "
            row = word

    return text_splitted


def add_text(img, text):
    draw = ImageDraw.Draw(img)
    if len(text) < 50:
        font_size = 70
    elif len(text) < 80:
        font_size = 60
    else:
        font_size = 40
    font = ImageFont.truetype(FONT, font_size)
    draw.text((585, 224), split_text(text), (0, 0, 0), font=font)


def prepare_img(img):
    width, height = img.size
    if width <= height:
        width_new = 480
        height_new = int(480 / width * height)
        print(height_new)
        if 550 - height_new < 100:
            height_new = 550
    else:
        height_new = 550
        width_new = int(550 / height * width)

    img = img.resize((width_new, height_new), Image.ANTIALIAS)
    img = img.crop((width_new / 2 - 240, height_new / 2 - 275, width_new / 2 + 240, height_new / 2 + 275))
    img = add_corners(img, 20)


    return img


def prepare_rss_cover(podcast) -> str:

    img = Image.open(podcast.cover).convert("RGBA")

    width, height = img.size
    width_new = 1400
    height_new = int(1400 / width * height)

    img = img.resize((width_new, height_new), Image.ANTIALIAS)

    bottom = Image.open("img/defaults/background.png")
    bottom.paste(img, (0, 300))

    rss_cover_name = f"img/covers/{podcast.filename}_rss_cover.png"
    bottom.save(rss_cover_name)

    return rss_cover_name


def prepare_vk_cover(podcast) -> str:

    img = Image.open(podcast.img).convert("RGBA")

    width, height = img.size

    if width <= height:
        width_new = 1400
        height_new = int(1400 / width * height)
    else:
        height_new = 1400
        width_new = int(1400 / height * width)

    img = img.resize((width_new, height_new), Image.ANTIALIAS)
    img = img.crop((0, 0, 1400, 1400))

    vk_cover_name = f"img/covers/{podcast.filename}_vk_cover.png"
    img.save(vk_cover_name)

    return vk_cover_name


def gen_cover(podcast) -> str:

    img = prepare_img(Image.open(podcast.img)).convert("RGBA")

    r, g, b, a = img.split()
    top = Image.merge("RGB", (r, g, b))
    mask = Image.merge("L", (a,))

    bottom = Image.open(f"img/defaults/{podcast.feed}.jpg")
    bottom.paste(top, (44, 83), mask)

    add_text(bottom, podcast.title)

    cover_name = f"img/covers/{podcast.filename}_cover.png"
    bottom.save(cover_name)

    return cover_name
