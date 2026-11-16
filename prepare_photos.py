"""写真を公開用に整える：向き補正→長辺1280px→位置情報など全メタデータ削除→指定範囲をぼかし→JPEG保存
使い方: python prepare_photos.py 入力.jpg 出力.jpg [--blur x1,y1,x2,y2 ...]   (座標は0〜1の割合)"""
import sys
from PIL import Image, ImageOps, ImageFilter
def prepare(src, dst, boxes=(), long=1280, q=78):
    im = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
    im.thumbnail((long, long), Image.LANCZOS)
    W, H = im.size
    for x1, y1, x2, y2 in boxes:
        b = (int(x1*W), int(y1*H), int(x2*W), int(y2*H))
        reg = im.crop(b)
        sm = reg.resize((max(1, reg.width//14), max(1, reg.height//14))).resize(reg.size, Image.NEAREST)
        im.paste(sm.filter(ImageFilter.GaussianBlur(6)), b)
    im.save(dst, "JPEG", quality=q, optimize=True, progressive=True)  # exif を渡さない＝メタデータなし
if __name__ == "__main__":
    a = sys.argv[1:]; boxes = []
    if "--blur" in a:
        i = a.index("--blur"); boxes = [tuple(map(float, s.split(","))) for s in a[i+1:]]; a = a[:i]
    prepare(a[0], a[1], boxes)
