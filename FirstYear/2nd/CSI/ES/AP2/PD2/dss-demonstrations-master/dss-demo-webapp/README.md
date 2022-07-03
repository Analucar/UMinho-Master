# INFORMAÇÕES

## PROBLEMA 1
A funcionalidade do grupo do ano passado já se encontra toda na versão 5.10.

## PROBLEMA 2 e 3
Paginas html e chamadas ao backend estão implementadas. Para isso foi necessário acrescentar os seguintes ficheiros

### Backend
+ **AutenticateUserController.java**: Controlador do login, registo e profile do user. É esta classe que chama as paginas html para cada funcionalidade e aquela que vai receber os inputs do utilizador. Faz de intermediário entre o frontend e o backend da aplicação
+ **AutenticateUserForm.java**: Vai armazenar a informação que é recebida de input sobre o user (userID, password (string??), telemóvel).
+ **AutenticateService.java**: Vai fazer de interméddio entre a BD e a aplicação. Neste serviço vamos retirar e armazenar informação na BD. É também neste serviço que vamos hash a password - já implementado.  

### Frontend
+ **autenticatePage.html**: Pagina inicial da aplicação vai apresentar uma secção para fazer o user fazer o login e vai apresentar um botão caso o user se prentenda inscrever.
+ **login-layout.html**: Vai apresentar o layout da pagina de login e registo
+ **signup.html**: Pagina de resgisto do user.
+ **profile.html**: Pagina com o perfil do user onde este vai poder indicar o número de telemóvel.

Para implementação correta destes dois problemas vai ser necessários:
+ Escolher e implementar uma BD que permita armazenar informação sobre o user (encontrei este tutorial com o mysql que nos podia ajudar - https://www.javaguides.net/2018/10/user-registration-module-using-springboot-springmvc-springsecurity-hibernate5-thymeleaf-mysql.html)
+ Temos de transmitir a password de forma segura quando é introduzida na aplicação. Esta é enviada em formato string do frontend para o backend. Talvez tenhamos de passar logo que é introduzida no frontend para uma hash. Se não só é passada quando se faz o handler do input no controller. 
+ Temos de arranjar um mecanismo que impeça o user de ir para páginas na aplicação sem que este esteja autenticado. Por exemplo, não podemos permitir que o user na página inicial (de login) consiga escrever no url _../home_ e conseguir ir para a pagina home sem antes de se ter autenticado. Temos garantir isto para todos o urls.
+ Será necessário criar uma outra classe representativa da informação da BD? Não tenho a certeza. 

A informação sobre o que se deve implementar em cada método do controller encontram-se todos na classe AutenticateUserController.java. As páginas html so funcionam uma vez -> necessário resolver estes problema.

## PROBLEMA 4
Para alterar a implementação do grupo do ano passado de forma acrescentar o telemóvel sempre que o ser tenha essa informação armazenada na BD, vamos ter de alterar o scrip **jsSaveCmdUserId.js** segundo o que está lá mencionado.
+ Se o utilizador tiver o telemóvel armazenado na BD então o campo para introdução do telemóvel não é utilizado ou coloca-se lá o telemóvel do user.
+ Se o utilizador não tiver lá o telemóvel então o campo terá de ser preenchiodo com o input do user. 

## PROBLEMA 5
Neste problema teremos de possiblitar ao user que quando este pertende assinar um documento, o certificado e chave privada para o fazer pode estar num ficheiro no disco (que o utilizador tem de indicar), e será esse certificado e chave privada que vai ser utilizado para assinar.

**Dúvida**: Já existe uma funcionalidade de Sign Document, temos de acrescentar uma nova só com esta possiblidade ou é para alterar a já existente e acrescentar essa possiblidade?

Devido a esta dúvida ainda não avançei com este problema. 
