console.log("Opa")

let machoCamp = document.getElementById('id_sex_0')
let femeaCamp = document.getElementById('id_sex_1')

let machoButton = document.getElementById('machoButton')
let femeaButton = document.getElementById('femeaButton')

machoButton.addEventListener('click', triggerMacho)
femeaButton.addEventListener('click', triggerFemea)

function triggerMacho(){
    if(machoCamp.checked == false){
        machoCamp.checked = true
        machoButton.classList.add('active-radio')
        femeaButton.classList.remove('active-radio')
    }
}

function triggerFemea(){
    if(femeaCamp.checked == false){
        femeaCamp.checked = true
        machoButton.classList.remove('active-radio')
        femeaButton.classList.add('active-radio')
    }
}