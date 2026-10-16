from pathlib import Path
from xml.etree import ElementTree as ET
from zipfile import ZipFile
import re


DOCX_PATH = Path(
    r"C:\Users\user\Desktop\251\Создание системы бронирования экскурсий и мастер-классов в туристическом городе\Создание системы бронирования экскурсий и мастер-классов в туристическом городе.docx"
)
OUT_DIR = Path(r"e:\PycharmProjects\TuristPRO\presentation_assets")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    media_dir = OUT_DIR / "docx_media"
    media_dir.mkdir(exist_ok=True)

    with ZipFile(DOCX_PATH) as archive:
        media = [name for name in archive.namelist() if name.startswith("word/media/")]
        for index, name in enumerate(media, 1):
            ext = Path(name).suffix.lower()
            target = media_dir / f"media_{index:02d}{ext}"
            target.write_bytes(archive.read(name))

        xml = archive.read("word/document.xml")

    root = ET.fromstring(xml)
    ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
    paragraphs: list[str] = []

    for paragraph in root.findall(".//w:p", ns):
        texts = [node.text or "" for node in paragraph.findall(".//w:t", ns)]
        value = "".join(texts).strip()
        if value:
            paragraphs.append(value)

    (OUT_DIR / "docx_text.txt").write_text("\n".join(paragraphs), encoding="utf-8")

    print(f"paragraphs {len(paragraphs)}")
    print(f"media {len(media)}")
    for paragraph in paragraphs[:120]:
        if re.match(r"^(Введение|Глава|\d\.\d|Заключение|Рисунок|Таблица|Листинг)", paragraph, re.I):
            print(paragraph[:180])


if __name__ == "__main__":
    main()
