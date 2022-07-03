import java.util.Scanner;
import java.util.Base64;

import java.nio.file.Files;
import java.nio.file.Paths;
import java.nio.file.Path;
import java.nio.charset.StandardCharsets;
import java.io.IOException;
import java.io.FileInputStream;
import java.io.BufferedOutputStream;
import java.io.BufferedInputStream;
import java.io.FileOutputStream;
import java.io.FileNotFoundException;

import javax.crypto.spec.SecretKeySpec;
import java.security.spec.PKCS8EncodedKeySpec;
import javax.crypto.NoSuchPaddingException;
import java.security.interfaces.RSAPublicKey;
import java.security.interfaces.RSAPrivateKey;
import java.security.NoSuchAlgorithmException;
import java.security.InvalidKeyException;
import java.security.spec.InvalidKeySpecException;
import java.security.SecureRandom;
import java.security.InvalidAlgorithmParameterException;
import java.security.Signature;
import java.security.PrivateKey;
import java.security.PublicKey;
import java.security.spec.EncodedKeySpec;
import java.security.spec.X509EncodedKeySpec;
import java.security.KeyFactory;
import java.security.KeyPairGenerator;
import java.security.KeyPair;
import java.security.SignatureException;



public class RSA_PSS{

    private static final int KEY_SIZE = 2048; //Tamanho em bits da chave

    /* Metodo que trata da funcionalidade de gerar chaves públicas e privadas RSA
     * input: Paths para os ficheiros onde ficarão as chaves publica e privada.
    */

    private static void keyGenHandler(String pubKeyFile, String privKeyFile){
        try{
            KeyPairGenerator keyGen = KeyPairGenerator.getInstance("RSA");
            keyGen.initialize(KEY_SIZE);
            KeyPair keyPair = keyGen.generateKeyPair();
            writePrivateKey(keyPair.getPrivate(), privKeyFile);
            writePublicKey(keyPair.getPublic(), pubKeyFile);
        } catch(NoSuchAlgorithmException e) {
            System.out.println(e.getMessage());

        } 
    }

    /* Metodo que trata da funcionalidade de assinar um ficheiro
     * input: Path para o ficheiro que contém a chave RSA privada, ficheiro de input da mensagem 
     *        e ficheiro de output onde será guardada a assinatura.
    */

    private static void signatureHandler(String privKey, String input, String output){
        byte [] buffer = new byte[2048]; //Buffer para leitura do ficheiro
        
        try{
            PrivateKey privateKey = readPrivateKey(privKey);
            Signature sign = Signature.getInstance("SHA256withRSA");
            sign.initSign(privateKey);
            
            BufferedInputStream in = new BufferedInputStream(new FileInputStream(input)); 

            BufferedOutputStream out = new BufferedOutputStream(new FileOutputStream(output)); 
            
            int readBytes;

            while((readBytes = in.read(buffer)) != -1)
                sign.update(buffer, 0, readBytes);
            
            out.write(sign.sign());

            out.close();
            in.close();
            
        } catch(NoSuchAlgorithmException | SignatureException | IOException e) {
            System.out.println(e.getMessage());

        } catch(InvalidKeyException e){
            System.out.println("A chave é inválida.");
        }

    }
    /* Metodo que trata da funcionalidade de verificação da assinatura do ficheiro
     * input: Path para o ficheiro que contém a chave RSA pública, ficheiro de input da mensagem 
     *        e ficheiro que contém a assinatura.
     * output: true caso a assinatura seja válida, false caso contrário
    */

    private static boolean verifyHandler(String pubKey, String input, String signatureFile){
        byte [] buffer = new byte[2048]; //Buffer para leitura do ficheiro de input
        try{
            PublicKey publicKey = readPublicKey(pubKey);
            Signature sign = Signature.getInstance("SHA256withRSA");
            sign.initVerify(publicKey);
            
            BufferedInputStream in = new BufferedInputStream(new FileInputStream(input)); 

            int readBytes;

            while((readBytes = in.read(buffer)) != -1)
                sign.update(buffer, 0, readBytes);
            
            in.close();

            Path signaturePath = Paths.get(signatureFile);
            byte [] signature = Files.readAllBytes(signaturePath);

            return sign.verify(signature);     
        } catch(NoSuchAlgorithmException | SignatureException | IOException e) {
            System.out.println(e.getMessage());

        } catch(InvalidKeyException e){
            System.out.println("A chave é inválida.");
        }

        return false;
    }
    
    private static PrivateKey readPrivateKey(String fileName){
        try{
            Path path = Paths.get(fileName);
            byte [] privKey = Files.readAllBytes(path);

            KeyFactory keyFactory = KeyFactory.getInstance("RSA");
            PKCS8EncodedKeySpec privKeySpec = new PKCS8EncodedKeySpec(privKey);
            return (RSAPrivateKey) keyFactory.generatePrivate(privKeySpec);

        } catch(NoSuchAlgorithmException | InvalidKeySpecException | IOException e) {
            System.out.println(e.getMessage());
        }
        return null;
    }
    
    private static PublicKey readPublicKey(String fileName){
        try{
            Path path = Paths.get(fileName);
            byte [] pubKey = Files.readAllBytes(path);

            KeyFactory keyFactory = KeyFactory.getInstance("RSA");
            EncodedKeySpec publicKeySpec = new X509EncodedKeySpec(pubKey);
            return (RSAPublicKey) keyFactory.generatePublic(publicKeySpec);

        } catch(NoSuchAlgorithmException | InvalidKeySpecException | IOException e) {
            System.out.println(e.getMessage());
        }
        return null;

    }

    private static void writePrivateKey(PrivateKey key, String output){
        try{
            FileOutputStream out = new FileOutputStream(output); 
            out.write(key.getEncoded());
        } catch(IOException e){}
    }

    private static void writePublicKey(PublicKey key, String output){
        try{
            BufferedOutputStream out = new BufferedOutputStream(new FileOutputStream(output)); 
            out.write(key.getEncoded());
            out.close();
        } catch(IOException e){}
    }

    public static void main(String[] args){
        Scanner sc = new Scanner(System.in);
        String opt = "";

        if(args.length > 0)
            opt = args[0].toUpperCase();

        //Verificacao do numero de argumentos passados ao programa
        if((opt.equals("SIGN") && args.length == 4) || (opt.equals("VERIFY") && args.length == 4) || (opt.equals("KEYGEN") && args.length == 3)){

            if(opt.equals("SIGN"))
                signatureHandler(args[3], args[1], args[2]);

            else if (opt.equals("KEYGEN"))
                keyGenHandler(args[1], args[2]);

            else if (opt.equals("VERIFY"))
                System.out.println("A assinatura é valida? " + verifyHandler(args[2], args[1], args[3]));
            
        } else {
            System.out.println("Comando inválido!");
            System.out.println("Gerar chaves: RSA_PSS keyGen [PUBLIC_KEY_OUTPUT_FILE] [PRIVATE_KEY_OUTPUT_FILE]");
            System.out.println("Assinar: RSA_PSS sign [INPUT_FILE] [OUTPUT_FILE] [PRIVATE KEY]");
            System.out.println("Verificar assinatura: RSA_PSS verify [INPUT_FILE] [PUBLIC KEY] [SIGNATURE_FILE]");
        }
    }   
}


