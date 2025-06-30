# ファイル名: github_to_discord.py

from flask import Flask, request
import requests

# ✅ DiscordのWebhook URLを貼り付けてください
DISCORD_WEBHOOK_URL = "https://discordapp.com/api/webhooks/1389091790774075483/x4fAwsn3IWahIR5ZqtMxMHRyRAqt4dXHqhEiV2esj38XN5bENx_mpAw30ALluenolucB"

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def github_webhook():
    data = request.json

    # PRが「作成（opened）」されたときだけ反応
    if data.get("action") == "opened" and "pull_request" in data:
        pr = data["pull_request"]
        title = pr["title"]
        url = pr["html_url"]
        user = pr["user"]["login"]
        repo = data["repository"]["full_name"]

        # Discordに送るメッセージを作成
        message = {
            "content": (
                f"🆕 **新しいプルリクエストが作成されました！**\n"
                f"📂 リポジトリ: `{repo}`\n"
                f"📝 タイトル: `{title}`\n"
                f"🙋 作成者: `{user}`\n"
                f"🔗 [PRリンクはこちら]({url})"
            )
        }

        # Discordに送信
        res = requests.post(DISCORD_WEBHOOK_URL, json=message)
        print(f"Discord通知結果: {res.status_code}")

    return "", 204

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
