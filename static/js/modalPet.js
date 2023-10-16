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
        if (clickedOutOfModal == true){
            e.currentTarget.classList.add('hidden')
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