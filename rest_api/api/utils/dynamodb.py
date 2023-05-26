from datetime import datetime
import json
import os
import random
import uuid

import boto3


def get_dynamodb_client():
    endpoint_url = os.getenv("DYNAMODB_ENTRYPOINT")
    client = boto3.client("dynamodb", endpoint_url=endpoint_url)
    return client


def generate_uuid(seed):
    """seed固定でuuidを生成する

    Args:
        seed (_type_): _description_

    Returns:
        _type_: _description_
    """
    random.seed(seed)
    uuid_parts = [
        "".join(random.choices("0123456789abcdef", k=8)),
        "".join(random.choices("0123456789abcdef", k=4)),
        "".join(random.choices("0123456789abcdef", k=4)),
        "".join(random.choices("0123456789abcdef", k=4)),
        "".join(random.choices("0123456789abcdef", k=12)),
    ]
    return "-".join(uuid_parts)


def put_analyze_info(
    user_id,
    youtube_video_url,
    title,
    artist,
    description,
    original_audio_file,
    separated_audio_files,
    duration,
    table,
):
    analysis_id = uuid.uuid4()
    split_duration = duration / 3
    data = {
        "user_id": {"S": user_id},
        "analysis_id": {"S": str(analysis_id)},
        "youtube_video_url": {"S": youtube_video_url},
        "title": {"S": title},
        "artist": {"S": artist},
        "youtube_description": {"S": description},
        "source_type": {"S": "youtube"},
        "audio_file": {"S": original_audio_file},
        "separated_audio_files": {"S": json.dumps(separated_audio_files)},
        "last_played_position": {"N": "0"},
        "loop_intervals": {
            "S": json.dumps(
                [
                    [0, split_duration],
                    [split_duration, split_duration * 2],
                    [split_duration * 2, duration],
                ]
            )
        },
        "playback_speed": {"N": "1"},
        "instruments_volume": {
            "S": json.dumps({"vocals": 1, "drums": 1, "bass": 1, "other": 1})
        },
        "created_at": {"S": datetime.utcnow().isoformat()},
        "updated_at": {"S": datetime.utcnow().isoformat()},
        "comment": {"S": ""},
    }

    # ダミーデータをテーブルに追加
    table.put_item(TableName="AnalysisResults", Item=data)

    print(f"put data: {data}")
