from functools import wraps
from googleapiclient.discovery import build


class YoutubeConnector:
    def __init__(self, developer_key: str) -> None:
        self._developer_key = developer_key
        self._disco = self._build_discovery()


    def paginate(req):
        @wraps(req)
        def inner(*args, **kwargs):
            page_token = ""
            while True:
                response = req(*args, **kwargs, pageToken=page_token)
                page_token = response.get("nextPageToken")
                if page_token:
                    yield response
                else:
                    break
        return inner

    def _build_discovery(self):
        return build(
            serviceName="youtube", version="v3", developerKey=self._developer_key
        )

    @paginate
    def get_comments(self, video_id, part, **kwargs):
        comment_lazy = self._disco.commentThreads().list(
            part=",".join(part), videoId=video_id, **kwargs
        )
        comment_response = comment_lazy.execute()
        return comment_response

    def _get_channel_upload_id(self, channel_id):
        channel_content_lazy = self._disco.channels().list(
            part="contentDetails", id=channel_id, maxResults=50
        )
        channel_content = channel_content_lazy.execute()
        response_items = channel_content["items"]
        if len(response_items) > 1:
            raise Exception(
                "Undefined behaviour - response contains more than 1 element."
            )
        upload_id = response_items[0]["contentDetails"]["relatedPlaylists"]["uploads"]
        return upload_id

    def get_videos(self, channel_id, part):
        channel_upload_id = self._get_channel_upload_id(channel_id)
        return self._get_videos(channel_upload_id, part)

    @paginate
    def _get_videos(self, channel_upload_id, part, **kwargs):
        videos_lazy = self._disco.playlistItems().list(
            part=",".join(part), playlistId=channel_upload_id, maxResults=50, **kwargs
        )
        videos = videos_lazy.execute()
        return videos
