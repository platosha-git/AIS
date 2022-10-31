from tkinter import *     
from tkinter import messagebox
from tkinter import scrolledtext
from PIL import ImageTk, Image

img_path = "/home/platosha/Desktop/BMSTU/1Msem/AIS/background.png"

def show_image():
	img = Image.open(img_path)
	
	width = 1000
	ratio = (width / float(img.size[0]))
	height = int((float(img.size[1]) * float(ratio)))
	imag = img.resize((width, height), Image.ANTIALIAS)

	image = ImageTk.PhotoImage(imag)
	return image
	

def clicked():   
	messagebox.showinfo('Заголовок', 'Текст') 
	res = "Привет {}".format(txt.get())  
	lbl.configure(text=res)      

def widget():
	window = Tk()  
	window.title("Рекомендательная система туров по России")  
	window.geometry('1000x554')

	image = show_image()

	canvas = Canvas(window, width=1000, height=554)
	canvas.pack(side="top", fill="both", expand="no")
	canvas.create_image(0, 0, anchor="nw", image=image)


	btn = Button(window, text="Ввести", command=clicked)  
	btn.place(x=400, y=310)
	canvas.create_window((250, 250), anchor="nw", window=btn)
	#canvas.create_text(100, 100, text="Cat", fill="Yellow", font="Verdana 14")


	window.mainloop()
