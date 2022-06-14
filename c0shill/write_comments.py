from mod.youtube_connector import YoutubeConnector
from utils import list_video_info
import json
import os
from glob import glob
import pandas as pd
with open("secrets.json") as sio:
    fstr = sio.read()
    api_key = json.loads(fstr)["GCP_API_KEY"]

youtube_conn = YoutubeConnector(developer_key=api_key)

video_df = pd.read_csv("persist/cleansed/environmental_videos.csv")

ids = video_df[["videoId", "channelId"]].to_records(index=False)

for v_id, c_id in ids:
    j = 0 
    if j >= 100:
        break
    filedir = "persist/blob/channels/{0}/video_snippet/{1}/".format(c_id, v_id)
    os.makedirs(filedir, exist_ok=True)
    for chunk in youtube_conn.get_comments(video_id=v_id, part=["snippet", "replies"]):
        print(j)
        filepath = f"{filedir}/comments-pt-{j}.json"
        with open(filepath, "w+") as ioer:
            json.dump(chunk, ioer)
        j += 1
