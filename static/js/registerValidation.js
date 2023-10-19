completeName = document.getElementById('completeName')
emailCamp = document.getElementById('emailCamp')
pass1 = document.getElementById('pass1')
pass2 = document.getElementById('pass2')
errorMessage = document.getElementById('errorMessage')
radios = document.querySelectorAll('.radios')
submitButton = document.getElementById('submitButton')
defaultErrorMessage = "<div class='errors-header'>Registro não pode ser concluido pois: </div>"
errorMessage.innerHTML = defaultErrorMessage

submitButton.addEventListener('click', handleForm)




function triggerError(e){
    errorMessage.classList.remove('hiddeable')
    e.preventDefault()
}

function handleForm(e){
    errorMessage.innerHTML = defaultErrorMessage
    let count = 0
    errors = []
    if(completeName.value == ""){
        errors.push("<li>Nome não pode estar vazio!</li>")
        completeName.classList.add('error-camp')
        count += 1
    }
    else{
        completeName.classList.remove('error-camp')
    }

    var validRegex = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/;
    if (emailCamp.value.match(validRegex)) {
        emailCamp.classList.remove('error-camp')
    } 
    else {
        errors.push("<li>Formato de e-mail não válido!</li>")
        emailCamp.classList.add('error-camp')
        count += 1
    }

    if(pass1.value != pass2.value){
        errors.push('<li>Senhas não coincidem!</li>')
        pass1.classList.add('error-camp')
        pass2.classList.add('error-camp')
        count += 1
    }
    else if(pass1.value.length < 8){
        errors.push('<li>Senha não pode ter menos que 8 caracteres!</li>')
        pass1.classList.add('error-camp')
        pass2.classList.add('error-camp')
        count += 1
    }
    else{
        pass1.classList.remove('error-camp')
        pass2.classList.remove('error-camp')
    }

    let radioCheckeds = 0
    radios.forEach(radio => {
        if(radio.checked){
            radioCheckeds += 1
        }
    })
    if(radioCheckeds < 1){
        errors.push('<li>Tipo de usuário não selecionado!</li>')
        count += 1
    }

    if(count >= 1){
        errors.forEach(error => {
            errorMessage.innerHTML += error
        })
        triggerError(e)
    }
    else{
        errorMessage.classList.add('hiddeable')
    }

}
