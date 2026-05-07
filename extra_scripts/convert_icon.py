from PIL import Image
import os

def convert_png_to_ico(png_path, ico_path):
    if os.path.exists(png_path):
        img = Image.open(png_path)
        # Tạo icon với nhiều kích thước chuẩn Windows
        icon_sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
        img.save(ico_path, sizes=icon_sizes)
        print(f"Da chuyen doi {png_path} thanh {ico_path}")
    else:
        print(f"Khong tim thay {png_path}")

if __name__ == "__main__":
    convert_png_to_ico("Logo512.png", "Logo512.ico")
