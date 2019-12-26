from tkinter import *

class AutoScrollbar(Scrollbar):
    # a scrollbar that hides itself if it's not needed.  only
    # works if you use the grid geometry manager.
    placement = 'pack'
    option = {}

    def set(self, lo, hi):
        if float(lo) <= 0.0 and float(hi) >= 1.0:
            # grid_remove is currently missing from Tkinter!
            if self.placement is 'pack':
                self.pack_forget()
            elif self.placement is 'grid':
                self.grid_remove()
        else:
            if self.placement is 'pack':
                self.pack()
            elif self.placement is 'grid': 
                self.grid()
        super().set(lo, hi)
    def pack(self, **kw):
        self.placement = 'pack'
        if kw:
            self.option = kw
        super().pack(self.option)

    def grid(self, **kw):
        self.placement = 'grid'
        if kw:
            self.option = kw
        super().grid(self.option)

    def place(self, **kw):
        raise TclError("cannot use place with this widget")