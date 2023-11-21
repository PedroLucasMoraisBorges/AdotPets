message = document.getElementsByClassName('message')[0]

setTimeout(()=>{
    message.classList.add("slided")
}, 1000)

setTimeout(()=>{
    message.classList.remove("slided")
}, 7000)