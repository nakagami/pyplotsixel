from tempfile import NamedTemporaryFile
from matplotlib.backend_bases import _Backend, FigureManagerBase
from matplotlib.backends.backend_agg import FigureCanvasAgg
from libsixel.encoder import Encoder as SixelEncoder


class SixelFigureManager(FigureManagerBase):
    def show(self):
        with NamedTemporaryFile(prefix="sixel-") as f:
            self.canvas.figure.savefig(f, format="png")
            f.flush()
            encoder = SixelEncoder()
            encoder.encode(f.name)


class SixelFigureCanvas(FigureCanvasAgg):
    manager_class = SixelFigureManager


@_Backend.export
class _BackendSixelAgg(_Backend):
    FigureCanvas = SixelFigureCanvas
    FigureManager = SixelFigureManager
