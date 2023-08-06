from nnoir.functions import *
from .utils import *


class OpReduceMean(Op):

    def __init__(self, node):
        super(OpReduceMean, self).__init__(node)

        self.axes = None
        self.keepdims = True
        for attr in node.attribute:
            if attr.name == 'axes':
                self.axes = attr.ints
            if attr.name == 'keepdims':
                self.keepdims = attr.i > 0

    def to_function(self, env, constants):
        if self.axes == [2, 3] and self.keepdims:
            [x] = self.node.input
            _input = env[x]
            in_h = _input.shape[2]
            in_w = _input.shape[3]
            kh = in_h
            kw = in_w
            sy = 1
            sx = 1
            pad_h = (0, 0)
            pad_w = (0, 0)
            return [
                AveragePooling2D(
                    list(self.node.input),
                    list(self.node.output),
                    kernel=(kh, kw),
                    stride=(sy, sx),
                    pad_h=pad_h,
                    pad_w=pad_w,
                    count_exclude_pad=False,
                )
            ]
        else:
            raise UnsupportedONNXOperation(self.node, "can't replace by AveragePooling2D")
