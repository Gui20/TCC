import cv2

from openalpr import Alpr

#Seleciona o país e os arquivos padrões para funcionamento do framework
alpr = Alpr("br", "openalpr.conf.defaults", "runtime_data")

#Seleciona o número de placas que serão lidas
alpr.set_top_n(20)

#Seleciona o padrão da região 
alpr.set_default_region("br")

#Define a variável que acessa a webcam
cap = cv2.VideoCapture(0)

#Lendo arquivo com as strings das placas
placas = []
arquivo = open('placas.txt','r')
for linha in arquivo:
    linha = linha.rstrip()
    placas.append(linha)
arquivo.close()

#Loop para captura das imagens e reconhecimento em tempo real
while True:
    #Abre a webcam
    ret, img = cap.read()

    #Transforma as imagens capturadas em String
    img_str = cv2.imencode('.jpg', img)[1].tostring()

    #Reconhecendo imagem local 
    results = alpr.recognize_array(img_str)

    #Desenhando retângulo na placa
    for plate in results['results']:

        cv2.putText(img, plate['plate'], (plate['coordinates'][0]['x'], plate['coordinates'][0]['y'] - 5), 0, 1, (255, 0, 0), 3)
        cv2.rectangle(img, (plate['coordinates'][0]['x'], plate['coordinates'][0]['y']), (plate['coordinates'][2]['x'], plate['coordinates'][2]['y']), (0, 255, 0), 2 )

        print("{} com taxa de confiança de {}".format(plate['plate'], plate['confidence']))
        for p in placas:
     	     if plate['plate'] == p:
     	         print("Acesso Liberado!")
                
    cv2.imshow('img', img)

    key = cv2.waitKey(1)

    #Finaliza o loop ao apertar ESC
    if key == 27:
        break


