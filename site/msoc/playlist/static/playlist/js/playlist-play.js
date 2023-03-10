const btnPlay = document.querySelector("#play-musics")
const btnNextPlay = document.querySelector("#next-music")

let audioAll = document.querySelectorAll("audio")

const randomMusic = document.querySelector("ul.dropdown-menu > li > input.form-check-input")

let numMusic = 0
let modePlay = true


function Timer(fn, t) {
    let timerObj = setInterval(fn, t);

    this.stop = function() {
        if (timerObj) {
            this.stoped = true;
            clearInterval(timerObj);
            timerObj = null;
        }
        return this;
    }

    this.stoped = false;

    this.start = function() {
        if (!timerObj) {
            this.stop();
            timerObj = setInterval(fn, t);
            this.stoped = false;
        }
        return this;
    }

    this.stop()
}


function startAudio() {
    if (audioAll.length == 0) {
        interval.stop()
        return
    }
    
    let audio = audioAll[numMusic]
    if (!audio) {
        if (randomMusic.checked) {
            numMusic = Math.floor(Math.random() * audioAll.length)
        } else {
            numMusic = 0
        }

        return
    }

    if (!audio.paused || audio.currentTime == 0) {
        audio.play()
    }

    if (audio.ended) {
        if (randomMusic.checked) {
            numMusic = Math.floor(Math.random() * audioAll.length)
        } else {
            numMusic++
            if (numMusic == audioAll.length) {
                numMusic = 0
            }
        }
        
        audio.currentTime = 0
    }
}

const interval = new Timer(startAudio, 1000)
setInterval(() => {
    audioAll = document.querySelectorAll("audio")
}, 1000)

btnPlay.onclick = () => {
    btnPlay.classList.toggle("btn-primary")
    btnPlay.classList.toggle("btn-danger")
    btnNextPlay.toggleAttribute("disabled");

    const music = audioAll[numMusic]
    modePlay = !modePlay

    if (modePlay) {
        btnPlay.textContent = "Воспроизвести"
        interval.stop()

        music.pause()
    } else {
        btnPlay.textContent = "Остановить"
        interval.start()

        music.play()
    }
}

btnNextPlay.onclick = () => {
    const lastMusic = audioAll[numMusic]

    lastMusic.pause()
    lastMusic.currentTime = 0

    if (randomMusic.checked) {
        numMusic = Math.floor(Math.random() * audioAll.length)
    } else {
        numMusic++
    }
}