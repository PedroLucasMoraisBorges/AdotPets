let exitRequestButtons = document.querySelectorAll('.exit-request-button')
exitRequestButtons.forEach(button => {
    button.addEventListener('click', closeRequestModals)
})

function closeRequestModals(){
    let modalRequests = document.querySelectorAll('.modal-request')
    modalRequests.forEach(modal => {
        modal.classList.add('hidden')
    })
}


let requestsButtons = document.querySelectorAll('.requests-button')
requestsButtons.forEach(button => {
    button.addEventListener('click', openRequestsModal)
})

function openRequestsModal(e){
    id = e.target.getAttribute('petId')
    document.getElementById('modal-request-' + id).classList.remove('hidden')
}