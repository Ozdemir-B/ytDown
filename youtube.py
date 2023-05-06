"""Set of functions for working with YouTube"""

from os.path import join
from typing import Any, NamedTuple

from yt_dlp import YoutubeDL
from yt_dlp.utils import YoutubeDLError





class VideoInfo(NamedTuple):
    """Presents information about the video"""

    description: str
    url: str


class YouTube:
    """Describes methods for working with YouTube videos"""

    
    def _remove_unwanted_chars(string: str) -> str:
        """Removes everything from the string except letters, numbers, spaces, hyphens, and underscores"""
        processed_string: str = ""
        for char in string[:100]:
            if char.isalnum() or char == "-" or char == "_":
                processed_string += char
            elif char.isspace() and (not processed_string or not processed_string[-1].isspace()):
                processed_string += char
        return processed_string

    
    def get_thumbnail(self,url:str) -> Any:
        """
        Downloads the best video stream from the YouTube Shorts link
        Note: Do not use named arguments when calling this method
        Args:
            youtube_watch_url (): link to YouTube Shorts video
        Returns:
            The path to the uploaded video file, or None if the original video file is a live broadcast
        """
        options: dict = {
            "format": "best",
            "geo_bypass": True,
            "noplaylist": True,
            "noprogress": True,
            "quiet": True,
        }
        ydl: YoutubeDL = YoutubeDL(params=options)

        try:
            # Getting information about the video
            video_info = ydl.extract_info(url, download=False)

            return video_info.get("thumbnail")
        except Exception as e:
            print("getThumbnail error ::: ")
            print(e)
            return "Error"
    
    
    def download_video(self, youtube_watch_url: str,id:str) -> Any:
        """
        Downloads the best video stream from the YouTube Shorts link
        Note: Do not use named arguments when calling this method
        Args:
            youtube_watch_url (): link to YouTube Shorts video
        Returns:
            The path to the uploaded video file, or None if the original video file is a live broadcast
        """
        options: dict = {
            "format": "best",
            "geo_bypass": True,
            "noplaylist": True,
            "noprogress": True,
            "quiet": True,
        }
        ydl: YoutubeDL = YoutubeDL(params=options)

        try:
            # Getting information about the video
            video_info = ydl.extract_info(youtube_watch_url, download=False)
            duration: int | None = video_info.get("duration")

            if duration and duration <= 60:
                # Set save folder and file name
                #print(video_info)
                for v in video_info:
                    pass
                    #print(v,end="--")
                print(type(video_info.get("thumbnail")))
                print(video_info.get("thumbnail"))
                title: str = video_info.get("title")
                print(title)
                path_to_file: str = f"static/{id}.mp4"
                params: dict = getattr(ydl, "params")
                params.update({"outtmpl": {"default": path_to_file}})
                setattr(ydl, "params", params)
                #print(params)
                # Load a video stream
                ydl.download(youtube_watch_url)
                
                print("ended...")
                return f"{path_to_file}", title

        except YoutubeDLError as ex:
            print("Error when loading video: %s", repr(ex))

        return None


if __name__ == "__main__":
    youtube = YouTube()
    x=youtube.download_video("https://www.youtube.com/shorts/u1c9TRKkYgE","some_name")#"https://www.youtube.com/watch?v=Llr2dcd-VBo")#"https://www.youtube.com/shorts/u1c9TRKkYgE")
    #print(x)
