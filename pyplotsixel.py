# Copyright (c) 2024 Hajime Nakagami
# Released under the BSD license.
# https://github.com/nakagami/pyplotsixel/blob/master/pyplotsixel.py
import sys
import io
import numpy as np
from PIL import Image
from matplotlib.backend_bases import _Backend, FigureManagerBase
from matplotlib.backends.backend_agg import FigureCanvasAgg


def convert_line(data):
    colors_set = set()
    buf = []
    height, width = np.shape(data)

    def _convert_line(color, next_x):
        node = []
        count = 0
        cache = 0
        if next_x:
            node.append((0, next_x))
        for x in range(next_x, width):
            count += 1
            six = 0
            for y in range(height):
                p = data[y, x]
                if p == color:
                    six |= 1 << y
                elif p not in colors_set:
                    colors_set.add(p)
                    _convert_line(p, x)
            if six != cache:
                node.append((cache, count))
                count = 0
                cache = six
        if cache != 0:
            node.append((cache, count))
        buf.append((color, node))

    _convert_line(data[0, 0], 0)

    return buf


def output_sixel(image, output):
    image = image.quantize(256).convert("P", palette=Image.ADAPTIVE, colors=256)
    width, height = image.size

    # header
    output.write(f'\x1bP7;1;75q"1;1;{width};{height}')

    # palette
    palette = np.array(image.getpalette())
    palette = np.reshape(palette, (palette.size // 3, 3))
    for i in set(image.getdata()):
        p = palette[i]
        output.write(f'#{i};2;{p[0]*100//256};{p[1]*100//256};{p[2]*100//256}\n')

    # body
    data = np.array(image.getdata())
    data = np.reshape(data, (data.size // width, width))
    for y in range(0, height, 6):
        for n, node in convert_line(data[y:y+6]):
            output.write(f"#{n}\n")
            for six, count in node:
                if count < 4:
                    output.write(chr(0x3f + six) * count)
                else:
                    output.write('!%d%c' % (count, 0x3f + six))
            output.write("$\n")
        output.write("-\n")

    # terminate
    output.write('\x1b\\')


class SixelFigureManager(FigureManagerBase):
    def show(self):
        buf = io.BytesIO()
        self.canvas.figure.savefig(buf)
        with Image.open(buf) as image:
            output_sixel(image, sys.stdout)


class SixelFigureCanvas(FigureCanvasAgg):
    manager_class = SixelFigureManager


@_Backend.export
class _BackendSixelAgg(_Backend):
    FigureCanvas = SixelFigureCanvas
    FigureManager = SixelFigureManager
