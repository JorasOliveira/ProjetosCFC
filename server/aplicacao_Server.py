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
from itertools import count
from operator import index, indexOf
from tkinter import Image

from enlace_Server import *
import time
import numpy as np
from random import randint, choice
from datetime import datetime

# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM3"                  # Windows(variacao de)


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

        #-----P4-----

        def log_recebe(tipo,tamanho, n_atual, n_total, local):
            agora = str(datetime.now())
            string_log = agora + '/recebe/' + str(tipo) + '/' + str(tamanho) + '/' + str(n_atual) + '/' +str(n_total)
            with open(local, 'a') as f:
                f.write(string_log)
                f.write('\n')

        def log_envio(tipo,local):
            agora = str(datetime.now())
            string_log = agora + '/envio/' + str(tipo) + '/14'
            with open(local, 'a') as f:
                f.write(string_log)
                f.write('\n')


        def tipo2():

            head = [2, 0, 0, 0, 0, 0, 0, 0 ,0 ,0] #numero total a ser visto
            eop = [0xAA, 0xBB, 0xCC, 0xDD]

            pacote = head + eop
            txBuffer = pacote

            log_envio(2,"server/log/Server5.txt")
            time.sleep(0.1)
            com1.sendData(np.asarray(bytes(txBuffer)))

        def tipo4(tipo3):

            ultimo_pacote = tipo3[7]# numero do pacote aferido

            head = [4, 0, 0, 0, 0, 0, 0, ultimo_pacote ,0 ,0]
            eop = [0xAA, 0xBB, 0xCC, 0xDD]

            pacote = head + eop
            txBuffer = pacote

            log_envio(4,"server/log/Server5.txt")
            time.sleep(0.1)
            com1.sendData(np.asarray(bytes(txBuffer)))

        def tipo5():

            head = [5, 0, 0, 0, 0, 0, 0, 0 ,0 ,0] #numero total a ser visto
            eop = [0xAA, 0xBB, 0xCC, 0xDD]

            pacote = head + eop
            txBuffer = pacote

            log_envio(5,"server/log/Server5.txt")
            time.sleep(0.1)
            com1.sendData(np.asarray(bytes(txBuffer)))
        
        def tipo6(numero_pacote):

            head = [6, 0, 0, 0, 0, 0, numero_pacote, 0 ,0 ,0] #numero total a ser visto
            eop = [0xAA, 0xBB, 0xCC, 0xDD]

            pacote = head + eop
            txBuffer = pacote

            log_envio(6,"server/log/Server5.txt")
            time.sleep(0.1)
            com1.sendData(np.asarray(bytes(txBuffer)))

        
        identificador = 10
        pkg = 1
        lista_imagem = []
        ocioso = True

        while ocioso:

            print("ouvindo handshake:")

            txLen = 10
            rxBuffer, nRx = com1.getData(txLen)

            rxBuffer = list(rxBuffer)
            print(rxBuffer)

            tipo_mensagem = rxBuffer[0]
            numero_de_pacotes = rxBuffer[3]

            if tipo_mensagem == 1: # ver se é handshake

                id_mensagem = rxBuffer[5]

                if id_mensagem == identificador: #ver se é para o server

                    ocioso = False
                    time.sleep(1)

                else:
                    time.sleep(1)
            else:
                time.sleep(1)
            
            #eop do handshake
            txLen = 4
            rxBuffer, nRx = com1.getData(txLen)
        
        #envia a mensagem de tipo 2
        tipo2()

        time.sleep(5)

        cont = 1
        eop = [170, 187, 204, 221]


        img = b''

        while cont <= numero_de_pacotes:

            l = 0

            ti_1 = time.time() 
            ti_2 = time.time()
            timer_1 = 0
            timer_2 = 0

            print("ouvindo mensagem:")

            while l < 10:
                l = com1.rx.getBufferLen()

                timer_1 = time.time()-ti_1
                timer_2 = time.time()-ti_2

                # print(timer_2)

                if timer_2 >= 20:
                    ocioso == True
                    tipo5()
                    print(':-(')
                    print('encerrando a comunição por tempo')
                    com1.disable()
                    exit()

                if timer_1 >= 2:
                    tipo4(head)
                    timer_1 = 0
                    ti_1 = time.time()
                    print('pedindo a imagem novamente')

            if l >= 10:
                txLen = 10
                rxBuffer, nRx = com1.getData(txLen)
                head = rxBuffer
                print('peguei head')
            

            head_n = list(rxBuffer)
            print(head_n)
            
            tipo_mensagem = rxBuffer[0]
            numero_do_pacote = rxBuffer[4]
            numero_total = rxBuffer[3]
            tamanho_payload = rxBuffer[5]

            print('analisando o head')

            time.sleep(1)

            if tipo_mensagem == 3: #tipo de mensagem certa
                    
                if pkg == numero_do_pacote: #verifica o numero de pkg junto com o numero do pacote da mensagem
                    
                    #payload
                    log_recebe(tipo_mensagem,tamanho_payload, numero_do_pacote, numero_total, "server/log/Server5.txt")

                    txLen = tamanho_payload
                    time.sleep(0.1)
                    rxBuffer, nRx = com1.getData(txLen)
                    print('peguei payload')
                    # lista_imagem.append(rxBuffer)
                    img+=rxBuffer

                    #eop
                    print('escutando eop')
                    txLen = 4
                    time.sleep(0.1)
                    rxBuffer, nRx = com1.getData(txLen)
                    print('peguei eop')

                    eop_mensagem = rxBuffer # pegar os 4 ultimos elementos para matar o eop

                    print(list(eop_mensagem))
                    print(eop)

                    if eop == list(eop_mensagem):

                        print('mais um')
                    
                        pkg+=1

                        tipo4(head_n)

                        cont+=1

                    else:
                        tipo6(pkg)
                        tamanho_payload = rxBuffer[5]
                        log_recebe(tipo_mensagem,tamanho_payload, numero_do_pacote, numero_total, "server/log/Server5.txt")

                        txLen = tamanho_payload
                        time.sleep(0.1)
                        rxBuffer, nRx = com1.getData(txLen)

                        txLen = 4
                        time.sleep(0.1)
                        rxBuffer, nRx = com1.getData(txLen)

                        print('o eop nao bateu')
                        print('tirando do buffer')
                else:
                    tipo6(pkg)
                    tamanho_payload = rxBuffer[5]
                    log_recebe(tipo_mensagem,tamanho_payload, numero_do_pacote, numero_total, "server/log/Server5.txt")

                    txLen = tamanho_payload
                    time.sleep(0.1)
                    rxBuffer, nRx = com1.getData(txLen)

                    txLen = 4
                    time.sleep(0.1)
                    rxBuffer, nRx = com1.getData(txLen)

                    print('o numero do pacote nao bateu com o esperado')
                    print('tirando do buffer')
            else:
                log_recebe(tipo_mensagem,tamanho_payload, numero_do_pacote, numero_total, "server/log/Server5.txt")
                time.sleep(1)

        print('SUCESSO DE ENVIO')

        imgW = "server/img/copyDog.jpg"
        f = open(imgW, 'wb')
        f.write(img)
        f.close()
        print("acabou de fazer a imagem!")


        print("SUCESSO NA CONSTRUÇÃO DA IMAGEM")
        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")
        com1.disable()

    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()


        

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
        




        

        #-----P3-----

        # #CONSTRUCAO DA IMAGEM
        # eop_correto = [85, 85, 85, 85]

        # if start:
        #     lista_imagem = []
        #     for i in range(quantidade_pacotes-1):

        #         #lendo o HEAD:

        #         txLen = 10
        #         time.sleep(0.5)
        #         rxBuffer, nRx = com1.getData(txLen)
        #         print("recebeu: {}" .format(list(rxBuffer)))
        #         #

        #         index = rxBuffer[0]

        #         n_pacotes = rxBuffer[1]

        #         quantidade_pacotes = rxBuffer[2]

        #         tamanho_payload = rxBuffer[3]

        #         resto = rxBuffer[3:-1]

        #         # print(f"codigo: {index}")
        #         # print(f"numero do pacote: {n_pacotes}")
        #         # print(f"quantidade de pacotes: {quantidade_pacotes}")
        
        #         if i == 0:
        #             n_ultimo_pacote = 0

        #         if n_pacotes != (n_ultimo_pacote + 1):
        #             print("ERRO no numero do pacote")
        #             acknowledge(False)

        #         n_ultimo_pacote = n_pacotes

        #             # print("tamanho payload: {}" .format(tamanho_payload))
        #             # print(list(rxBuffer))

        #             #Montando a imagem
        #         txLen = tamanho_payload
        #             #

        #         time.sleep(0.5)
        #         rxBuffer, nRx = com1.getData(txLen)
        #         # print(f"tamanho da payload:{len(rxBuffer)}")
        #         # print(f"tamanho experado da payload: {txLen}")

        #         if len(rxBuffer) != txLen:
        #             print("erro no tamanho da payload")
        #             acknowledge(False)

        #         else:
        #                 #
        #                 #le a payload, adiciona a lista_imagem
        #             n_pacotes += 1
        #             lista_imagem.append(rxBuffer)
        #             # print(len(rxBuffer))
        #             # print(rxBuffer)

        #             time.sleep(0.5)
        #             rxBuffer, nRx = com1.getData(4)
        #             eop_recebido = rxBuffer
        #             print(f"eop: {list(rxBuffer)}")

        #             if list(eop_recebido) != eop_correto: #compara a lista elemento a elemento
        #                 acknowledge(False)

        #             else: acknowledge(True)
                            


        # imgW = "server/img/copyDog.jpg"
        # f = open(imgW, 'wb')
        # f.write(bytes(lista_imagem))
        # f.close()
        # print("acabou!")
        



        # #-----P2-----

        # #recebendo o numero de comandos"
        # # print("ouvindo")


        # txLen = 1
        # rxBuffer, nRx = com1.getData(txLen)
        # rxBuffer = int.from_bytes(rxBuffer, byteorder='big')
        # number_commands = rxBuffer
        # print("recebeu n_commands: {}" .format(number_commands))
        # 

        # #recebendo os tamanhos dos commandos:
        # commands_size = []
        # for i in range(number_commands):
        #     
        #     rxBuffer, nRx = com1.getData(1)
        #     rxBuffer = int.from_bytes(rxBuffer, byteorder='big')
        #     commands_size.append(rxBuffer)
        #     print("recebeu tamanho {}:" .format(i))
        #     print(rxBuffer)




        # #faça aqui uma conferência do tamanho do seu txBuffer, ou seja, quantos bytes serão enviados.
       
            
        # #finalmente vamos transmitir os tados. Para isso usamos a funçao sendData que é um método da camada enlace.
        # #faça um print para avisar que a transmissão vai começar.
        # #tente entender como o método send funciona!
        # #Cuidado! Apenas trasmitimos arrays de bytes! Nao listas!
  
        # #txBuffer = #dados

        # # com1.sendData(np.asarray(txBuffer))

        # # A camada enlace possui uma camada inferior, TX possui um método para conhecermos o status da transmissão
        # # Tente entender como esse método funciona e o que ele retorna

        # txSize = com1.tx.getStatus()

        # #Agora vamos iniciar a recepção dos dados. Se algo chegou ao RX, deve estar automaticamente guardado
        # #Observe o que faz a rotina dentro do thread RX
        # #print um aviso de que a recepção vai começar.

      
        # #Será que todos os bytes enviados estão realmente guardadas? Será que conseguimos verificar?
        # #Veja o que faz a funcao do enlaceRX  getBufferLen

        # #recebendo os commandos em si:
        # commands = []
        # for i in commands_size:
        #     
        #     rxBuffer, nRx = com1.getData(i)
        #     print("here")
        #     commands.append(rxBuffer)
        #     print("recebeu commando {}:" .format(commands_size.index(i)))
        #     print(rxBuffer)
            

        #enviando quantos comandos foram recebidos:
        # txBuffer = (len(commands_size)).to_bytes(1,byteorder='big')
        # print("mandando {} commandos".format(len(commands_size)))
        # com1.sendData(np.asarray(txBuffer))
