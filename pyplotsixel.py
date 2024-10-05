# Copyright (c) 2024 Hajime Nakagami
# Released under the BSD license.
# https://github.com/nakagami/pyplotsixel/blob/master/pyplotsixel.py
import sys
import io
import numpy as np
from PIL import Image
from matplotlib.backend_bases import _Backend, FigureManagerBase
from matplotlib.backends.backend_agg import FigureCanvasAgg


def _convert_line(data):
    height, width = np.shape(data)
    colors = list(set(data.flatten()))
    six_list = dict([(color, []) for color in colors])
    buf = []

    for x in range(width):
        six = dict([(color, 0) for color in colors])
        for y in range(height):
            six[data[y, x]] |= 1 << y
        for color in colors:
            six_list[color].append(six[color])

    for color in colors:
        start_and_six = [(0, six_list[color][0])]
        for i, six in enumerate(six_list[color][1:], start=1):
            if start_and_six[-1][1] != six:
                start_and_six.append((i, six))

        node = []
        for i, (start, six) in enumerate(start_and_six[:-1]):
            next_start = start_and_six[i + 1][0]
            node.append((six, next_start - start))
        start, six = start_and_six[-1]
        node.append((six, width - start))

        buf.append((color, node))

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
        for n, node in _convert_line(data[y:y+6]):
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
