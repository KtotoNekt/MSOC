const buttonsAdd = document.querySelectorAll("#div-search > ul > li > div > ul > li > button")


buttonsAdd.forEach(btn => {
    btn.onclick = e => {
        getURL(btn, e.target.value, `Песня "${e.target.name}" успешно добавлена в плейлист "${e.target.textContent}"`)
    }
})