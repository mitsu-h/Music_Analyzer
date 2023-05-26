import os

import yt_dlp


def _get_video_info(url):
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


def download_youtube_audio_info(url, s3_client, output_s3_bucket):
    output_dir = "/tmp_audio/originals/"

    # Ensure directory exists
    os.makedirs(output_dir, exist_ok=True)

    ydl_opts = {
        "format": "bestaudio/best",
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "wav",
                "preferredquality": "192",
            }
        ],
        "outtmpl": output_dir + "%(title)s.%(ext)s",
        "writesubtitles": True,
        "writeinfojson": True,
        "writethumbnail": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        file_path = ydl.prepare_filename(info).replace(".webm", ".wav")
        description = info.get("description", "")
        duration = info.get("duration", 0)

        # S3のキー (パス) の設定
        s3_key = f"original/{os.path.basename(file_path)}"
        # S3にアップロード
        s3_client.upload_file(file_path, output_s3_bucket, s3_key)

    return file_path, description, duration, f"s3://{output_s3_bucket}/{s3_key}"


if __name__ == "__main__":
    url = "https://www.youtube.com/watch?v=29t3pJd75XU"  # 任意の YouTube 動画の URL
    video_info = _get_video_info(url)

    if video_info:
        print(f"Title: {video_info['title']}")
        print(f"Channel: {video_info['channel']}")
        filename, description, duration, s3_path = download_youtube_audio_info(url)
        print(f"wav filename: {filename}")
        print(f"description: {description}")
        print(f"audio duration: {duration}")
    else:
        print("Failed to get video information")
