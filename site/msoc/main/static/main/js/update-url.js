const audioUpdateAll = document.querySelectorAll("audio")

audioUpdateAll.forEach(audio => {
    setTimeout(() => {
        if (!audio.duration) {
            setTimeout(() => {
                audio.load()
            }, 1000)
        }
    }, 3000)
})
