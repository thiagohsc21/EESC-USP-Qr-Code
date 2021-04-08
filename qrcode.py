from imutils.video import WebcamVideoStream
from pyzbar import pyzbar
import argparse, datetime, imutils, time, cv2

class TC:
    RED     = '\033[31m'
    GREEN   = '\033[32m'
    CYAN    = '\033[36m'
    WHITE   = '\033[37m'


#Construir o analisador de argumentos e analisar os argumentos
ap = argparse.ArgumentParser()
ap.add_argument("-o", "--saida", type=str, default="frase.txt", help=".txt que salvaremos a saída")
args = vars(ap.parse_args())

#Iniciar a stream (iniciar a webcam) e permitir que o sensor da câmera aqueça
print(TC.CYAN+"Iniciando processamento de vídeo..."+TC.WHITE)
vid = WebcamVideoStream(0).start()
time.sleep(1.5)

#Abre o arquivo .txt e cria um set, de modo a não repetirmos os elementos
txt = open(args["saida"], "w")
found = set()

#Repetição para continuarmos rodando o vídeo
while True:

    #Lê o vídeo e o redimensiona para 400x400
    frame = vid.read()
    frame = imutils.resize(frame, width=400)
    #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    #Encontra o Qr Code nos frames e os decodifica
    barcodes = pyzbar.decode(frame)

    #Repetição para busca de barcodes
    for barcode in barcodes:

        #Destaca a delimitação do Qr Code usando a cor vermelha
        (x, y, w, h) = barcode.rect
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)

        #Como os dados do Qr são bytes, precisamos converter para uma string (padrão utf-8) antes
        barcodeData = barcode.data.decode("utf-8")

        #Desenha os dados contidos no QR na imagem 
        text = "{}".format(barcodeData)
        cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

        #Se o texto do qrcode não estiver no arquivo .txt, adiciona-o
        if barcodeData not in found:
            txt.write("{}\n".format(barcodeData))
            txt.flush()
            found.clear()
            found.add(barcodeData)
            print(TC.GREEN+"Os dados do Qr Code foram extraídos com sucesso!"+TC.WHITE)

    #Exibição do vídeo ao vivo
    cv2.imshow("Pressione 'esc' para encerrar", frame)

    #Comando para dar um break no loop e finalizar o código
    if cv2.waitKey(1) == 27:
        break

if len(found) == 0:
    print(TC.RED+"Infelizmente nenhum Qr Code foi detectado."+TC.WHITE)

txt.close()
cv2.destroyAllWindows()
vid.stop()

#----------------------#----------------------#----------------------#-------------------------#-------------------------#---
#Caso desejemos usar a câmera da Raspberry Pi, basta substituir a linha 16 pela abaixo
#vid = VideoStream(usePiCamera=True).start() 