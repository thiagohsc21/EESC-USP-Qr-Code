import cv2 as cv

def abre_camera():
    
    vid = cv.VideoCapture(0,cv2.CAP_V4L)
    if not vid.isOpened():
        print("Não foi possível abrir a câmera")
        exit(1)

    while(True):

        ret, frame = vid.read()
        if not ret:
            print("Frames não recebidos")
            break
    
        frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        cv.imshow("Vídeo Ao Vivo - Pressione 'q' para sair", frame)

        if cv.waitKey(1) == ord('q'):
            break
        
    vid.release()
    cv.destroyAllWindows()


def grava_camera():

    vid = cv.VideoCapture(0,cv2.CAP_V4L)
    if not vid.isOpened():
        print("Não foi possível abrir a câmera")
        exit(1)

    fourcc = cv.VideoWriter_fourcc ('X', 'V', 'I', 'D')
    out = cv.VideoWriter ( "gravacao.avi" , fourcc, 15.0, (640, 480), 0)

    while(True):

        ret, frame = vid.read()
        if not ret:
            print("Frames não recebidos")
            break
        
        frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        out.write (frame)
        cv.imshow("Vídeo Ao Vivo - Pressione 'q' para sair", frame)

        if cv.waitKey(1) == ord('q'):
            break

    vid.release()
    out.release()
    cv.destroyAllWindows()


if __name__ == "__main__":
    

