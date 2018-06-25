from os import listdir
from os.path import isfile, join
import re
import hashlib

class Blocks:

    # Constructeur de la classe
    # 
    # @params
    #   - nodeName : Le nom du noeud
    def __init__(self, nodeName):
        # Enregiste l'emplacement des blocs
        self.path = 'nodes/' + nodeName + '/blocks/'

    # Récupère un bloc donné (en fonction de son ID)
    # Retourne False en cas d'erreur
    def getBlock(self, id):
        # Lecture du bloc ligne par ligne
        block = {}
        with open(self.path + id, 'r') as f:
            content = f.readlines()
            for line in content:
                line = line.strip()
                # Découpe en fonction des espaces
                identifier = line.split(' ')
                # Vérifie si la ligne est correcte
                if len(identifier) == 0:
                    return False
                # Vérifie l'identificateur
                if identifier[0] in ['previous', 'miner', 'pow', 'date', 'nonce']:
                    block[identifier[0]] = line[(len(identifier[0])+1):]
                elif identifier[0] == 'transactions':
                    block[identifier[0]] = identifier[1:]
                elif line != '':
                    return False
            f.close()
        return block

    # Récupère la liste des blocs de la chaîne
    def getList(self):
        # Liste les fichiers (avec vérification du format)
        prog = re.compile(r"^\d+\.[\da-f]{1,64}$")
        return [f for f in listdir(self.path) if isfile(join(self.path, f)) and prog.match(f)]

    # Ecriture d'un bloc
    def writeBlock(self, previous, miner, pow, date, nonce, transactions):
        # On récupère le numéro de bloc actuel
        bloc_number = len(Blocks.getList(self))
        # Génère le contenu du fichier
        content = 'previous ' + previous + '\n'
        content += 'miner ' + miner + '\n'
        content += 'pow ' + str(pow) + '\n'
        content += 'date' + date + '\n'
        content += 'nonce ' + str(nonce) + '\n'
        content += 'transactions ' + ' '.join(transactions)
        # Hash le fichier
        id = str(bloc_number) + '.' + hashlib.md5(content.encode()).hexdigest()
        # Ecrit le fichier
        f = open(self.path + id, 'w+')
        f.write(content)
        f.close()
        # Retourne l'ID du block créé
        return id

# Test
if __name__ == '__main__':
    node = 'node_1'
    blocks = Blocks(node)
    l = blocks.getList()
    print(l)
    print(blocks.getBlock(l[0]))
    blocks.writeBlock('---', 'miner-name', 16, '17/09/1996', 1343, '')
