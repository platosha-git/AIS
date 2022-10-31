from tkinter import *     
from tkinter import messagebox
from PIL import ImageTk, Image

def clicked():   
	messagebox.showinfo('Заголовок', 'Текст') 
	res = "Привет {}".format(txt.get())  
	lbl.configure(text=res)      

window = Tk()  
window.title("Добро пожаловать в приложение PythonRu")  
window.geometry('500x450')  

img = Image.open('/home/platosha/Images/Обои/4')
width = 500
ratio = (width / float(img.size[0]))
height = int((float(img.size[1]) * float(ratio)))
imag = img.resize((width, height), Image.ANTIALIAS)
image = ImageTk.PhotoImage(imag)
#panel.pack(side="top", fill="both", expand="no")



lbl = Label(window, text="Привет", image=image)  
#lbl.grid(column=0, row=0)  
lbl.pack(side="top")

txt = Entry(window, width=10)  
#txt.grid(column=1, row=0)  
txt.pack()
txt.focus()

btn = Button(window, text="Не нажимать!", command=clicked)  
btn.place(x=250, y=250)
#btn.grid(column=0, row=1)  
#btn.pack(ipadx=10, ipady=10)

window.mainloop()
