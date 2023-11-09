    let carrouselInterval = null
    let carrouselIndicators = null
    let iterator = 0

    let petCards = document.querySelectorAll('.pet-card')
    petCards.forEach(card => {
        card.addEventListener('click', openPetModal)
    })

    function triggerCarrousel(id, carrousel, indicators){
        iterator = 0
        numImgs = carrousel.childElementCount
        moveQuantity = 0;
        indicators[0].classList.add('indicator-active')
        function carrouselIntervalFunction(){
            iterator += 1
            if (iterator > (numImgs - 1)){
                moveQuantity = 0
                iterator = 0
                carrousel.style.transform = 'translateX(-'+ moveQuantity +'%)'
                indicators.forEach(indicator=>{
                    indicator.classList.remove('indicator-active')
                })
                indicators[0].classList.add('indicator-active')
            }
            else{
                moveQuantity += 100
                carrousel.style.transform = 'translateX(-'+ moveQuantity +'%)'
                indicators.forEach(indicator=>{
                    indicator.classList.remove('indicator-active')
                })
                indicators[iterator].classList.add('indicator-active')
            }
        }
        function carrouselIntervalFunctionReverse(){
            iterator -= 1
            if (iterator < 0){
                moveQuantity = (numImgs - 1) * 100
                iterator = (numImgs - 1)
                carrousel.style.transform = 'translateX(-'+ moveQuantity +'%)'
                indicators.forEach(indicator=>{
                    indicator.classList.remove('indicator-active')
                })
                indicators[iterator].classList.add('indicator-active')
            }
            else{
                carrousel.style.transform = 'translateX(-'+ (moveQuantity - 100) +'%)'
                indicators.forEach(indicator=>{
                    indicator.classList.remove('indicator-active')
                })
                indicators[iterator].classList.add('indicator-active')
                moveQuantity -= 100
            }
        }
        carrouselInterval = setInterval(carrouselIntervalFunction, 4000)

        let nextImageTrigger = document.querySelector('#triggerAfter-' + id)
        nextImageTrigger.addEventListener('click', nextImage)
        let prevImageTriggers = document.querySelector('#triggerBefore-' + id)
        prevImageTriggers.addEventListener('click', prevImage)

        function nextImage(e){
            clearInterval(carrouselInterval)
            carrouselInterval = setInterval(carrouselIntervalFunction, 4000)
            carrouselIntervalFunction()
            e.stopImmediatePropagation()
            console.log(iterator)
            console.log(moveQuantity)
        }

        function prevImage(e){
            clearInterval(carrouselInterval)
            carrouselInterval = setInterval(carrouselIntervalFunction, 4000)
            carrouselIntervalFunctionReverse()
            e.stopImmediatePropagation()
        }
    }

    function openPetModal(e){
        id = e.currentTarget.getAttribute('id').replace('pet-card-', '')
        let referenceForModal = 'modal-pet-' + id
        let modal = document.getElementById(referenceForModal)
        modal.classList.remove('hidden')
        modal.children[0].classList.add('animation')
        
        
        
        let referenceForCarrousel = 'carrousel-' + id
        let carrousel = document.getElementById(referenceForCarrousel)
        let referenceForCarrouselIndicators = '.carrousel-indicator-' + id
        carrouselIndicators = document.querySelectorAll(referenceForCarrouselIndicators)

        triggerCarrousel(id, carrousel, carrouselIndicators)
    }


    let modals = document.querySelectorAll('.modal-pet-container')
    modals.forEach(modal => {
        modal.addEventListener('click', closeModal)
    })

    function closeModal(e){
        clickedOutOfModal = e.target.classList.contains('modal-pet-container')
        clickedXButton = e.target.classList.contains('exit-modal-button')
        if (clickedOutOfModal == true || clickedXButton == true){
            e.currentTarget.classList.add('hidden')
            e.currentTarget.classList.remove('animation')
        }

        target = e.currentTarget
        id = e.currentTarget.getAttribute('id').replace('modal-pet-', '')
        let referenceForCarrousel = 'carrousel-' + id
        let carrousel = document.getElementById(referenceForCarrousel)
        let referenceForCarrouselIndicators = '.carrousel-indicator-' + id
        carrouselIndicators = document.querySelectorAll(referenceForCarrouselIndicators)

        if(e.target.classList.contains('modal-pet-container')){
            carrousel.style.transform = 'translateX(0%)'    
            clearInterval(carrouselInterval)
            carrouselIndicators.forEach(indicator=>{
                indicator.classList.remove('indicator-active')
            })
            carrouselIndicators[0].classList.add('indicator-active')
            iterator = 0
        }
    }

    // Contact options for lost pets
    
    let contactButtons = document.querySelectorAll(".contact-button")
    contactButtons.forEach(button => {
        button.addEventListener("click", toggleContactDiv)
    })

    function toggleContactDiv(e){
        button = e.target
        id = button.getAttribute('id').replace("contactButton-", "")
        referenceForContactDiv = "#contactDiv-" + id
        div = document.querySelector(referenceForContactDiv)
        div.classList.toggle("visible");
    }
    
    let requestText = document.querySelector('#requestTextContainer')
    let request = document.querySelector('#requestText')
    let exitRequestTextButton = document.querySelector("#exitRequestText")
    requestText.addEventListener('click', modalClose)
    exitRequestTextButton.addEventListener('click', hideRequestText)

    function hideRequestText(){
        requestText.classList.add('hidden')
        request.value = ""
    }

    function modalClose(e){
        target = e.target
        id = target.getAttribute('id')
        if(id == 'requestTextContainer'){
            hideRequestText()
        }
    }

    function toggleRequestText(e){
        petId = e.target.getAttribute('petId')
        document.querySelector("#requestIdPet").setAttribute('value', petId)

        userId = e.target.getAttribute('userId')
        document.querySelector("#requestIdUser").setAttribute('value', userId)
    
        requestText.classList.toggle('hidden')
    }

    let adoptButtons = document.querySelectorAll('.adopt-button')
    adoptButtons.forEach(button => {
        button.addEventListener("click", toggleRequestText)
    })

    /* Fazendo animação de processo de ações (PROCESSANDO...) */

    let sendRequestText = document.querySelector("#sendRequestText")
    let requestForm = document.querySelector(".request-text-around")
    let processingContainer = document.querySelector(".processing-container")

    sendRequestText.addEventListener("click", processingAnimation)

    function processingAnimation(){
        requestForm.classList.add("hidden")
        processingContainer.classList.remove("hidden")
    }

    /* Final dessa seção */