import cv2
from tkinter import *
import _thread
from openalpr import Alpr
#-------------------PRE CONFIG-------------------

#Seleciona o país e os arquivos padrões para funcionamento do framework
alpr = Alpr("br", "openalpr.conf.defaults", "runtime_data")

#Seleciona o número de placas que serão lidas
alpr.set_top_n(20)

#Seleciona o padrão da região
alpr.set_default_region("br")

#-------------------FUNCTIONS-------------------

def detect(img):
    img_str = cv2.imencode('.jpg', img)[1].tostring()
    results = alpr.recognize_array(img_str)
    for plate in results['results']:
        cv2.putText(img, plate['plate'], (plate['coordinates'][0]['x'], plate['coordinates'][0]['y'] - 5), 0, 1, (255, 0, 0), 3)
        cv2.rectangle(img, (plate['coordinates'][0]['x'], plate['coordinates'][0]['y']), (plate['coordinates'][2]['x'], plate['coordinates'][2]['y']), (0, 255, 0), 2 )
    print(results)
    return img
    
def show_frame():
    th = _thread.start_new(video_stream, ())

def video_stream():
    cap = cv2.VideoCapture(streamSrc.get())
    streamName = streamSrc.get()
    while(True):
        ret, frame = cap.read()
        frame = detect(frame)
        cv2.imshow(streamName, frame)
        if cv2.waitKey(1) and 0xFF == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            break


#-------------------MAIN FRAME-------------------
root = Tk()

root.geometry('600x600+200+200')
root.wm_title("Alpr")

#-------------------DETECT FRAME-------------------
detectsframe = LabelFrame(root, text= "Detecções")
detectsframe.place(relwidth=1, relheight=0.5)

plateTxtframe = LabelFrame(detectsframe, text= "Placa Detectada")
plateTxtframe.place(relwidth=0.5, relheight=0.5)

plateTxtlabel = Label(plateTxtframe, text= "AAA0000", font=("Arial", 14))
plateTxtlabel.place(relx=0.5, rely=0.5, anchor ='center')

plateImgframe = LabelFrame(detectsframe, text= "Imagem Placa")
plateImgframe.place(relx = 0.5, relwidth=0.5, relheight=0.5)

#-------------------CONFIG FRAME-------------------

configframe = LabelFrame(root, text= "Configurações")
configframe.place(relwidth=1, relheight=0.6, rely =0.4)

streamframe = LabelFrame(configframe, text= "Stream")
streamframe.place(relwidth=1, relheight=0.2)

streamSrc = Entry(streamframe)
streamSrc.place(relwidth=0.75, relheight=0.6, relx = 0, rely = 0.15)

streamStartBnt = Button(streamframe, text='Start', command =show_frame)
streamStartBnt.place(relwidth=0.25, relheight=0.6, relx = 0.75, rely = 0.15)

#-------------------FIREBASE FRAME-------------------

firebframe = LabelFrame(configframe, text= "FireBase")
firebframe.place(relwidth=1, relheight=0.8, rely =0.2)

#-------------------START APP-------------------
root.mainloop()


