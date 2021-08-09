import numpy as np
import serial as sr
import time
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# --------------MAIN GUI------------------
root = tk.Tk()
root.title('Real Time Plot EMG')
root.configure(background='black')
root.geometry('700x500')

# -------------create plot object on GUI-------------
fig = Figure();
ax = fig.add_subplot(111)
ax.set_title('Serial Data');
ax.set_xlabel('Sample')
ax.set_ylabel('Voltage (V)')
ax.set_xlim(0,200)
ax.set_ylim(-0.5,6)
lines = ax.plot([],[])[0]

canvas = FigureCanvasTkAgg(fig, master = root)
canvas.get_tk_widget().place(x=10,y=10,width=500,height=400)
canvas.draw()

# ------------create button---------------
root.update();
start = tk.Button(
    root,
    text='Start',
    font=('calibri',12),
    command = lambda: plot_start()
)
start.place(x=100,y=500)

root.update();
stop = tk.Button(
    root,
    text='Stop',
    font=('calibri',12),
    command = lambda: plot_stop()
)
stop.place(x=start.winfo_x()+start.winfo_reqwidth()+20,y=500)
root.mainloop()
