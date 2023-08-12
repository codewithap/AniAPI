from utils import getM3u8
from scrappers import gogoscrapper
import time
from flask import Flask, request

app = Flask("__name__")
gogoanime = gogoscrapper()

@app.route("/")
def home():
    return "<h1>Hello,World!</h1>"

@app.route("/episodes")
def anime():
    name = request.args.get("name")
    return gogoanime.getEpis(name)

@app.route("/m3u8")
def getvideo():
    epid = request.args.get("id")[2:-1]
    return gogoanime.episodeJson(epid)



if __name__== "__main__":
    app.run(debug=True, host="0.0.0.0")


