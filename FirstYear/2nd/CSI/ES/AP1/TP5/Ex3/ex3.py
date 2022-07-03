import os, sys, subprocess
sys.tracebacklimit = 0

def ex3(certificate):

    final = None

    # se o ficheiro for do tipo .cer converter para pem
    if certificate.endswith(".cer"):

        converter = "openssl x509 -inform Der -in " + certificate + " -out CertExchange.pem"
        subprocess.call(converter, shell=True)
        certificate = "CertExchange.pem"

    if certificate.endswith(".pem"):

        # obter linha do issuer
        get_issuer = "openssl x509 -in " + certificate + " -noout -issuer"
        issuer_name = str(subprocess.check_output(get_issuer, shell=True), 'utf-8').rstrip()
        
        # obter numero do certificado do EC
        issuer_num = issuer_name[issuer_name.rfind(' ') + 1:]

        # obter certificado do EC
        issuer_link = "http://pki.cartaodecidadao.pt/publico/certificado/cc_ec_cidadao_cmd/EC%20de%20Chave%20Movel%20Digital%20de%20Assinatura%20Digital%20Qualificada%20do%20Cartao%20de%20Cidadao%20" + issuer_num + ".cer"
        get_issuer_link = "wget -q -O issuer.cer " + issuer_link
        subprocess.call(get_issuer_link, shell=True)

        # converter certificado do EC para pem
        issuer_converter = "openssl x509 -inform Der -in issuer.cer -out issuer.pem"
        subprocess.call(issuer_converter, shell=True)
        issuer = "issuer.pem"

        # url do serviço ocsp
        get_url = "openssl x509 -noout -ocsp_uri -in " + certificate
        url = str(subprocess.check_output(get_url, shell=True), 'utf-8').rstrip()
        print("\nUrl do OCSP: " + url + "\n")

        # comando de informação de revogação
        date = "openssl ocsp -issuer " + issuer + " -cert " + certificate + " -url " + url + " -noverify"
        final = str(subprocess.check_output(date, shell=True), 'utf-8')

        # remover ficheiros depois da execuçao
        os.remove(issuer)
        os.remove("issuer.cer")
    
    else:
        print("\nCertificado inválido!")
        os.system("python3 ex3.py")
        exit()

    return final


if __name__ == "__main__":
    print("\nNome do certificado: ", end = '')
    certificate = input()
    status = ex3(certificate)
    if status != None:
        print(status)
