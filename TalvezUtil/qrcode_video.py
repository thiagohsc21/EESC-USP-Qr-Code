from imutils.video import VideoStream
from pyzbar import pyzbar
import argparse
import datetime
import imutils
import time
import cv

#Argumento da linha de comando 
ap = argparse.ArgumentParser()
ap.add_argument("-o", "--output", type=str, default="resultado.csv", help=".csv em que será armazenado o resultado")
args = vars(ap.parse_args())

#Inicializa o stream de vídeo
print("Começando o vídeo...")
vid = VideoStream(src=0).start() #usa a webcam usb
time.sleep(2.0) #pausa por 2 segundos

#Abre o arquivo CSV para escrita e o set armazenará os códigos de barra
#encontrados, o que evitará duplicatas
csv = open(args["output"], "w")
found = set()

while True:

	#Recebe o framde de vídeo e muda para no máximo 400x400 
	frame = vid.read()
	frame = imutils.resize(frame, width=400)

	#Localiza o QrCode no frame e decodifica-o
	barcodes = pyzbar.decode(frame)

    for barcode in barcodes:
        # extrair o local da caixa delimitadora do código de barras e desenhar
        # a caixa delimitadora que envolve o código de barras na imagem (nesse caso está verde)
        (x, y, w, h) = barcode.rect
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # os dados do código de barras é um objeto de bytes por isso, se queremos desenhá-lo
        # na nossa imagem de saída, precisamos convertê-lo para uma string primeiro
        barcodeData = barcode.data.decode("utf-8")
        barcodeType = barcode.type

        #Desenha os dados contidos no QR na imagem 
        text = "{} ({})".format(barcodeData, barcodeType)
        cv.putText(image, text, (x, y - 10), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        
        #Se o texto do qrcode não estiver no arquivo CSV, escreve
		#o carimbo de data + qrcode e atualiza o set
		if barcodeData not in found:
		    csv.write("{},{}\n".format(datetime.datetime.now(), barcodeData))
			csv.flush()
			found.add(barcodeData)

    #Exibição do vídeo ao vivo
    cv.imshow("Scanner de Qr Code", frame)

    #Comando para dar um break no loop e finalizar o código
    if cv.waitKey(1) == ord('q'):
        break

# feche o arquivo CSV de saída e faça uma limpeza
print("Limpando...")
csv.close()
cv.destroyAllWindows()
vid.stop()

#----------------------#----------------------#----------------------#----------------------
#Caso desejemos usar a câmera da Raspberry Pi, basta substituir a linha 16 pela abaixo
#vs = VideoStream(usePiCamera=True).start() 