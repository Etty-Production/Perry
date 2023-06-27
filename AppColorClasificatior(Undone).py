import tkinter
import time
import cv2

class Scroll:
    def __init__(self, frame, xp, yp):
        self.frame = frame
        self.variable = tkinter.DoubleVar()
        scale = tkinter.Scale( self.frame, variable = self.variable, length = 200, from_ = 0, to = 255, orient = tkinter.HORIZONTAL).place(x = xp, y = yp)

    def GetValue(self):
        return int(self.variable.get())

class App:
    """docstring for ClassName"""
    def __init__(self):

        self.Number = 0

        self.root = tkinter.Tk()
        self.root.geometry('500x500')

        # создаем рабочую область
        self.frame = tkinter.Frame(self.root)

        self.label = tkinter.Label(self.root, text="Nothing")
        self.label.place(x = 10, y = 10)
        
        self.Lmin = Scroll(self.root, 10, 0)
        self.Lmax = Scroll(self.root, 10, 40)

        self.Amin = Scroll(self.root, 230, 0)
        self.Amax = Scroll(self.root, 230, 40)

        # вставляем кнопку
        self.but = tkinter.Button(self.root, text="SaveMask", command=self.UpdateText)
        self.but.place(x = 80, y = 10)

      
        self.canvas = tkinter.Canvas(self.root, height=480, width=620)
        self.cap = cv2.VideoCapture(0)
        self.UpdateImage() 

        self.root.mainloop()
       

    def UpdateText(self):
        self.Number += 1
        self.label = tkinter.Label(self.root, text="Nothing"+str(self.Number)).place(x = 200, y = 200)
        print(self.Lmin.GetValue())

    def UpdateImage(self):
        ret = False
        while not ret:
            ret, frame = self.cap.read()

            if ret:
                frame = cv2.resize(frame,(620, 480))
                cv2.imwrite('Buffer.png', frame)


                #Добавим изображение
                self.PngFrame = tkinter.PhotoImage(file = 'Buffer.png') 
                self.image = self.canvas.create_image(0, 0, anchor='nw',image=self.PngFrame)
                self.root.after(33, self.UpdateImage)
                self.canvas.place(x = 10, y = 10)

            

Window = App()
