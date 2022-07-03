from cryptography import x509
import sys
from cryptography.x509.oid import ExtensionOID
import os
from pprint import pprint
import requests

def getCRLfile():
    crl = cert.extensions.get_extension_for_oid(ExtensionOID.CRL_DISTRIBUTION_POINTS)
    crl_url = crl.value[0].full_name[0].value

    print("CRL URL: " + str(crl_url))

    crl_file = requests.get(crl_url)
    
    p = open(crlFileName, 'wb')
    p.write(crl_file.content)
    p.close()


def check():
    f = open(crlFileName, 'rb')
        
    crl = x509.load_der_x509_crl(f.read())
    revoked = crl.get_revoked_certificate_by_serial_number(cert.serial_number)
        
    print("Data da CRL atual: " + str(crl.last_update))
    print("Data da próxima CRL: " + str(crl.next_update))

    if revoked == None:
        print("O certificado não foi revocado!")

    else:
        print("O certificado foi revogado!")
        print("Data: " + str(revoked.revocation_date))

if len(sys.argv) != 3:
    print("Argumentos inválidos!")
    print("python3 ex2.py [CERTIFICATE PATH] [CRL FILE NAME]")

else:
    certificateName = sys.argv[1]
    crlFileName = sys.argv[2]

    f = open(certificateName, 'rb')

    if certificateName.endswith(".cer"):
        cert = x509.load_der_x509_certificate(f.read())

    else:
        cert = x509.load_pem_x509_certificate(f.read())

    getCRLfile()
    check()

    f.close()

