from tkinter import *     
from tkinter import messagebox
from PIL import ImageTk, Image

img_path = "/home/platosha/Desktop/BMSTU/1Msem/AIS/background.png"

def load_image():
	img = Image.open(img_path)

	width = 1000
	ratio = (width / float(img.size[0]))
	height = int((float(img.size[1]) * float(ratio)))
	imag = img.resize((width, height), Image.ANTIALIAS)
	
	image = ImageTk.PhotoImage(imag)
	return image

def clicked():   
	#messagebox.showinfo('Заголовок', 'Текст') 
	res = "Привет {}".format(txt.get())  
	lbl.configure(text=res)      

window = Tk()  
window.title("Рекомендательная система туров по России")  
window.geometry('1000x554')

image = load_image()
panel = Label(window, image=image)
panel.pack(side="top", fill="both", expand="no")

lbl = Label(window, text="Введите имя", width=17)  
lbl.place(x=412, y=260)

txt = Entry(window, width=17)   
txt.place(x=412, y=290)
txt.focus()

btn = Button(window, text="Ввести", activebackground='#545885', bd=3, bg='#7F90C4', height=1, width=17, command=clicked)  
btn.place(x=400, y=325)

window.mainloop()