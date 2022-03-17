#####################################################
# Camada Física da Computação
#Carareto
#11/08/2020
#Aplicação
####################################################


#esta é a camada superior, de aplicação do seu software de comunicação serial UART.
#para acompanhar a execução e identificar erros, construa prints ao longo do código! 


from base64 import decode
from calendar import c
from http import client, server
from sys import byteorder
from enlace_Client import *
import time
import numpy as np
from random import randint, choice
# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM4"                  # Windows(variacao de)

def main():
    try:
        #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        #para declarar esse objeto é o nome da porta.
        com1 = enlace('COM4')
        
        # Ativa comunicacao. Inicia os threads e a comunicação seiral 
        com1.enable()
        #Se chegamos até aqui, a comunicação foi aberta com sucesso. Faça um print para informar.
        print("Communication Successfull!")

        #aqui você deverá gerar os dados a serem transmitidos. 
        #seus dados a serem transmitidos são uma lista de bytes a serem transmitidos. Gere esta lista com o 
        #nome de txBuffer. Esla sempre irá armazenar os dados a serem enviados.


        #-----P3-----
         # 1- mandando o head
        #t_i= time.time()   #tempo inicial p/ timeout

        #compondo o head
        '''HEAD: 
        tipo de mensagem - 1 byte (character)
        ordem dos pacotes: numero/total - 2 bytes (numero/numero)
        tamanho da payload - 2bytes (nuemro)
        stuff - 1 byte (charater?) - ff
        5 bytes vazios

        TIPOS DE MENSAGEM:
        HandShake  - 10
        Dados      - 20
        Acknowledge- 30
        Resend     - 40 
        FIM        - 50
        '''
        #carregando a imagem
        imgR = "client/img/dog.jpg"
        print("Loading Image: ")
        print(" - {}".format(imgR))
        dog = open(imgR, 'rb').read()

        print(f"a imagem tem  tamanho: {len(dog)}")
        size_of_dog = int(len(dog)/114) + 1
        print(f"a imagem sera dividida em: {size_of_dog} pacotes")

        eop = [85, 85, 85, 85]

        #le o acknowledge e checa se ta correto:
        def acknowledge():
            txLen = 10
            (0.01)
            rxBuffer, nRx = com1.getData(txLen)
            print(f"head: {list(rxBuffer)}")

            if isinstance(rxBuffer, str):
                print("error timeout")
                return False

            index = rxBuffer[0]
            n_pacotes = rxBuffer[1]
            print(f"codigo: {index}")
            print(f"numero do pacote: {n_pacotes}")

            txLen = 4
            (0.01)
            rxBuffer, nRx = com1.getData(txLen)

            print(f"eop: {list(rxBuffer)}")
            if eop != list(rxBuffer):
                return False

            if index == 30:
                print("works")
                #tira o EOP do buffer e retorna
                txLen = 4
                rxBuffer, nRx = com1.getData(txLen)
                return True
                
                #apenas para testes quando nao tem outro pc
                # if rxBuffer[0] == 10:
                #     #tira o EOP do buffer e retorna
                #     txLen = 4
                #     rxBuffer, nRx = com1.getData(txLen)
                #     return True

            elif index == 40:
                print("data error")
                return 'f'
                    #chama a si mesmo e checa o aknowledge, idealmente sempre vai retornar a menos que tenha um loop
                    #infinito de 40 como resposta :/
                acknowledge()
                    #tira o EOP do buffer e retorna
                txLen = 4
                rxBuffer, nRx = com1.getData(txLen)
                return True

            else:
                print("FUCK")
                #tira o EOP do buffer e retorna
                txLen = 4
                rxBuffer, nRx = com1.getData(txLen)
                return False

        #manda a imagem, monta o pacote baseado no index recebido
        def send_img(i):
            print("sending")
            #variando o tamanho da payload quando chegamos no ultimo pacote
            try: 
                h = [20, i+1, size_of_dog, 114, 0, 0, 0, 0, 0, 0]
                pacote = bytes(h + list(dog[114*i: 114*(i+1)]) + eop)

            #no ultimo pacote, teremos erro de index out of range, dai usamos o except
            except: 
                h = [20, i+1, size_of_dog, 114, 0, 0, 0, 0, 0, 0]
                pacote = bytes(h + list(dog[114*i: -1]) + eop)

            #print(pacote[3])
            txBuffer = pacote
            print(txBuffer)
            (0.01)
            com1.sendData(np.asarray(txBuffer))



        def handshake():
            #lista de ints, cada int sera escrito como um byte quando byte(l)
            #lista do head
            l = [10, 0, size_of_dog, 0, 0, 0, 0, 0, 0, 0]       
            #fazemos uma lista de bytes com a lista de ints, cada byte tem tamanho e posicao igual ao do int equivalente na lista
            handshake = bytes(l + eop) 
            pacote = handshake  #temporario     

            #mandando o HandShake:
            txBuffer = pacote
            #print(f"enviando: {txBuffer}")
            (0.01)
            com1.sendData(np.asarray(txBuffer))

            if acknowledge():
                return True
            else: return False
        

        #mandando a imagem:
        start = handshake()
        while(start is False):
            print("HandShake ERROR, retrying")
            start = handshake()
            
        if start:
            acabou = False
            i = 0
            while not acabou:
                if i < size_of_dog:
                    if i > 0:
                        help  = acknowledge()
                    else: help = True

                    if isinstance(help, str):
                        send_img(i -1)

                    if help:
                        send_img(i)
                        i += 1
                        (0.01)

                    else: 
                        print("waiting for Acknowledge...")

                else : acabou = True






        #-----P2-----

        # 1- Passando a quantidade de comandos que o server ira passar
        # t_i= time.time()   #tempo inicial p/ timeout
        #mandando o numero de comandos
        # commands = [0b11, 0b00, 1100, 0b0011, 0b1111, 0b1010]
        # n_commands = randint(10, 30)
        # txBuffer = (n_commands).to_bytes(1,byteorder='big')
        # print("mandando {} commandos".format(n_commands))
        # 
        # com1.sendData(np.asarray(txBuffer))

        # 2- Passar o comando em si


        
        #mandando os tamanhos dos comandos
        # sent_commands = []
        # for command in range(n_commands):
        #     
        #     c = choice(commands)
        #     sent_commands.append(c)
        #     txBuffer = len(c).to_bytes(1,byteorder='big')
        #     print("mandando tamanho: {}".format(command))
        #     print(int.from_bytes(txBuffer, byteorder='big'))
        #     com1.sendData(np.asarray(txBuffer))

        # #mandando os commandos em si
        # for command in range(n_commands):
        #     
        #     c = sent_commands.pop(0)
        #     # txBuffer = bytes(c, "UTF-8")
        #     txBuffer = c.encode(encoding = 'UTF-8')
        #     print("mandando commando {}".format(command))
        #     print(txBuffer)
        #     com1.sendData(np.asarray(txBuffer))


        # 3- Ficar ouvindo ate receber uma resposta ou ate o time-out de 10 seg

        
        # deltaTime = time.time() - t_i
        # print("deltaT: {}".format(deltaTime))

        # txLen = 1
        # rxBuffer, nRx = com1.getData(txLen)
        # if rxBuffer.isalpha():
        #     print("TimeOut :(")
        #     com1.disable()
        #     exit()
        # rxBuffer = int.from_bytes(rxBuffer, byteorder='big')
        # print("recebeu n_commands: {}" .format(rxBuffer))

        # if (rxBuffer - n_commands) == 0:
        #     print("commandos enviados com sucesso!!")
        #     com1.disable()
        #     exit()
        # else: 
        #     print("Erro ao enviar os commandos :(") 
        #     com1.disable()
        #     exit()

        
    
        #faça aqui uma conferência do tamanho do seu txBuffer, ou seja, quantos bytes serão enviados.
       
            
        #finalmente vamos transmitir os tados. Para isso usamos a funçao sendData que é um método da camada enlace.
        #faça um print para avisar que a transmissão vai começar.
        #tente entender como o método send funciona!
        #Cuidado! Apenas trasmitimos arrays de bytes! Nao listas!
  
        #txBuffer = #dados

        # com1.sendData(np.asarray(txBuffer))

        # A camada enlace possui uma camada inferior, TX possui um método para conhecermos o status da transmissão
        # Tente entender como esse método funciona e o que ele retorna

        # txSize = com1.tx.getStatus()

        #Agora vamos iniciar a recepção dos dados. Se algo chegou ao RX, deve estar automaticamente guardado
        #Observe o que faz a rotina dentro do thread RX
        #print um aviso de que a recepção vai começar.

      
        #Será que todos os bytes enviados estão realmente guardadas? Será que conseguimos verificar?
        #Veja o que faz a funcao do enlaceRX  getBufferLen

        #--------------

    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()


        

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()

    # answer = int(input("Client(1) or Server(0)?"))

    # if answer is 1:
    #     print("client")

    # if answer is not 1:
    #     print("server")

    # ready = input("Press ENTER when ready")
    # main(answer)
    