/**
 * ESTE JAVASCRIPT VAI TER DE SER ALTERADO
 */

function onDocumentReady() {

    // Variavel que corresponde ao campo do telemovel
    const $userId = $("#userId");
    // Variavel que corresponde ao telemovel enviado pelo o backend
    const $phone = document.getElementById('userPhone').value

    console.log($phone)
    console.log($userId)

    // caso o perfil desse user não tenha armazenado lá o telemovel
    if($phone=== "") {
        $userId.val("+351 ");
    } else {
        // caso o perfil desse user tenha armazenado lá o telemovel, vamo colocá-lo no $userId
        $userId.val($phone);
    }
}

$(document).ready(onDocumentReady);
