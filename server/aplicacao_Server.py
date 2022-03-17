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
from operator import index, indexOf
from enlace_Server import *
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

        #-----P3-----

        def acknowledge(b): #boolean
            #caso tenha dado algo errado, remandar o ultimo pacote
            if b: 
                head = [30, 0, 0 ,0 ,0, 0, 0 ,0 ,0, 0]
            else: 
                head = [40, 0, 0 ,0 ,0, 0, 0 ,0 ,0, 0]

            eop = [85, 85, 85, 85]
            pacote = head + eop
            txBuffer = pacote
            time.sleep(0.1)
            com1.sendData(np.asarray(bytes(txBuffer)))

        print("ouvindo:")

        #HANDSHAKE
        txLen = 10
        rxBuffer, nRx = com1.getData(txLen)
        print("recebeu: {}" .format(rxBuffer))
        time.sleep(0.1)

        index = rxBuffer[0]

        n_pacotes = rxBuffer[1]

        quantidade_pacotes = rxBuffer[2]

        tamanho_payload = rxBuffer[3]
        
        # print(f"codigo: {index}")
        # print(f"numero do pacote: {n_pacotes}")
        # print(f"quantidade de pacotes: {quantidade_pacotes}")

        txLen = 4
        rxBuffer, nRx = com1.getData(txLen)
        #print("EOP: {}" .format(list(rxBuffer)))
        
        if index == 10: # index 10 == handhsake, podemos prosseguir]
            acknowledge(True)
            start = True
        else: 
            start = False



        # acknowledge(True)
        
        time.sleep(0.5)

        #CONSTRUCAO DA IMAGEM
        eop_correto = [85, 85, 85, 85]

        if start:
            lista_imagem = []
            for i in range(quantidade_pacotes):

                #lendo o HEAD:

                txLen = 10
                time.sleep(0.1)
                rxBuffer, nRx = com1.getData(txLen)
                print("recebeu: {}" .format(list(rxBuffer)))
                #time.sleep(0.1)

                index = rxBuffer[0]

                n_pacotes = rxBuffer[1]

                quantidade_pacotes = rxBuffer[2]

                tamanho_payload = rxBuffer[3]

                resto = rxBuffer[3:-1]

                print(f"codigo: {index}")
                print(f"numero do pacote: {n_pacotes}")
                print(f"quantidade de pacotes: {quantidade_pacotes}")
        
                if i == 0:
                    n_ultimo_pacote = n_pacotes

                if n_pacotes != (n_ultimo_pacote + 1):
                    print("erro no numero de pacotes")
                    acknowledge(False)

                elif i >= 0:
                    #print("tamanho payload: {}" .format(tamanho_payload))
                    #print(list(rxBuffer))

                    #Montando a imagem
                    txLen = tamanho_payload
                    #time.sleep(0.1)

                    time.sleep(0.1)
                    rxBuffer, nRx = com1.getData(txLen)
                    print(f"tamanho da payloadL{len(rxBuffer)}")
                    print(f"tamanho experado da payload: {txLen}")

                    if len(rxBuffer) != txLen:
                        print("erro no tamanho da payload")
                        acknowledge(False)

                    else:
                        #time.sleep(0.1)
                        #le a payload, adiciona a lista_imagem
                        lista_imagem.append(rxBuffer)
                        print(len(rxBuffer))
                        print(rxBuffer)

                        time.sleep(0.1)
                        rxBuffer, nRx = com1.getData(4)
                        time.sleep(0.1)
                        eop_recebido = rxBuffer
                        print(f"eop: {list(rxBuffer)}")

                        if eop_recebido != eop_correto: #compara a lista elemento a elemento
                            acknowledge(False)

                        else: acknowledge(True)
                            


        imgW = "server/img/copyDog.jpg"
        f = open(imgW, 'wb')
        f.write(bytes(lista_imagem))
        f.close()
        print("acabou!")
        time.sleep(0.1)


            


        




        # #-----P2-----

        # #recebendo o numero de comandos"
        # # print("ouvindo")


        # txLen = 1
        # rxBuffer, nRx = com1.getData(txLen)
        # rxBuffer = int.from_bytes(rxBuffer, byteorder='big')
        # number_commands = rxBuffer
        # print("recebeu n_commands: {}" .format(number_commands))
        # time.sleep(0.1)

        # #recebendo os tamanhos dos commandos:
        # commands_size = []
        # for i in range(number_commands):
        #     time.sleep(0.1)
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
        #     time.sleep(0.1)
        #     rxBuffer, nRx = com1.getData(i)
        #     print("here")
        #     commands.append(rxBuffer)
        #     print("recebeu commando {}:" .format(commands_size.index(i)))
        #     print(rxBuffer)
            

        #enviando quantos comandos foram recebidos:
        # txBuffer = (len(commands_size)).to_bytes(1,byteorder='big')
        # print("mandando {} commandos".format(len(commands_size)))
        # com1.sendData(np.asarray(txBuffer))

        print("-------------------------")
        print("Comunicação encerrada")
        com1.disable()

    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()


        

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
