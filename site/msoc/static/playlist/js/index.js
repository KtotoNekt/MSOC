const buttonsDelete = document.querySelectorAll("button.btn.btn-danger.p-2")


buttonsDelete.forEach(btn => {
    btn.onclick = e => {
        const url = btn.value

        const xhr = new XMLHttpRequest()

        xhr.open("GET", url)

        xhr.onload = () => {
            if (xhr.status >= 400) {
                alert("Произошла ошибка... Попробуйте чуть позже")
            } else {
                
                const ul = btn.parentElement.parentElement.parentElement

                if (ul.childElementCount == 1) {
                    const li = document.createElement("li")
                    const p = document.createElement("p")

                    p.textContent = "Пустой плейлист"

                    li.classList.add("list-group-item")
                    li.classList.add("bg-dark")
                    li.classList.add("text-white")
                    li.classList.add("rounded-4")

                    li.appendChild(p)

                    ul.appendChild(li)
                }

                e.target.offsetParent.remove()
            }
        }
    
        xhr.onerror = er => {
            console.log(er)
        }

        xhr.send()
    }
})