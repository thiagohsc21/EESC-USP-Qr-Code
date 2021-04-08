from pyzbar import pyzbar
import argparse
import cv2 as cv

#Para decodificar uma imagem, basta digitar no terminal :
#python3 nome_codigo.py --image nome_foto.png

#Define um argumento obrigatório na linha de comando "--image"
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path to input image")
args = vars(ap.parse_args())

#Carrega a imagem da entrada
image = cv.imread(args["image"])

#Localiza o qrcode e o decodifica
barcodes = pyzbar.decode(image)

for barcode in barcodes:

	#Acha a delimitação do Qr Code para com a imagem e a destaca
	(x, y, w, h) = barcode.rect
	cv.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)

	#Converte os bytes do qe para string seguindo o padrão utf-8
	barcodeData = barcode.data.decode("utf-8")
	barcodeType = barcode.type

	#Desenha os dados contidos no QR na imagem 
	text = "{} ({})".format(barcodeData, barcodeType)
	cv.putText(image, text, (x, y - 10), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

	#Printa o tipo do qr code e os dados para no terminal
	print("[INFO] Found {} barcode: {}".format(barcodeType, barcodeData))

#Mostra a imagem na tela
cv.imshow("Image", image)
cv.waitKey(0)
