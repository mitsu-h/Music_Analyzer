import json
from datetime import datetime
import random

import boto3


def generate_uuid(seed):
    random.seed(seed)
    uuid_parts = [
        "".join(random.choices("0123456789abcdef", k=8)),
        "".join(random.choices("0123456789abcdef", k=4)),
        "".join(random.choices("0123456789abcdef", k=4)),
        "".join(random.choices("0123456789abcdef", k=4)),
        "".join(random.choices("0123456789abcdef", k=12)),
    ]
    return "-".join(uuid_parts)


# ダミーデータの作成
user_id_seed = 42
analysis_id_seed = 102

user_id = generate_uuid(user_id_seed)
analysis_id = generate_uuid(analysis_id_seed)


dynamodb = boto3.resource(
    "dynamodb", endpoint_url="http://localhost:8082"  # "http://dynamodb-local:8000",
)

table_name = "AnalysisResults"

try:
    table = dynamodb.Table(table_name)
except:
    # テーブルを作成
    table = dynamodb.create_table(
        TableName=table_name,
        KeySchema=[
            {"AttributeName": "user_id", "KeyType": "HASH"},
            {"AttributeName": "analysis_id", "KeyType": "RANGE"},
        ],
        AttributeDefinitions=[
            {"AttributeName": "user_id", "AttributeType": "S"},
            {"AttributeName": "analysis_id", "AttributeType": "S"},
        ],
        ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
    )

    table.meta.client.get_waiter("table_exists").wait(TableName=table_name)
    print(f"{table_name} table is created")

# ダミーデータを作成
target_title_path = "08 愛のけだもの"
spleeter_path = "s3://music/spleeter/" + target_title_path
dummy_data = {
    "user_id": user_id,
    "analysis_id": analysis_id,
    "youtube_video_url": "https://www.youtube.com/watch?v=7o7_OXsvu7E",
    "title": target_title_path,
    "artist": "神はサイコロを振らない",
    "youtube_description": "YouTube Video Description",
    "source_type": "youtube",
    "audio_file": f"s3://music/original/{target_title_path}.m4a",
    "separated_audio_files": json.dumps(
        {
            "vocals": f"{spleeter_path}/vocals.wav",
            "drums": f"{spleeter_path}/drums.wav",
            "bass": f"{spleeter_path}/bass.wav",
            "other": f"{spleeter_path}/other.wav",
        }
    ),
    "last_played_position": 0,
    "loop_intervals": json.dumps(
        [{"start": 0, "end": 10}], [{"start": 0, "end": 10}], [{"start": 0, "end": 10}]
    ),
    "playback_speed": 1,
    "instruments_volume": json.dumps({"vocals": 1, "drums": 1, "bass": 1, "other": 1}),
    "created_at": datetime.utcnow().isoformat(),
    "updated_at": datetime.utcnow().isoformat(),
    "comment": "Sample comment",
}

# ダミーデータをテーブルに追加
table.put_item(Item=dummy_data)
print(f"Dummy data is added to {table_name} table")
