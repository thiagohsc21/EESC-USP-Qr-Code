# EESC-USP Qr Code
---
## Tutorial para instalar os itens necessários para o código
* Atualizar o sistema:


&nbsp;
`$ sudo apt-get upgrade`
* Instalar o python3:


&nbsp;
`$ sudo apt-get install python3`
* Instalar o gerenciador de pacotes do python:


&nbsp;
`$ sudo apt-get install python3-pip`
* Instalar a biblioteca OpenCV (para mais detalhes, clique [aqui](https://docs.opencv.org/master/d2/de6/tutorial_py_setup_in_ubuntu.html)):


&nbsp;
`$ sudo apt-get install python3-opencv`

* Instalar a biblioteca pyzbar:


&nbsp;
`$ sudo apt-get install libzbar0`

* Instalar o imutils (provavelmente já o tem, mas execute o comando mesmo assim):


&nbsp;
`$ pip3 install imutils` 

Se estiver usando uma webcam integrada ou a PiCam, pule para a parte em que eu rodo o código. :)

## Tutorial para configurar a câmera como webcam

Antes de realizarmos as operações na câmera, é necessário que ela tenha suporte para LiveView oferecido pelo gphoto2, você pode checar [aqui](http://gphoto.org/proj/libgphoto2/support.php). Algo do tipo deve aparecer ao lado do nome da sua câmera:



&nbsp;
![verificando_liveview](https://user-images.githubusercontent.com/61644143/114025462-8407b980-984b-11eb-954d-049cdc61de6e.png)

* Instalar o gphoto2:


&nbsp;
`$ sudo apt install -y gphoto2`
* Instalar o driver de loopback:


&nbsp;
`$ sudo apt install -y v4l2loopback-utils`
* Instalar o ffmpeg, que realiza codificação e decodificação de vídeo (resumidamente):


&nbsp;
`$ sudo apt install -y ffmpeg`
* Plugue a câmera no USB e digite:


&nbsp;
`$ gphoto2 --auto-detect`
> É necessário que ela tenha sido reconhecida pelo aplicativo
* Liste todos os dispositivos de vídeo digitando:


&nbsp;
`v4l2-ctl --list-devices` ou `ls -ltrh /dev/video*`
> Provavelmente você verá alguns arquivos do tipo /dev/video0 ~ /dev/video1 ~  /dev/video2, esses são os 
> dispositivos (ou dependências) de vídeo conectados ao computador. Não necessariamente cada um desses /dev/videoX são outputs de vídeo

* Digite no terminal ignorando qualquer mensagem de erro: 


&nbsp;
`$ sudo rmmod v4l2loopback`
> Agora liste todos os dispositivos utilizando o passo anterior. É possível que um deles tenha sumido, faz parte do processo.

* Ativação do módulo do kernel ('driver de loopback'):


&nbsp;
`$ sudo modprobe v4l2loopback exclusive_caps=1 max_buffers=2`
> Ele permitirá a criação de um dispositivo de vídeo a partir de sua câmera DSLR.

* Liste todos os dispositivos novamente, utilizando os comandos já passados. 
> Repare que um novo dispositivo (do tipo /dev/videoX) será criado, este será utilizado pelo driver de loopback como nossa webcam virtual e o colocaremos no próximo comando. 

* Comando de captura do vídeo e envio para a webcam virtual:


&nbsp;
`$ gphoto2 --stdout --capture-movie | ffmpeg -i - -vcodec rawvideo -pix_fmt yuv420p -threads 0 -f v4l2 /dev/videoX`
> Não esqueça de substituir o X do /dev/videoX pelo número do novo dispositivo criado. 

* Para fins de teste, abra o VLC > Media > Open Capture Devices > Video Device Name > Escolha "/dev/videoX. 
> Se alguma imagem for gerada, parabéns!

Enquanto fizer uso dessa câmera como webcam, você NÃO pode fechar o terminal em que realizamos tais operações!!!

## Tutorial para rodar o código
1. Baixe o código `qrcode.py` em um diretório específico.
2. Abra o terminal e digite `$ cd nome_do_diretório`
3. Dentro desse direótiro, digite `$ python3 qrcode.py --saida frase.txt`
4. Aponte um Qr Code para a câmera, ele será lido e decodificado.
5. A resposta aparecerá na tela, mas também será gerado um arquivo .txt com a frase identificada.


&nbsp;


Se alguma mensagem de erro referente a não identificação da câmera aparecer, é devido a um detalhe do código. 

Abra `qrcode.py` usando algum editor de texto e nas linhas de código abaixo, substitua o 0 pelo número X em /dev/videoX supracitado.
``` 
    #Iniciar a stream (iniciar a webcam) e permitir que o sensor da câmera aqueça
    print(TC.CYAN+"Iniciando processamento de vídeo..."+TC.WHITE)
    vid = WebcamVideoStream(0).start()
    time.sleep(1.5) 
```

Agora basta prosseguir do passo 3. em diante.


    
   






 
