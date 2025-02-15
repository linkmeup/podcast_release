from PIL import Image, ImageDraw, ImageFont

from constants import FONT, FONT_DOSHLO_1


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


def split_text_doshlo(text: str) -> str:
    text = text.split(". ")[-1]

    # return text
    words = text.split()
    width = 20

    row = ""
    lines = []
    for word in words:
        if len(row + word) + 1 <= width:
            row += f"{word} "
        else:
            row += f"{word}"
            lines.append(row)
            row = ""
    lines.append(row)
    return lines


def add_text(img, text, podcast):

    width, height = img.size
    if podcast.feed == "donasdoshlo":
        draw = ImageDraw.Draw(img)
        font1 = ImageFont.truetype(FONT_DOSHLO_1, height / 10)
        font2 = ImageFont.truetype(FONT_DOSHLO_1, height / 20)
        draw.text(
            (width / 2, height / 2 - 300),
            "До нас дошло",
            (0, 0, 0),
            anchor="ms",
            font=font1,
        )

        i = 0
        lines = split_text_doshlo(text)
        for line in lines:
            i += 200
            draw.text(
                (width / 2, height / 2 + 100 + i),
                line,
                (0, 0, 0),
                anchor="ms",
                font=font2,
            )

        font3 = ImageFont.truetype(FONT_DOSHLO_1, height / 80)
        draw.text(
            (width / 2, height - height / 7),
            podcast.episode_number,
            (0, 0, 0),
            anchor="ms",
            font=font3,
        )
    else:
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

    img = img.resize((width_new, height_new), Image.LANCZOS)
    img = img.crop(
        (
            width_new / 2 - 240,
            height_new / 2 - 275,
            width_new / 2 + 240,
            height_new / 2 + 275,
        )
    )
    img = add_corners(img, 20)

    return img


def prepare_rss_cover(podcast) -> str:

    if podcast.feed == "donasdoshlo":
        img = Image.open(podcast.cover).convert("RGBA")
        rss_cover_name = f"img/covers/{podcast.filename}_rss_cover.png"
        img = img.resize((1400, 1400), Image.LANCZOS)
        img.save(rss_cover_name)

        return rss_cover_name

    img = Image.open(podcast.cover).convert("RGBA")

    width, height = img.size
    width_new = 1400
    height_new = int(1400 / width * height)

    img = img.resize((width_new, height_new), Image.LANCZOS)

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

    img = img.resize((width_new, height_new), Image.LANCZOS)
    img = img.crop((0, 0, 1400, 1400))

    vk_cover_name = f"img/covers/{podcast.filename}_vk_cover.png"
    img.save(vk_cover_name)

    return vk_cover_name


def prepare_video_cover(podcast) -> str:

    if podcast.feed == "donasdoshlo":
        video_cover_file_name = f"img/defaults/{podcast.feed}_video.png"

    bottom = Image.open(video_cover_file_name)
    add_text(bottom, podcast.title, podcast)

    bottom = bottom.resize((1920, 1080), Image.LANCZOS)

    video_cover_name = (
        f"{podcast.cover.split('_')[0]}_video_{podcast.cover.split('_')[1]}"
    )
    bottom.save(video_cover_name)

    return video_cover_name


def gen_cover(podcast) -> str:

    img = prepare_img(Image.open(podcast.img)).convert("RGBA")

    cover_file_name = f"img/defaults/{podcast.feed}.jpg"

    if podcast.feed == "donasdoshlo":
        cover_file_name = f"img/defaults/{podcast.feed}.png"

    bottom = Image.open(cover_file_name)

    if podcast.feed != "donasdoshlo":
        r, g, b, a = img.split()
        top = Image.merge("RGB", (r, g, b))
        mask = Image.merge("L", (a,))

        bottom.paste(top, (44, 83), mask)

    add_text(bottom, podcast.title, podcast)
    bottom = bottom.resize((1000, 1000), Image.LANCZOS)

    cover_name = f"img/covers/{podcast.filename}_cover.png"
    bottom.save(cover_name)

    return cover_name
