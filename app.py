from flask import Flask, render_template_string
import json

app = Flask(__name__)

@app.route("/")
def musics():
    with open("musics.json", "r") as fr:
        musics = json.loads(fr.read())
    source = ""
    for k, v in musics.items():
        source += f'<p>{k}</p><video controls="" src="{v}" autoplay="" style="height: 40px; width: 66%;"></video>'
    return render_template_string(source)
