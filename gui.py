import tkinter as tk

root = tk.Tk()

def event_tekan():
    label2 = tk.Label(root,text='Program telah diakhiri')
    label2.pack()
def simpan_data():
    textentry = tk.Entry(root, width=20, bg='white')
    textentry.grid(row=2, column=0)
    label3 = tk.Label(root,text='Data telah di simpan !')
    label3.pack()
def click():
    entered_text = texentry.get()

label = tk.Label(root, text='Real Time \n Identification Emotion')
button = tk.Button(root, text='Stop',command = event_tekan)
simpan = tk.Button(root, text='Save',command = simpan_data)
label.pack()
button.pack()
simpan.pack()
root.mainloop()