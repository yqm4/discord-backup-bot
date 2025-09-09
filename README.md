discordbot.py
AサーバーからBサーバーへチャンネル、ロールの移行　
一度Bサーバーのチャンネルなどを初期化してから以降を行います

TOKEN = "TOKEN"　discordbotのトークン

A_SERVER_ID = A_SERVER_ID　移行元のサバ　

B_SERVER_ID = B_SERVER_ID 移行後のサバ

適当に作ったコードなのでそこまで作り込んでないです。
後日webhook経由のメッセージコピーbotのソースコードも貼っておきます。

ikou.py 
webhook経由でメッセを移行します。
A_SERVER_ID = A_SERVER_ID　移行元のサバ　

B_SERVER_ID = B_SERVER_ID 移行後のサバ
チャンネルを同じ名前にするとできます。

﻿/transfer_logs_webhook_one これはチャンネル名を一緒にすればできる。
﻿/transfer_logs_webhook　これはチャンネルの名前が一緒のもののメッセを移行します
