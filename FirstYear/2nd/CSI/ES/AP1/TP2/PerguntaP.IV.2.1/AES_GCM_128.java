import java.util.Scanner;
import java.util.Base64;

import java.nio.file.Files;
import java.nio.charset.StandardCharsets;

import java.io.IOException;
import java.io.FileInputStream;
import java.io.BufferedOutputStream;
import java.io.FileOutputStream;
import java.io.FileNotFoundException;

import javax.crypto.spec.GCMParameterSpec;
import javax.crypto.spec.IvParameterSpec;
import javax.crypto.spec.SecretKeySpec;
import javax.crypto.SecretKey;
import javax.crypto.AEADBadTagException;
import javax.crypto.Cipher;
import javax.crypto.CipherInputStream;
import javax.crypto.NoSuchPaddingException;

import java.security.NoSuchAlgorithmException;
import java.security.InvalidKeyException;
import java.security.SecureRandom;
import java.security.InvalidAlgorithmParameterException;


public class AES_GCM_128{

    private static final int TAG_SIZE = 128; //Tamanho em bits da tag
    private static final int IV_SIZE = 12; //Tamanho em bytes do IV
    
    /* Metodo que trata da funcionalidade de cifra do programa 
     * input: Chave de cifra, path do ficheiro de input, path do ficheiro de output
     * output: array de bytes que contém o IV
    */

    private static byte[] encipherHandler(String key, String input, String output){
        byte [] buffer = new byte[512]; //Buffer para leitura do ficheiro (plaintext)
        byte iv [] = new byte[IV_SIZE]; //Iv que vai ser gerado
        try{
            //Output Stream com buffer para não escrever constantemente no ficheiro
            BufferedOutputStream out = new BufferedOutputStream(new FileOutputStream(output)); 
            
            //Passagem da key fornecida pelo utilizador para bytes
            //Criacao do objecto de chave secreta a partir do array de bytes anterior
            byte[] keyBytes = key.getBytes(StandardCharsets.UTF_8);
            SecretKey sk = new SecretKeySpec(keyBytes, 0, keyBytes.length, "AES");

            //Geracao aleatoria do iv pseudo-aleatorio com 12 bytes de tamanho
            SecureRandom sr = new SecureRandom();
            sr.nextBytes(iv);
            GCMParameterSpec params = new GCMParameterSpec(TAG_SIZE, iv);
            
            //Criacao do objeto correspondente a cifra AES no modo GCM
            Cipher AES_128_Cipher = Cipher.getInstance("AES/GCM/NOPADDING");
            AES_128_Cipher.init(Cipher.ENCRYPT_MODE, sk, params);
            
            //Criacao de uma inputstream que aplica a cifra anterior aquilo que for lido do ficheiro
            //de input
            CipherInputStream in = new CipherInputStream(new FileInputStream(input), AES_128_Cipher);     
            int readBytes;

            //Leitura para o buffer e escrita do texto cifrado para o ficheiro de output
            while((readBytes = in.read(buffer)) != -1){
                out.write(buffer, 0, readBytes);
                out.flush();
            }

            out.close();
            in.close();
            
            return iv;
        } catch(NoSuchAlgorithmException | IOException | NoSuchPaddingException | InvalidAlgorithmParameterException e) {
            System.out.println(e.getMessage());

        } catch(InvalidKeyException e){
            System.out.println("A chave é inválida.");
        }

        return null;
    }
    /* Metodo que trata da funcionalidade de decifragem do programa 
     * input: Chave de cifra, path do ficheiro de input, path do ficheiro de output, IV
     * output: true se a operacao foi efetuada com sucesso. false caso contrario.
    */

    private static boolean decipherHandler(String key, String input, String output, byte [] iv){
        byte [] buffer = new byte[512]; //Buffer do ficheiro de input (ciphertext)
        try{
            
            BufferedOutputStream out = new BufferedOutputStream(new FileOutputStream(output));     
            
            GCMParameterSpec params = new GCMParameterSpec(TAG_SIZE, iv);

            //Criacao da chave secreta a partir da chave fornecida pelo utilizador
            byte[] keyBytes = key.getBytes(StandardCharsets.UTF_8);
            SecretKey sk = new SecretKeySpec(keyBytes, 0, keyBytes.length, "AES");

            Cipher AES_128_Cipher = Cipher.getInstance("AES/GCM/NoPadding");

            AES_128_Cipher.init(Cipher.DECRYPT_MODE, sk, params);

            CipherInputStream in = new CipherInputStream(new FileInputStream(input), AES_128_Cipher);     
            int readBytes;

            while((readBytes = in.read(buffer)) != -1){
                out.write(buffer, 0, readBytes);
                out.flush();
            }

            out.close();
            in.close();

            return true;
        } catch(NoSuchAlgorithmException | IOException | NoSuchPaddingException | InvalidAlgorithmParameterException e) {
            System.out.println(e.getMessage());

        } catch(InvalidKeyException e){
            System.out.println("A chave é inválida.");
        } 
        return false;
    }
    
    /* Metodo auxiliar que lê o IV presente no ficheiro especificado
     * input: Path do ficheiro que contem o IV
     * output: IV em forma de array de bytes
    */

    private static byte [] readIV(String path){
        try{
            FileInputStream in = new FileInputStream(path);
            byte [] iv = new byte[IV_SIZE];

            in.read(iv, 0, IV_SIZE);
            in.close();
            return iv;
        } catch (FileNotFoundException e){
            System.out.println(path + " não existe.");

        } catch (IOException e){
            e.printStackTrace();
        }

        return null;
    }

    /* Metodo auxiliar que escreve o IV no ficheiro indicado
     * input: Path do ficheiro de output e o IV em forma de array de bytes
    */

    private static void writeIV(String path, byte [] iv){
        try{
            FileOutputStream out = new FileOutputStream(path);
            out.write(iv, 0, IV_SIZE);
            out.flush();
            out.close();

        } catch (FileNotFoundException e){
            System.out.println(path + " não existe.");

        } catch (IOException e){
            e.printStackTrace();
        }
    }

    public static void main(String[] args){
        Scanner sc = new Scanner(System.in);
        String key, opt; 
        opt = "";
        byte [] iv;
        boolean success;

        if(args.length > 0)
            opt = args[0].toUpperCase();

        //Verificacao do numero de argumentos passados ao programa
        if((opt.equals("CIFRA") && (args.length == 5 || args.length == 4)) || (opt.equals("DECIFRA") && (args.length == 5 || args.length == 4))){
            
            //A chave e o ultimo argumento
            key = args[args.length - 1];
            
            //Caso a chave nao tenha sido introduzida pelo utilizador o programa pede-lhe neste passo
            if((args.length == 4 && opt.equals("CIFRA")) || (args.length == 4 && opt.equals("DECIFRA"))){
                System.out.println("Introduza a chave: ");
                key = sc.nextLine();
            }

            if(opt.equals("CIFRA")){
                //Caso a operacao seja de cifra chama o metodo auxiliar que trata desse processo
                iv = encipherHandler(key, args[1], args[2]);

                //Caso o resultado nao seja nulo escreve o IV no ficheiro
                //Caso contrario imprime uma mensagem de erro.
                if(iv != null){
                    writeIV(args[3], iv);
                    System.out.println("O Ficheiro foi cifrado. O Resultado está no ficheiro: " + args[2]);
                    System.out.println("O IV foi escrito no ficheiro: " + args[3]);
                }else
                    System.out.println("A operação falhou!");
            } else if (opt.equals("DECIFRA")){
                //Caso a operacao seja de decifra carrega o IV para um array de bytes 
                //a partir do ficheiro indicado
                byte [] ivBytes = readIV(args[3]);
                
                //Caso o array nao seja nulo e possua os 12 bytes
                //chama o metodo que realiza o processo de decifragem
                if (ivBytes != null && ivBytes.length == IV_SIZE){
                    success = decipherHandler(key, args[1], args[2], ivBytes);

                    if(success)
                        System.out.println("O Ficheiro foi decifrado. O Resultado está no ficheiro: " + args[2]);
                    else
                        System.out.println("A operação falhou!");
                } else
                    System.out.println("O IV tem de ter 12 bytes!");
            }

        } else {
            System.out.println("Comando inválido!");
            System.out.println("Cifrar: AES_GCM_128 cifra [INPUT_FILE] [OUTPUT_FILE] [IV_OUTPUT_FILE] [KEY (16 bytes)]");
            System.out.println("Decifrar: AES_GCM_128 decifra [INPUT_FILE] [OUTPUT_FILE] [IV_INPUT_FILE] [KEY (16 bytes)]");
        }
    }
}


