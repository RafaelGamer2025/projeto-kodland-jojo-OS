import tkinter as tk
from ui.widgets.grid_system import snap_to_grid


class DraggableIcon:
    def __init__(self, canvas, widget):
        self.canvas = canvas
        self.widget = widget

        self.offset_x = 0
        self.offset_y = 0

        self._bind_all(self.widget)

    def _bind_all(self, current_widget):
        current_widget.bind("<Button-1>", self.start_drag)
        current_widget.bind("<B1-Motion>", self.drag)
        current_widget.bind("<ButtonRelease-1>", self.drop)

        for child in current_widget.winfo_children():
            self._bind_all(child)

    def start_drag(self, event):
        self.offset_x = event.x
        self.offset_y = event.y

    def drag(self, event):
        x = self.widget.winfo_x() + event.x - self.offset_x
        y = self.widget.winfo_y() + event.y - self.offset_y

        new_x, new_y = snap_to_grid(x, y)
        self.widget.place(x=new_x, y=new_y)

    def drop(self, event):
        x = self.widget.winfo_x()
        y = self.widget.winfo_y()

        new_x, new_y = snap_to_grid(x, y)
        self.widget.place(x=new_x, y=new_y)