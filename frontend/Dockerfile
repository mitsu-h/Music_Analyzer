# ベースイメージとして Node.js の最新 LTS バージョンを使用
FROM node:14

# 作業ディレクトリの設定
WORKDIR /app

# Vue CLI のグローバルインストール
RUN npm install -g @vue/cli

# プロジェクトの依存関係をインストール
COPY package*.json ./
RUN npm install

# ソースコードをコンテナにコピー
COPY . .

# 開発サーバーを起動
CMD ["npm", "run", "serve"]
