from datetime import datetime
from dateutil import tz

# JST（日本標準時）のタイムゾーンを取得
jst = tz.gettz('Asia/Tokyo')

# 現在の日付と時刻をUTC（協定世界時）で取得
now_utc = datetime.utcnow()

# JST（日本標準時）に変換
now_jst = now_utc.replace(tzinfo=tz.tzutc()).astimezone(jst)

print("Today's date in JST:", now_jst)
