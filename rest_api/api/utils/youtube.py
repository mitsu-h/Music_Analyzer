import yt_dlp


def get_video_info(url):
    ydl_opts = {
        "quiet": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            video_info = ydl.extract_info(url, download=False)
            return {
                "title": video_info["title"],
                "channel": video_info["uploader"],
            }
        except Exception as e:
            print(f"Error occurred: {e}")
            return None


if __name__ == "__main__":
    url = "https://www.youtube.com/watch?v=clB3yOKaayE"  # 任意の YouTube 動画の URL
    video_info = get_video_info(url)

    if video_info:
        print(f"Title: {video_info['title']}")
        print(f"Channel: {video_info['channel']}")
    else:
        print("Failed to get video information")
