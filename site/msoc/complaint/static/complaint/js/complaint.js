const buttonsAcceptComplaint = document.querySelectorAll("button.accept")
const buttonsDeclineComplaint = document.querySelectorAll("button.decline")


function sendGetDeleteComplaint(url) {
    const xhr = new XMLHttpRequest()

    xhr.open("GET", url)

    xhr.onload = e => {
        if (xhr.status >= 400) {
            alert("Произошла ошибка... Попробуйте чуть позже")
        }
    }

    xhr.onerror = er => {
        console.log(er)
    }

    xhr.send()
}


buttonsAcceptComplaint.forEach(btn => {
    btn.onclick = () => {
        const urlDeleteComplaint = btn.parentElement.getAttribute("url-delete-complaint")

        sendGetDeleteComplaint(urlDeleteComplaint)

        const xhr = new XMLHttpRequest()

        xhr.open("GET", btn.value)

        xhr.onload = e => {
            if (xhr.status >= 400) {
                alert("Произошла ошибка... Попробуйте чуть позже")
            } else {
                btn.parentElement.parentElement.remove()
            }
        }
    
        xhr.onerror = er => {
            console.log(er)
        }
    
        xhr.send()
    }
})

buttonsDeclineComplaint.forEach(btn => {
    btn.onclick = () => {
        const urlDeleteComplaint = btn.parentElement.getAttribute("url-delete-complaint")
        sendGetDeleteComplaint(urlDeleteComplaint)
        btn.parentElement.parentElement.remove()
    }
})

