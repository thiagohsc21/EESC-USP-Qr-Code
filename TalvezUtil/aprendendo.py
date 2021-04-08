import cv2 as cv

#inicia a captura de vídeo, sendo o parâmetro () a câmera que utilizaremos VideoCapture(0,1,2,..) ou  
#o arquivo passado como input VideoCapture("video_input.avi")
vid = cv.VideoCapture(0,cv2.CAP_V4L)
if not vid.isOpened():
    print("Não foi possível abrir a câmera")
    exit(1)

#Código de 4bytes que especifica o codec de vídeo ~ o escolhido foi XVID (não sei o motivo)
#Um codec de vídeo é um programa que permite comprimir e descomprimir um vídeo digital
fourcc = cv.VideoWriter_fourcc ('X', 'V', 'I', 'D')

#(nome_output, codigo_fourcc, taxa_fps, tamanho(A,B), cor (1 colorido e 0 cinza))
out = cv.VideoWriter ( "gravacao.avi" , fourcc, 15.0, (640, 480), 0)

while(True):

    #realiza a leitura do vídeo quadro a quadro e armazena no frame e ret (não sei q porra é ret)
    ret, frame = vid.read()

    #Sai de 640x480 e passa a ser 320x240 - Câmera Buga
    #ret = vid.set(cv.CAP_PROP_FRAME_WIDTH,480)
    #ret = vid.set(cv.CAP_PROP_FRAME_HEIGHT,480)

    #se o quadro for lido corretamente, ret = True
    if not ret:
        print("Não pudemos receber os frames (stream acabou?). Saindo ...")
        break
    
    #converte o frame pra cinza
    frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    #define o output como sendo o frame 
    out.write (frame)

    #Exibição do vídeo ao vivo
    cv.imshow("Vídeo Ao Vivo - Pressione 'q' para sair", frame)

    #Comando para dar um break no loop e finalizar o código
    if cv.waitKey(1) == ord('q'):
        break

#Quando tudo estiver OK, libera a capture
vid.release()
#Libera 
out.release()
#Fecha tudo
cv.destroyAllWindows()

# Possibilidades Input()
# 1) Realizar a gravação enquanto sobrevoamos o QR Code e após isso, passar esse vídeo como input pro código
# 2) Utilizar a imagem ao vivo da câmera embarcada
# 3) Tirar foto automaticamente a cada X segundos enquanto passamos elas como input para o código
# 4) Tirar foto manualmente e passar para o código