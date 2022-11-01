from tkinter import *     
from tkinter import messagebox
from PIL import ImageTk, Image

from authorization import login

img_path = "/home/platosha/Desktop/BMSTU/1Msem/AIS/lab3/background.png"

def back():
	output_text.place_forget()
	output_btn.place_forget()

	txt.delete(0, 'end')
	output_text.delete('1.0', END)

	lbl.place(x=412, y=260)
	txt.place(x=413, y=285)
	btn.place(x=400, y=325)


def output_cities(like_cities, dislike_cities, cities):
	lbl.place_forget()
	txt.place_forget()
	btn.place_forget()

	output_text.place(x=290, y=20)
	output_btn.place(x=25, y=500)

	output_text.insert(INSERT, "Любимые города:")
	for i in range(len(like_cities)):
		output_text.insert(INSERT, "\n\t" + like_cities[i]['Город'])

	output_text.insert(INSERT, "\nНелюбимые города:")
	for i in range(len(dislike_cities)):
		output_text.insert(INSERT, "\n\t" + dislike_cities[i]['Город'])

	for i in range(len(cities)):
		output_text.insert(INSERT, "\n----------------------------------------------\n")
		output_text.insert(INSERT, cities[i])


def clicked():   
	user = txt.get()
	like_cities, dislike_cities, cities = login(user)
	if (cities):
		output_cities(like_cities, dislike_cities, cities)
		

def load_image(img_path):
	img = Image.open(img_path)

	width = 1000
	ratio = (width / float(img.size[0]))
	height = int((float(img.size[1]) * float(ratio)))
	imag = img.resize((width, height), Image.ANTIALIAS)
	
	image = ImageTk.PhotoImage(imag)
	return image


window = Tk()  
window.title("Рекомендательная система туров по России")  
window.geometry('1000x554')

image = load_image(img_path)
panel = Label(window, image=image)
panel.pack(side="top", fill="both", expand="no")

lbl = Label(window, text="Введите имя", bg='#96B8E5', width=17)  
lbl.place(x=412, y=260)

txt = Entry(window, width=17)   
txt.place(x=413, y=285)
txt.focus()

btn = Button(window, text="Ввести", activebackground='#545885', bd=3, bg='#7F90C4', height=1, width=17, command=clicked)  
btn.place(x=400, y=325)

output_text = Text(width=48, height=30, wrap=WORD)
output_btn = Button(window, text="Назад", activebackground='#545885', bd=3, bg='#7F90C4', height=1, width=17, command=back)

window.mainloop()
