from natsort import natsorted
from PIL import Image, ImageDraw
from pdf2image import convert_from_path
from reportlab.pdfgen import canvas
import datetime
import shutil
import sys
import os
import re


def clear_dir(src):
    files_names = os.listdir(src)
    for file_name in files_names:
        os.remove(os.path.join(src, file_name))


def extract_img_from_pdf(src, dst, fmt, dpi):
    pages = convert_from_path(src, dpi=dpi, fmt=fmt)
    for page in pages:
        name = re.sub(r'[\s:.-]', '', str(datetime.datetime.now()))
        page.save(os.path.join(dst, name + '.' + fmt), fmt)


def process_lt_corner(draw, px, wnd):
    for i in range(wnd):
        for j in range(wnd):
            draw.point((i, j), px[wnd + 1, j])
            lt = px[(wnd + 1, 0)]
            lb = px[(0, wnd + 1)]
            draw.point((0, j), (
                int(lb[0] + j * ((lt[0] - lb[0]) / wnd)),
                int(lb[1] + j * ((lt[1] - lb[1]) / wnd)),
                int(lb[2] + j * ((lt[2] - lb[2]) / wnd))
            ))
            draw.point((1, j), (
                int(lb[0] + j * ((lt[0] - lb[0]) / wnd)),
                int(lb[1] + j * ((lt[1] - lb[1]) / wnd)),
                int(lb[2] + j * ((lt[2] - lb[2]) / wnd))
            ))


def process_rt_corner(draw, px, wnd):
    for i in range(wnd):
        for j in range(wnd):
            draw.point((img_width - i, j), px[img_width - wnd - 1, j])
            rt = px[(img_width - wnd - 1, 0)]
            rb = px[(img_width - 1, wnd + 1)]
            draw.point((img_width - 1, j), (
                int(rb[0] + j * ((rt[0] - rb[0]) / wnd)),
                int(rb[1] + j * ((rt[1] - rb[1]) / wnd)),
                int(rb[2] + j * ((rt[2] - rb[2]) / wnd))
            ))
            draw.point((img_width - 2, j), (
                int(rb[0] + j * ((rt[0] - rb[0]) / wnd)),
                int(rb[1] + j * ((rt[1] - rb[1]) / wnd)),
                int(rb[2] + j * ((rt[2] - rb[2]) / wnd))
            ))


def process_rb_corner(draw, px, wnd):
    for i in range(wnd):
        for j in range(wnd):
            draw.point((img_width - i, img_height - j - 1), px[img_width - wnd - 1, img_height - j - 1])
            rb = px[(img_width - wnd - 1, img_height - 1)]
            rt = px[(img_width - 1, img_height - wnd - 1)]
            draw.point((img_width - 1, img_height - j - 1), (
                int(rb[0] + j * ((rt[0] - rb[0]) / wnd)),
                int(rb[1] + j * ((rt[1] - rb[1]) / wnd)),
                int(rb[2] + j * ((rt[2] - rb[2]) / wnd))
            ))
            draw.point((img_width - 2, img_height - j - 1), (
                int(rb[0] + j * ((rt[0] - rb[0]) / wnd)),
                int(rb[1] + j * ((rt[1] - rb[1]) / wnd)),
                int(rb[2] + j * ((rt[2] - rb[2]) / wnd))
            ))


def process_lb_corner(draw, px, wnd):
    for i in range(wnd):
        for j in range(wnd):
            draw.point((i, img_height - j - 1), px[wnd + 1, img_height - j - 1])
            lb = px[(wnd + 1, img_height - 1)]
            lt = px[(0, img_height - wnd - 1)]
            draw.point((0, img_height - j - 1), (
                int(lb[0] + j * ((lt[0] - lb[0]) / wnd)),
                int(lb[1] + j * ((lt[1] - lb[1]) / wnd)),
                int(lb[2] + j * ((lt[2] - lb[2]) / wnd))
            ))
            draw.point((1, img_height - j - 1), (
                int(lb[0] + j * ((lt[0] - lb[0]) / wnd)),
                int(lb[1] + j * ((lt[1] - lb[1]) / wnd)),
                int(lb[2] + j * ((lt[2] - lb[2]) / wnd))
            ))


def process_img(src, dst, fmt, wnd):
    img = Image.open(src)
    draw = ImageDraw.Draw(img)
    px = img.load()
    process_lt_corner(draw, px, wnd)
    process_rt_corner(draw, px, wnd)
    process_rb_corner(draw, px, wnd)
    process_lb_corner(draw, px, wnd)
    img.save(dst, fmt)
    del draw


def create_pdf_from_img(src, dst, img_width, img_height):
    c = canvas.Canvas(dst, pagesize=(img_width, img_height))
    png_names = os.listdir(src)
    png_names = natsorted(png_names, key=lambda y: y.lower())
    for png_name in png_names:
        c.drawImage(os.path.join(src, png_name), 0, 0, width=img_width, height=img_height)
        c.showPage()
    c.save()


if __name__ == "__main__":
    dir_root = os.path.dirname(__file__)
    src_pdf_path = os.path.join(dir_root, 'pdf\\input\\')
    dst_pdf_path = os.path.join(dir_root, 'pdf\\output\\')
    src_png_path = os.path.join(dir_root, 'png\\input\\')
    dst_png_path = os.path.join(dir_root, 'png\\output\\')
    fmt = 'png'
    dpi = 300
    pps = 3 / 4

    if '-png' in sys.argv:
        clear_dir(src_pdf_path)
        pdf_name = re.sub(r'[\s:.-]', '', str(datetime.datetime.now())) + '.pdf'
        png_names = os.listdir(src_png_path)
        img = Image.open(os.path.join(src_png_path, png_names[0]))
        create_pdf_from_img(src_png_path, os.path.join(src_pdf_path, pdf_name), img.size[0], img.size[1])
        del img
    elif '-pdf' in sys.argv:
        pass
    else:
        print(
            """
            You have to run the script with one of the arguments:\n
            1. -pdf - To process pdf documents.
            2. -png - To process image documents.
            """
        )
        exit()

    pdf_names = os.listdir(src_pdf_path)
    for pdf_name in pdf_names:
        clear_dir(src_png_path)
        clear_dir(dst_png_path)

        extract_img_from_pdf(os.path.join(src_pdf_path, pdf_name), src_png_path, fmt, dpi)

        png_names = os.listdir(src_png_path)
        img = Image.open(os.path.join(src_png_path, png_names[0]))
        img_width = img.size[0]
        img_height = img.size[1]
        wnd = int(((img_width / 3000) * dpi) / 6)
        for png_name in png_names:
            process_img(os.path.join(src_png_path, png_name), os.path.join(dst_png_path, png_name), fmt, wnd)

        create_pdf_from_img(dst_png_path, os.path.join(dst_pdf_path, pdf_name), img_width, img_height)
