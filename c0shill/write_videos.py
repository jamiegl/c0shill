from mod.youtube_connector import YoutubeConnector
import json
import os

with open("secrets.json") as sio:
    fstr = sio.read()
    api_key = json.loads(fstr)["GCP_API_KEY"]

youtube_conn = YoutubeConnector(developer_key=api_key)

with open("c0shill/data/channels.json") as reader:
    strout = reader.read()
    channels = json.loads(strout)

for row in channels:
    channel_id = row["id"]
    channel_meta = youtube_conn.get_videos(
        channel_id=channel_id,
        part=["snippet","contentDetails"]
    )
    i = 0
    for chunk in channel_meta:
        if i > 100:
            break
        print(i)
        chunk["channel_id"] = channel_id
        chunk["channel_name_px"] = row["channel"]
        filedir = f"persist/blob/channels/{channel_id}/video_list"
        os.makedirs(filedir, exist_ok=True)
        filepath = f"{filedir}/videos-pt-{i}.json"
        with open(filepath, "w+") as ioer:
            json.dump(chunk, ioer)
        i += 1
