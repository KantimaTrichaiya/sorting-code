from pyglet.window import Window
from pyglet.app import run
from pyglet.shapes import Rectangle
from pyglet.graphics import Batch
from pyglet import clock

class Renderer(Window):
    def __init__(self):
        super().__init__(640, 640, "Merge Sort")
        self.batch = Batch()
        self.x = [3, 4, 2, 1, 6, 5] 
        self.bars = [Rectangle(50 + i * 90, 100, 80, self.x[i] * 30, color=(255, 255, 255), batch=self.batch) for i in range(len(self.x))]
        self.sorted = False
        self.animation_generator = self.merge_sort_animation(0, len(self.x) - 1)
        self.done = False

    def merge_sort_animation(self, l, r):
        if l < r:
            mid = (l + r) // 2
            yield from self.merge_sort_animation(l, mid)
            yield from self.merge_sort_animation(mid + 1, r)
            yield from self.merge_animation(l, mid, r)

    def merge_animation(self, l, mid, r):
        left = self.x[l:mid + 1]
        right = self.x[mid + 1:r + 1]

        i = j = 0
        k = l

        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                self.x[k] = left[i]
                i += 1
            else:
                self.x[k] = right[j]
                j += 1
            k += 1
            yield 

        while i < len(left):
            self.x[k] = left[i]
            i += 1
            k += 1
            yield

        while j < len(right):
            self.x[k] = right[j]
            j += 1
            k += 1
            yield

        self.update_bars()

    def update_bars(self):
        self.batch = Batch()
        for e, i in enumerate(self.x):
            self.bars[e] = Rectangle(50 + e * 90, 100, 80, i * 30, color=(255, 255, 255), batch=self.batch)

    def on_update(self, deltatime):
        if not self.done:
            try:
                next(self.animation_generator)
            except StopIteration:
                self.done = True

    def on_draw(self):
        self.clear()
        self.batch.draw()

renderer = Renderer()
clock.schedule_interval(renderer.on_update, 0.2)
run()

