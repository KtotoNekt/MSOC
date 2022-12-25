from flask import Flask, render_template_string
import json

app = Flask(__name__)

@app.route("/")
def musics():
    with open("musics.json", "r") as fr:
        musics = json.loads(fr.read())
    source = f"<p>Если на странице не загружаются некоторые песни, попробуйте перезагрузить страницу и отключить расширения для блокировки рекламы и т. п.</p>"
    for k, v in musics.items():
        source += f'<p>{k}</p><video controls="" src="{v}" autoplay="" style="height: 40px; width: 66%;"></video>'
    return render_template_string(source)
