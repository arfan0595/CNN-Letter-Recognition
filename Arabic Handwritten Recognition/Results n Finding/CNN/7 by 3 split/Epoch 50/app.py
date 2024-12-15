import customtkinter
import tkinter as tk
from tkinter import *
from customtkinter import*
import tkinter.font as tkFont
from tkinter import filedialog
import win32gui
from PIL import ImageGrab, Image, ImageTk
import numpy as np
from keras.models import load_model
import cv2


arabic_characters =list('ابتثجحخدذرزسشصضطظعغفقكلمنهوي')
arabic_chars = ['alef', 'beh', 'teh', 'theh', 'jeem', 'hah', 'khah', 'dal', 'thal',
                'reh', 'zain', 'seen', 'sheen', 'sad', 'dad', 'tah', 'zah', 'ain',
                'ghain', 'feh', 'qaf', 'kaf', 'lam', 'meem', 'noon', 'heh', 'waw', 'yeh']


class application(Frame):
    def __init__(self,master):
        super().__init__(master)
        self.fontStyle = tkFont.Font(family="Roboto", size=17)
        self.master=master
        self.master.geometry("1000x650")
        self.pack()
        self.createWidget()

    def createWidget(self):
        self.canvas = Canvas(self,width=400,height=400,bg='black')
        self.canvas.pack(expand=YES, fill=BOTH)
        self.canvas.bind('<Button-1>',self.activate_paint)

    def activate_paint(self, event):
        global lastx, lasty
        self.canvas.bind('<B1-Motion>', self.paint)
        lastx, lasty = event.x, event.y

    def paint(self,event):
        global lastx, lasty
        x, y = event.x, event.y
        self.canvas.create_line((lastx, lasty, x, y), width=14, fill='#ffb703')

        lastx, lasty = x, y

    def clearCanvas(self):
        self.canvas.delete("all")
        answer.configure(text='Prediction Will Be Displayed Here', font=self.fontStyle)
        self.canvas.bind('<B1-Motion>',self.activate_paint)

    def predicted_result(self, data):
        ans = data.argsort()[-8:][::-1]  #sorting in descending
        return ans

    def predictLetter(self):
        HWND = self.canvas.winfo_id()  # get the handle of the canvas
        rect = win32gui.GetWindowRect(HWND)  # get the coordinate of the canvas
        im = ImageGrab.grab(rect) # get image of the current location
        im.save('file.png')

        img = Image.open('file.png').convert('L')
        img = img.resize((32,32))
        img.save('resized.png')

        #after resizing the image data
        #convert to np array

        data = np.array(img)
        data = data/255.0 # for range b/w 0-1
        data = data.reshape(1, 32, 32, 1).astype('float32')

        #import the model
        model_cnn = r'c:\Users\arfan\OneDrive\Desktop\Sem 6\CSP650\Results n Finding\CNN\7 by 3 split\Epoch 50\CNN_Epoch50_(7.3).h5'

        model = load_model(model_cnn)
        result = model.predict(data)
        ans = arabic_characters[np.argmax(result)]
        ans2 = arabic_chars[np.argmax(result)]

        answer.configure(text='Predicted Letter : '+ '(' + ans + ') '+ ans2, font=self.fontStyle)
    
    def open_image(self):
    # Open a file dialog to select an image
        filename = filedialog.askopenfilename(title="Select Image",
                           filetypes=(("png images","*.png"),("jpg images","*.jpg")))
        img = Image.open(filename)
        img = img.resize((32,32))
        img.save('resized.png')
        #after resizing the image data
        #convert to np array

        data = np.array(img)
        data = data/255.0 # for range b/w 0-1
        data = data.reshape(1, 32, 32, 1)
        data = data.astype('float32')

        #import the model
        model_cnn = r'c:\Users\arfan\OneDrive\Desktop\Sem 6\CSP650\Results n Finding\CNN\7 by 3 split\Epoch 50\CNN_Epoch50_(7.3).h5'

        model = load_model(model_cnn)
        result = model.predict(data)
        ans = arabic_characters[np.argmax(result)]
        ans2 = arabic_chars[np.argmax(result)]

        answer.configure(text='Predicted Letter : '+ '(' + ans + ') '+ ans2, font=self.fontStyle)



if __name__ == '__main__':
    root = CTk()
    root.geometry('300x400')
    root.title("Arabic Handwritten Letter Recognition")
    set_appearance_mode("dark")
    #customtkinter.set_default_color_theme(r"C:\Users\arfan\OneDrive\Desktop\Sem 6\CSP650\Results n Finding\CNN\7 by 3 split\Epoch 50\app\Oceanix.json")

    app=application(root)

    clear = CTkButton(root, text='Clear', command=app.clearCanvas, corner_radius=15, fg_color="transparent", hover_color="#830707", border_color="#F72C2C", border_width=1.3, font=("Roboto",15), text_color="#FFFFFF")
    clear.pack(pady=12, padx=10)

    predict = CTkButton(root, text='Predict', command=app.predictLetter, corner_radius=15, fg_color="transparent", hover_color="#259352", border_color="#36D677", border_width=1.3, font=("Roboto",15), text_color="#FFFFFF")
    predict.pack(pady=2, padx=10)

    open_file_button = CTkButton(root, text='Open Image', command=app.open_image, corner_radius=15, fg_color="transparent", hover_color="#BC9916", border_color="#FCC600", border_width=1.3, font=("Roboto",15), text_color="#FFFFFF")
    open_file_button.pack(pady=12, padx=10)

    answer = Label(root, text="Prediction Will Be Displayed Here", fg="#FFFFFF", font=app.fontStyle, bg="#242424")
    answer.pack(pady=12, padx=10)

    root.mainloop()


   