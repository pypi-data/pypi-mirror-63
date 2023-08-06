"""提供拖动tkinter控件工具的模块。
A module supplies tools to drag tkinter window and widgets."""
import tkinter as tk
import tkinter.ttk as ttk

__author__="qfcy"
__version__="1.0"

def mousedown(event):
    widget=event.widget
    widget.startx=event.x
    widget.starty=event.y
def drag(event):
    widget=event.widget
    try:
        if isinstance(widget,tk.Wm):
            widget.geometry("+%d+%d"%(widget.winfo_x()+(event.x-widget.startx),
                                  widget.winfo_y()+(event.y-widget.starty)))
        else:
            widget.place(x=widget.winfo_x()+(event.x-widget.startx),
                     y=widget.winfo_y()+(event.y-widget.starty))
    except AttributeError:
        raise ValueError("The widget %s is not draggable"%widget)

def draggable(tkwidget):
    """调用draggable(tkwidget) 使tkwidget可拖动。
tkwidget为一个控件(Widget)或一个窗口(Wm)。"""
    tkwidget.bind("<Button-1>",mousedown,add='+')
    tkwidget.bind("<B1-Motion>",drag,add='+')

def test():
    root=tk.Tk()
    root.title("Test")
    button=ttk.Button(root,text="Drag!")
    button.place(width=80,height=30)
    draggable(root) #只需调用draggable(root),就能使root下的子控件button可拖动
    root.mainloop()

if __name__=="__main__":test()
