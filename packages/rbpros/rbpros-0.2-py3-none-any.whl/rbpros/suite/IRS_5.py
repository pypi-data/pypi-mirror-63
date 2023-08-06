from typing import List
from ..device import Infrared


class IRS_5(Infrared):

    def __init__(self):
        super().__init__()
        self.probe_angle = 120
        self.max_ir = 0.0
        self.max_ir_dir = 0
        self.ir_vals: List[Tuple[int, int]] = []

    def on_attached(self):
        assert sum(p is not None for p in self.pins) > 0, 'Invalid Pins'

    def detect(self) -> bool:
        self.ir_vals.clear()
        for pin in self.pins:
            if pin:
                self.ir_vals.append((pin.num, pin.input()))
        self.ir_vals.sort(key=lambda t: t[1], reverse=True)
        max_ir = self.ir_vals[0]
        self.max_ir_dir = max_ir[0]
        self.value = self.max_ir = max_ir[1]
        return True
