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
from datetime import datetime
from email import message
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
        h0 - tipo
        h1 - 
        h2 - 
        h3 - numero total de pacotes
        h4 - numero do pacote enviado
        h5 - se tipo == handshake: id, se tipi == dados: tamanho da payload
        h6 - pacote solicitado para recomeco quadno tem erro no envio
        h7 - ultimo pacote recebido com sucesso
        h8 - CRC
        h9 - CRC

        TIPOS DE MENSAGEM:
        1 - inicio de transmissao, h0 = 1, h1 = identificador do server
        2 - enviada pelo server, resposta do handhsake
        3 - dados, contem o numero do ultimo pacote recebido, e o total a ser enviado
        4 - acknowledge, contem o numero do ultimo pacote recebido
        5 - timeout, deve finalizar a conecsao
        6 - erro, deve conter o numero do pacote esperado pelo server, nao importa o problema
        '''
        #carregando a imagem

        imgR = "client/img/dog.jpg"
        print("Loading Image: ")
        print(" - {}".format(imgR))
        dog = open(imgR, 'rb').read()

        print(f"a imagem tem  tamanho: {len(dog)}")
        size_of_dog = int(len(dog)/114) + 1
        print(f"a imagem sera dividida em: {size_of_dog} pacotes")

        eop = [0xAA, 0xBB, 0xCC, 0xDD]

        def writeLog(head):

            if head[0] == 4:
                message = str(datetime.now()) + " /" + str(head[0]) + " /" +str(head[5])
            else: #h3 - numero total de pacotes ; h4 - pacote atual; h5 size; 
                message = str(datetime.now()) + " /" + str(head[0]) + " /" + str(head[5]) + " /" + str(head[4]) + " /" + str(head[3])

            log = "client/log/Client2.txt"
            with open(log, 'a') as f:
                f.write(message)
                f.write('\n')



            # return "lol"
        #eh o handhsake, enviada pelo client para ver se pode comecar a transmissao
        #tipo 2 eh a resposta do handshake, eh recebida pelo client
        def type_1():
            #lista de ints, cada int sera escrito como um byte quando byte(l)
            #lista do head
            l = [1, 0, 0, size_of_dog, 0, 10, 0, 0, 0, 0]       
            #fazemos uma lista de bytes com a lista de ints, cada byte tem tamanho e posicao igual ao do int equivalente na lista
            handshake = bytes(l + eop) 
            pacote = handshake  #temporario     

            #mandando o HandShake:
           # print("mandando o handhshake")
            txBuffer = pacote
            #print(f"enviando: {txBuffer}")
            time.sleep(0.1)
            com1.sendData(np.asarray(txBuffer))
            writeLog(l)
            print("mandando o handhshake")
            print(f"handhsake: {list(pacote)}")

        
        #manda a imagem, monta o pacote baseado no index recebido
        #TODO re-escrever o codigo 
        #tipo 3 eh a mensagem de dados, o client envia os dados e escuta uma resposta
        def type_3(i):
            #print("sending")
            #variando o tamanho da payload quando chegamos no ultimo pacote
            if i == 1:
                i = 0
                k = 1
            else: k = i  
            try:
                h = [3, 0, 0, size_of_dog, k, 114, 0, 0, 0, 0]
                pacote = bytes(h + list(dog[114*i: 114*(i+1)]) + eop)

            #no ultimo pacote, teremos erro de index out of range, dai usamos o except
            except: 
                size = len(list(dog[114*i: -1]))

                h = [3, 0, 0, size_of_dog, k, size, 0, 0, 0, 0]
                pacote = bytes(h + list(dog[114*i: -1]) + eop)
                
            
            txBuffer = pacote
            print(f"enviando dados: {list(txBuffer)}")
            time.sleep(0.1)
            com1.sendData(np.asarray(txBuffer))
            writeLog(h)
        
        #TODO envia uma mensagem tipo 5, e corta a conecao
        def type_5():
            h = [5, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            pacote = bytes(h + eop)

            txBuffer = pacote
            print(txBuffer)
            time.sleep(0.1)
            com1.sendData(np.asarray(txBuffer))
            writeLog(h)
        
            print("TIME OUT")
            print(":(")
            com1.disable()

        def handler(i): #handles o recebimento
            print("ouvindo o recebimento")
            #timers: a == timer 1, b == timer 2
            t_i_1 = time.time()
            t_i_2 = time.time()
            timer_1 = 0
            timer_2 = 0
            l = 0
            while l < 10:
                l = com1.rx.getBufferLen()
                timer_1 = time.time() - t_i_1
                timer_2 = time.time() - t_i_2

                if timer_1 >= 5:
                    t_i_1 = 0
                    print("re-enviando o pacote de dados")
                    type_3(i - 1) #para ser o pacote correto
                    
                if timer_2 >= 20:
                    type_5()
                
            #l = 10  
            if l >= 10:
                txLen = 10
                time.sleep(0.1)
                rxBuffer, nRx = com1.getData(txLen) #pegando o HEAD, 1 = timer 1, 5 segundos
                #print(f"recebido: {list(rxBuffer)}")

                rxBuffer = list(rxBuffer)
                codigo = rxBuffer[0]
                pacote_correto = rxBuffer[6]
                print(f"codigo: {codigo}")
                writeLog(rxBuffer)

            txLen = 4
            time.sleep(0.1)
            rxBuffer, nRx = com1.getData(txLen)

            print(f"eop: {list(rxBuffer)}")

            if codigo == 2:
                return (True, pacote_correto)

            elif codigo == 4:
                return (True, pacote_correto)

            elif codigo == 5:
                type_5()
                
            else:
                return (False, pacote_correto)

        #mcomecando a transmissao:
        start = False
        while(start is False):
            type_1()
            time.sleep(5) 
            start = handler(0)
            if not start[0]:
                print("HandShake ERROR, retrying")

        if start:
            acabou = False
            i = 1
            while not acabou:
                if i <= size_of_dog:

                    if i > 1:
                        #bol,     int
                        next_pkg, ultimo_pacote = handler(i) #que burro, reescreva
                    else: 
                        next_pkg = True
                        ultimo_pacote = 1
                    
                    if not next_pkg:
                        i = ultimo_pacote

                    if next_pkg or i == 0:
                        type_3(i)
                        i += 1


                else: 
                    acabou = True
                    print("Terminou! :)")
                    com1.disable()

            






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

    # answer = int(input("Client(0.1) or Server(0)?"))

    # if answer is 1:
    #     print("client")

    # if answer is not 1:
    #     print("server")

    # ready = input("Press ENTER when ready")
    # main(answer)
    