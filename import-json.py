import requests
import json
import sqlite_utils
from datetime import date

# WARNING - THIS TAKES AGES TO RUN!
db = sqlite_utils.Database("commonplaces-.db")
comments = ['lewishamlocalplanmap',
    "lewishamstreetsmap",
    "rusheygreenncilmap",
    "downhamncilmap",
    "perryvalencilmap",
    "bellinghamncilmap",
    "ladywellncilmap",
    "blackheathncilmap",
    "telegraphhillncilmap",
    "sydenhamncilmap",
    "foresthillncilmap",
    "newcrossncilmap",
    "rusheygreenncilmap",
    "catfordsouthncilmap",
    "groveparkncilmap",
    "leegreenncilmap",
    "croftonparkncilmap",
    "brockleyncilmap",
    "evelynncilmap",
    "whitefootncilmap",
    "lewishamcentralncilmap",
    "lewishamlocalplanmap",
]

for survey in comments:
    print(survey)
    url = "https://" + survey + ".commonplace.is/api/v1/spatial/comments.geojson"
    comment_url_head = "https://" + survey + ".commonplace.is/comments.json/"
    req = requests.get(url, headers={"Connection": "close"})
    data = req.json()

    if db[survey].exists():
        db[survey].drop(ignore=True)

    db[survey].create(
        {
            "id": str,
            "origin": str,
            "date": date,
            "agree": str,
            "shortUrl": str,
            "consent": int,
            "feeling": int,
            "longitude": float,
            "latitude": float,
            "language": str,
            "fields": str,
        },
        pk="id",
    )

    for feature in data["features"]:
        comment_url = comment_url_head + feature["properties"]["id"]
        req = requests.get(comment_url, headers={"Connection": "close"})
        try:
            db[survey].upsert(req.json(), pk="id")
        except Exception as e:
            print(survey, req.json(), e)
