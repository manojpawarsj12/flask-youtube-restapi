from flask import Flask, request, Response, render_template
from yout import YoutubeSearch
import requests
import youtube_dl
from uuid import uuid4
from urllib.parse import unquote
from os import environ

app = Flask(__name__)


def yt_url(url):
    ydl_opts = {
        "format": "bestaudio/best",
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "320",
            }
        ],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:

        result = ydl.extract_info(url, download=False)
    return result.get("url")


@app.route("/search/<sed>", methods=["GET"])
def get_search(sed):
    app.logger.info("%s has been searched ", sed)
    sed = str(sed)
    sed = sed.replace("_", " ")
    title = dict()
    search_query = str(sed)
    print(search_query)
    search_results = YoutubeSearch(str(search_query), max_results=5).to_dict()
    for i in search_results:
        title[i["title"]] = "https://youtube.com" + i["url_suffix"]

    return title


@app.route("/stream/<ok>")
def get_stream(ok):
    app.logger.info("%s has been played ", ok)
    ok = str(ok)
    ok = ok.replace("_", " ")
    print(ok)
    search_results = YoutubeSearch(str(ok), max_results=1).to_dict()
    for i in search_results:
        url = "https://youtube.com" + i["url_suffix"]
    app.logger.info("url : %s ", url)
    yturl = yt_url(url)
    r = requests.get(yturl, stream=True)
    return Response(
        r.iter_content(chunk_size=10 * 1024), content_type=r.headers["Content-Type"]
    )


@app.route("/")
def hello():
    return render_template("index.html")


if __name__ == "__main__":
    port = int(environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)

