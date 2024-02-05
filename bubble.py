from pyglet.window import Window
from pyglet.app import run
from pyglet.shapes import Rectangle
from pyglet.graphics import Batch
from pyglet import clock

class Renderer(Window):
    def __init__(self):
        super().__init__(800, 680, "Bubble sort")
        self.batch = Batch()
        self.x = [3, 4, 2, 1, 6, 5]
        self.bars = [Rectangle(100 + e * 100, 100, 80, i * 100, batch=self.batch) for e, i in enumerate(self.x)]
        self.steps = self.bubble_sort()
        self.comparison_indices = None

    def bubble_sort(self):
        n = len(self.x)
        steps = []
        sorted_flag = False
        while not sorted_flag:
            sorted_flag = True
            for j in range(n - 1):
                steps.append((list(self.x), (j, j+1)))
                if self.x[j] > self.x[j + 1]:
                    self.x[j], self.x[j + 1] = self.x[j + 1], self.x[j]
                    sorted_flag = False
                steps.append((list(self.x), (j, j+1)))  # Add step after swapping to stop highlighting
            steps.append((list(self.x), None))  # Add step to make all bars white after each pass

        return steps

    def on_update(self, deltatime):
        if self.steps:
            current_step, comparison_indices = self.steps.pop(0)
            self.comparison_indices = comparison_indices

            for i, bar in enumerate(self.bars):
                bar.height = current_step[i] * 100

    def on_draw(self):
        self.clear()
        for i, bar in enumerate(self.bars):
            if self.comparison_indices and i in self.comparison_indices:
                bar.color = (255, 0, 0, 255)  # Red color for comparison
            else:
                bar.color = (255, 255, 255, 255)  # White color for other bars
            bar.draw()

renderer = Renderer()
clock.schedule_interval(renderer.on_update, 0.3)
run()