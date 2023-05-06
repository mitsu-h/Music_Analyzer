# Python の公式イメージをベースにします
FROM python:3.9

# ワーキングディレクトリを設定します
WORKDIR /app

# 必要なパッケージをインストールします
RUN apt-get update && \
    apt-get install -y ffmpeg

# requirements.txt をコピーし、依存関係をインストールします
COPY requirements.txt ./
RUN python -m pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# プロジェクトのファイルをコピーします
COPY . .

# Django アプリケーションを実行します
CMD ["python", "manage.py", "runserver", "0.0.0.0:8081"]

