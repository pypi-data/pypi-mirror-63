from typing import Union
from ..device import Servo
from ..pin import DIGPin, PWMPin


class OJ28(Servo):

    def __init__(self):
        super().__init__()
        self.running = False
        self.pos: Union[PWMPin, DIGPin] = None
        self.neg: Union[PWMPin, DIGPin] = None

    def on_attached(self):
        for pin in self.pins:
            setattr(self, pin.tag, pin)
        assert self.pos and self.neg, 'Invalid Pins'
        self.pos.change_frequency(60)
        self.running = True

    def on_detatched(self):
        self.running = False
        self.pos.stop()

    def move(self):
        if not self.running:
            return
        self.speed <= 1.0, 'Invalid Speed'
        self.pos.change_duty_cycle(self.speed * 100)
        if self.direction == 1:
            self.pos.output(1)
            self.neg.output(0)
        elif self.direction == -1:
            self.pos.output(0)
            self.neg.output(1)
        else:
            self.stop()

    def stop(self):
        self.pos.stop()
