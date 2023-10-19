var data = document.currentScript.dataset
let backErrorMessage = data.error
console.log(backErrorMessage)



completeName = document.getElementById('completeName')
emailCamp = document.getElementById('emailCamp')
emailLoginCamp = document.getElementById('emailLoginCamp')
pass1 = document.getElementById('pass1')
pass2 = document.getElementById('pass2')
passLoginCamp = document.getElementById('passwordLoginCamp')
errorMessage = document.getElementById('errorMessage')
radios = document.querySelectorAll('.radios')
submitRegisterButton = document.getElementById('submitButton')
submitLoginButton = document.getElementById('submitLoginButton')
defaultErrorMessage = backErrorMessage
errorMessage.innerHTML = defaultErrorMessage

if (backErrorMessage != ""){
    errorMessage.classList.remove('hiddeable')
}

submitRegisterButton.addEventListener('click', handleRegisterForm)
submitLoginButton.addEventListener('click', handleLoginForm)

function triggerError(e){
    errorMessage.classList.remove('hiddeable')
    e.preventDefault()
}

function handleRegisterForm(e){
    registerErrorMessage = "<div class='errors-header'>O registro não pôde ser concluído pois: </div>"
    errorMessage.innerHTML = registerErrorMessage
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

function handleLoginForm(e){
    loginErrorMessage = "<div class='errors-header'>O Login não pôde ser concluído pois: </div>"
    errorMessage.innerHTML = loginErrorMessage
    let count = 0
    errors = []
    var validRegex = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/;
    if (emailLoginCamp.value.match(validRegex)) {
        emailLoginCamp.classList.remove('error-camp')
    } 
    else {
        errors.push("<li>Formato de e-mail não válido!</li>")
        emailLoginCamp.classList.add('error-camp')
        count += 1
    }
    if(passLoginCamp.value == ""){
        errors.push('<li>Campo de senha não pode estar vazio!</li>')
        passLoginCamp.classList.add('error-camp')
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