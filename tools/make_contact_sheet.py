from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


MEDIA_DIR = Path(r"e:\PycharmProjects\TuristPRO\presentation_assets\docx_media")
OUT = Path(r"e:\PycharmProjects\TuristPRO\presentation_assets\contact_sheet.png")


def main() -> None:
    files = sorted(MEDIA_DIR.glob("*.png"))
    thumb_w, thumb_h = 260, 160
    cols = 3
    rows = (len(files) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * thumb_w, rows * (thumb_h + 34)), "white")
    draw = ImageDraw.Draw(sheet)

    for idx, file in enumerate(files):
        im = Image.open(file).convert("RGB")
        im.thumbnail((thumb_w - 20, thumb_h - 20))
        x = (idx % cols) * thumb_w + (thumb_w - im.width) // 2
        y = (idx // cols) * (thumb_h + 34) + 10
        sheet.paste(im, (x, y))
        label = f"{file.stem}  {Image.open(file).size[0]}x{Image.open(file).size[1]}"
        draw.text(((idx % cols) * thumb_w + 10, y + thumb_h - 6), label, fill=(30, 42, 40))

    sheet.save(OUT)
    print(OUT)


if __name__ == "__main__":
    main()
