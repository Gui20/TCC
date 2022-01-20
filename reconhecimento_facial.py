import face_recognition
import cv2
import numpy as np
import glob

video_capture = cv2.VideoCapture(0)

path = glob.glob("moradores/*.jpeg")

face_encoding = []
known_face_encodings = []
known_face_names = []

for pessoas in path:
    images = face_recognition.load_image_file(pessoas)

    face_encoding = face_recognition.face_encodings(images)[0]

    #vetor que armazena os pesos das imagens de rostos conhecidos
    known_face_encodings.append(face_encoding)

    names = str(pessoas[10:len(pessoas)-5])

    #Vetor que armazena os nomes das pessoas conhecidas
    known_face_names.append(names)


# Inicialização de algumas variáveis
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True


print(known_face_encodings)
print(known_face_names)
while True:
    # Capturar frames do video
    ret, frame = video_capture.read()

    # Reajuste do frame extraído do video para 1/4 de forma que o precessamento ocorra de forma mais rápida 
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Converte a imagem de BGR para RGB  
    rgb_small_frame = small_frame[:, :, ::-1]

    # Processa outros frames do video
    if process_this_frame:
        # Encontra todas as faces e características no video capturado 
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # Verifica se o rosto é igual a algum outro do banco de dados
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            #Verifica a melhor comparação 	       	
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]
                print("Acesso Liberado")
                
            face_names.append(name)

    process_this_frame = not process_this_frame


    # Apresenta os resultados
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Pega os frame que foram antes reajustados e transforma de novo ao tamanho original
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Desenha o retângulo em torno da face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Escreve o nome ao lado do retângulo 
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Mostra o resultado 
    cv2.imshow('Video', frame)

    # Pressione 'q' para finalizar o programa
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


video_capture.release()
cv2.destroyAllWindows()
