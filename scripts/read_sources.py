from pathlib import Path
import fitz
from PIL import Image, ImageDraw

out = Path('tmp/source')
out.mkdir(parents=True, exist_ok=True)
specs = [
    ('James Stewart Calculus Early Transcendentals, 7th Edition 2012.pdf', 'textbook', 131, 140),
    ('Stewart-7E-solutions.pdf', 'solutions', 97, 106),
]
for filename, prefix, start, end in specs:
    doc = fitz.open(filename)
    for number in range(start, end + 1):
        page = doc[number - 1]
        page.get_pixmap(matrix=fitz.Matrix(1.7, 1.7)).save(out / f'{prefix}-{number}.png')
        (out / f'{prefix}-{number}.txt').write_text(page.get_text(sort=True), encoding='utf-8')
    sheet = Image.new('RGB', (2300, 1360), 'white')
    draw = ImageDraw.Draw(sheet)
    for k, number in enumerate(range(start, end + 1)):
        im = Image.open(out / f'{prefix}-{number}.png')
        im.thumbnail((460, 640))
        x, y = k % 5 * 460, k // 5 * 680
        sheet.paste(im, (x, y + 25))
        draw.text((x + 10, y + 5), str(number), fill='black')
    sheet.save(out / f'{prefix}-contact.png')
