from glob import glob
from typing import List, Generator, Dict

def get_file_paths(feed: str) -> List[str]:
    return glob(f"blob/{feed}/*/*")

def list_video_info(video_response: Dict) -> Generator[str, None, None]:
    channel_id = video_response["channel_id"]
    channel_name = video_response["channel_name_px"]
    for elem in video_response["items"]:
        yield {
            "video_id": elem["contentDetails"]["videoId"],
            "channel_id": channel_id,
            "channel_name": channel_name
        }