import argparse
import boto3
import os
import shutil
from spleeter.separator import Separator


def separate_and_upload_to_s3(input_file_path, s3_client, output_s3_bucket="music"):
    # Spleeterの設定
    separator = Separator("spleeter:4stems-16kHz")

    # 出力ディレクトリの設定
    print(input_file_path)
    title = os.path.splitext(os.path.basename(input_file_path))[0]
    output_dir_path = f"/tmp_audio/spleeter/"

    # Spleeterで音源を分離
    separator.separate_to_file(input_file_path, output_dir_path, codec="wav")

    # 各トラックごとにS3にアップロード
    separated_audio_files = {}
    for root, dirs, files in os.walk(output_dir_path):
        for file in files:
            file_path = os.path.join(root, file)

            # S3のキー (パス) の設定
            s3_key = f"spleeter/{title}/{file}"

            # S3にアップロード
            s3_client.upload_file(file_path, output_s3_bucket, s3_key)

            # ファイル名からトラック名を取得 (e.g., "vocals.wav" -> "vocals") し、S3のパスを辞書に記録
            track_name = os.path.splitext(file)[0]
            separated_audio_files[track_name] = f"s3://{output_s3_bucket}/{s3_key}"

    # 出力ディレクトリを削除
    shutil.rmtree(output_dir_path + title)

    return separated_audio_files


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Separate audio file into stems and upload to S3."
    )
    parser.add_argument(
        "input_file_path", type=str, help="Path to the input audio file."
    )
    parser.add_argument(
        "--output_s3_bucket",
        type=str,
        default="music",
        help="Name of the output S3 bucket.",
    )

    args = parser.parse_args()

    # Initialize S3 client.
    endpoint_url = os.getenv("S3_ENDPOINT")
    s3_client = boto3.client("s3", endpoint_url=endpoint_url)

    # Call the separate_and_upload_to_s3 function.
    separated_audio_files = separate_and_upload_to_s3(
        args.input_file_path, s3_client, args.output_s3_bucket
    )

    # Print the returned dictionary.
    print(separated_audio_files)
