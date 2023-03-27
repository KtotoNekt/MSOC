const musicName = document.querySelector("p.title")

const buttonsAdd = document.querySelectorAll("#div-add-playlist > li > button")
const buttonsDel = document.querySelectorAll("#div-del-playlist > li > button")


buttonsAdd.forEach(btn => {
    btn.onclick = e => {
        getURL(btn, e.target.value, `Песня "${musicName.textContent}" успешно добавлена в плейлист "${e.target.textContent}"`)
    }
})

buttonsDel.forEach(btn => {
    btn.onclick = e => {
        getURL(btn, e.target.value, `Песня "${musicName.textContent}" успешно удалена из плейлиста "${e.target.textContent}"`)
    }
})