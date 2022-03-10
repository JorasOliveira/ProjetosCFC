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
        t_i= time.time()   #tempo inicial p/ timeout

        #compondo o head
        '''HEAD: 
        tipo de mensagem - 1 byte (character)
        ordem dos pacotes: numero/total - 2 bytes (numero/numero)
        tamanho da payload - 2bytes (nuemro)
        stuff - 1 byte (charater?) - ff
        5 bytes vazios

        TIPOS DE MENSAGEM:
        HandShake  - a
        Dados      - b
        Acknoledge - c
        FIM        - d
        '''

        #head exemplo p/ teste
        # txBuffer = (n_commands).to_bytes(1,byteorder='big')
        # pacote = ""
        # pacote += 'a' 
        # pacote += '2' 
        # pacote += '48' 
        # pacote += '144' 
        # pacote += '000'

        #carregando a imagem
        imgR = "client/img/dog.jpg"
        print("Loading Image: ")
        print(" - {}".format(imgR))
        dog = open(imgR, 'rb').read()

        print(f"a imagem tem  tamanho: {len(dog)}")

        size_of_dog = int(len(dog)/114) + 1
        print(f"a imagem sera dividida em: {size_of_dog} pacotes")

        #montando o head DO HANDSHAKE:
        size_bytes = size_of_dog.to_bytes(1, byteorder='big')

        bytes_to_number = int.from_bytes(size_bytes, byteorder='big')
        print(bytes_to_number)

        zero = (0).to_bytes(1, byteorder='big')
        a = str.encode('a')
        pacote = a + zero + size_bytes + zero*7     #0{size_of_dog.to_bytes(1, byteorder='big')}000000'
        print(pacote)
        
        #mandando
        time.sleep(0.1)
        txBuffer = pacote
        print(txBuffer)
        time.sleep(0.1)
        com1.sendData(np.asarray(txBuffer))


        #-----P2-----

        # 1- Passando a quantidade de comandos que o server ira passar
        # t_i= time.time()   #tempo inicial p/ timeout
        #mandando o numero de comandos
        # commands = [0b11, 0b00, 1100, 0b0011, 0b1111, 0b1010]
        # n_commands = randint(10, 30)
        # txBuffer = (n_commands).to_bytes(1,byteorder='big')
        # print("mandando {} commandos".format(n_commands))
        # time.sleep(0.1)
        # com1.sendData(np.asarray(txBuffer))

        # 2- Passar o comando em si


        
        #mandando os tamanhos dos comandos
        # sent_commands = []
        # for command in range(n_commands):
        #     time.sleep(0.1)
        #     c = choice(commands)
        #     sent_commands.append(c)
        #     txBuffer = len(c).to_bytes(1,byteorder='big')
        #     print("mandando tamanho: {}".format(command))
        #     print(int.from_bytes(txBuffer, byteorder='big'))
        #     com1.sendData(np.asarray(txBuffer))

        # #mandando os commandos em si
        # for command in range(n_commands):
        #     time.sleep(0.1)
        #     c = sent_commands.pop(0)
        #     # txBuffer = bytes(c, "UTF-8")
        #     txBuffer = c.encode(encoding = 'UTF-8')
        #     print("mandando commando {}".format(command))
        #     print(txBuffer)
        #     com1.sendData(np.asarray(txBuffer))


        # 3- Ficar ouvindo ate receber uma resposta ou ate o time-out de 10 seg

        
        deltaTime = time.time() - t_i
        print("deltaT: {}".format(deltaTime))

        txLen = 1
        rxBuffer, nRx = com1.getData(txLen)
        if rxBuffer.isalpha():
            print("TimeOut :(")
            com1.disable()
            exit()
        rxBuffer = int.from_bytes(rxBuffer, byteorder='big')
        print("recebeu n_commands: {}" .format(rxBuffer))

        if (rxBuffer - n_commands) == 0:
            print("commandos enviados com sucesso!!")
            com1.disable()
            exit()
        else: 
            print("Erro ao enviar os commandos :(") 
            com1.disable()
            exit()

        
    
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
    