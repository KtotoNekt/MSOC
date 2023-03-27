
function getURL(btn, url, messageSuccess) {
    const xhr = new XMLHttpRequest()

    xhr.open("GET", url)

    xhr.onload = e => {
        if (xhr.status >= 400) {
            alert("Произошла ошибка... Попробуйте чуть позже")
        } else {
            btn.disabled = true
            alert(messageSuccess)
        }
    }

    xhr.onerror = er => {
        console.log(er)
    }

    xhr.send()
}


