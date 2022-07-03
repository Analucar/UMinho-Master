# coding: latin-1
###############################################################################
# eVotUM - Electronic Voting System
#
# initSigner-app.py 
#
# Cripto-7.0.2 - Commmad line app to exemplify the usage of initSigner
#       function (see eccblind.py)
#
# Copyright (c) 2016 Universidade do Minho
# Developed by André Baptista - Devise Futures, Lda. (andre.baptista@devisefutures.com)
# Reviewed by Ricardo Barroso - Devise Futures, Lda. (ricardo.barroso@devisefutures.com)
#
# Reviewed and tested with Python 3 @Jan/2021 by
#      José Miranda - Devise Futures, Lda. (jose.miranda@devisefutures.com)
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
#
###############################################################################
"""
Command line app that writes initComponents and pRDashComponents to STDOUT.
"""

import getpass
import sys
from eVotUM.Cripto import eccblind
from eVotUM.Cripto import utils
from Crypto.PublicKey import ECC

def printUsage():
    print("Usage: python initSigner-app.py")
    print("Usage: python initSigner-app.py -init")

def parseArgs():
    if len(sys.argv) > 2:
        printUsage()
    elif len(sys.argv) == 1:
        main()
    elif sys.argv[1] == "-init":
        init()

def generateKey():

    #gera o par de chaves utilizando RSA
    eccKey = ECC.generate(curve='p256')

    privateFile = input('Ficheiro onde armazenar ' + 
                            'a chave privada (***.pem):  ')
    publicFile = input('Ficheiro onde armazenar ' + 
                                'a chave publica (***.pem):  ')

    #Password de proteção da chave privada
    password = getpass.getpass('Password de protecao da ' +
                                'chave privada:  ').encode('utf-8')
    
    #Exporta a chave pública e privada para um ficheiro
    privateKey = eccKey.export_key(format='PEM',passphrase=password, protection="PBKDF2WithHMAC-SHA1AndAES128-CBC")
    publicKey = eccKey.public_key().export_key(format='PEM')

    #Armazena a chave privada no ficheiro
    private_out = open(privateFile, "w")
    private_out.write(privateKey)
    private_out.close()

    #Armazena a chave publica no ficheiro
    public_out = open(publicFile, "w")
    public_out.write(publicKey)
    public_out.close()



def main():
    initComponents, pRDashComponents = eccblind.initSigner()
    print("pRDashComponents: %s" % pRDashComponents)

    f = open("AssinanteFile.txt", "w")
    f.write("Init Components:%s" % initComponents)
    f.close()

def init():
    initComponents, pRDashComponents = eccblind.initSigner()

    f = open("AssinanteFile.txt", "w")
    f.write("Init Components:%s" % initComponents)
    f.write("\n")
    f.write("pRDash Components:%s" % pRDashComponents)
    f.close()

if __name__ == "__main__":
    generateKey()
    parseArgs()