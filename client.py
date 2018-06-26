#from blockchain import Blockchain
#from block import Block
import socket
import sys
from threading import Thread
import time

OP_TRANSACTION = 3
OP_BLOCKCHAIN = 4
OP_VALIDATED = 5

# Cree un packet de donnee a partir des deux valeurs entieres v1 et v2 passees
# en parametre. C'est la serialisation et ce sera l'objet de cour 4.
def CreatePacket(op_code, data):
  return pack("!I{}s".format(len(data)), op_code, data)

def ProcessPacket(packet):
  return unpack("!I{}s".format(len(packet)-sizeof("!I")), packet)

# Ouvre et retourne une socket en mode connecte a l'adrresse et sur le port
# passes en parametre.
def CreateSocket():
  # La socket doit etre ouverte avec la famille d'adressage par defaut et le
  # protocol UDP (socket de type datagram)
  sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

  return sock

def printMenu():
  print ("Menu:")
  print ("\n[n] Nouveau Message")
  print ("\n[c] Consulter la blockchain")
  print ("\n[t] Telecharger toutes les transaction validees.")
  print ("\n[q] Quitter")

if __name__ == "__main__":
  if len(sys.argv) != 3:
    print("Usage: python {} adresseServeur port".format(sys.argv[0]))
    exit(1)
  server = (sys.argv[1], int(sys.argv[2])) 
  # Ouverture de la socket
  sock = CreateSocket()

  # Boucle principale
  while True:
    printMenu()
    choice = input("Entrer une commande:")
     
    if choice == 'n':
      transaction = input("Entrer une nouvelle transaction:")
      packet = CreatePacket(OP_TRANSACTION, transaction)
      print(packet, server)
      sock.sendto(packet, server)
      continue
      
    elif choice == "b":
      packet = CreatePacket(OP_BLOCKCHAIN, '')
      sock.sendto(packet, server)
      
    elif choice == "t":
      packet = CreatePacket(OP_VALIDATED, '')
      sock.sendto(packet, server)
    elif choice == "q":
      break
    else:
      continue

    # Attend une reponse du serveur
    packet = sock.recv(1024)
    if len(packet) > 0:
      (op_code, data) = ProcessPacket(packet)
      
      if op_code == OP_BLOCKCHAIN:
        bc = Blockchain()
        bc.deserialize(data)
        print(bc)
      elif op_code == OP_VALIDATED:
        transactions = data.split(";")
        for t in transactions:
          print(t) 
     
  sock.close()
