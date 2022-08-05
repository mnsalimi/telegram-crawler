from datetime import datetime, timezone, timedelta
from telethon import TelegramClient, events, sync

import pytz

def utc_to_local(utc_dt):
    return utc_dt.replace(tzinfo=timezone.utc).astimezone(pytz.timezone('Asia/Tehran'))


class TelegramCrawler:
    def __init__(self) -> None:
        self.api_id = 1684286022
        self.api_hash = '1688656102'
    
    def crawle_channel(self):
        res = []
        now = datetime.now()
        with TelegramClient("moein", self.api_id, self.api_hash) as client:
            for message in client.iter_messages("tehranboursemarket"):
                temp = {}
                message.date = utc_to_local(message.date).strftime('%Y-%m-%d %H:%M:%S.%f %Z%z')
                message.date = datetime.strptime(message.date, '%Y-%m-%d %H:%M:%S.%f %Z%z') + timedelta(hours=24)
                message.date = str(message.date).split("+")[0]
                message.date = datetime.strptime(message.date, '%Y-%m-%d %H:%M:%S') 
                if now<message.date:
                    temp['post_id'] = message.id
                    temp['channel_id'] = message.peer_id.channel_id
                    temp['datetime'] = message.date
                    temp['message'] = message.message
                    temp['views'] = message.views
                    res.append(temp)
                else:
                    break
            return res

if __name__ == "__main__":
    telegram_crawler = TelegramCrawler()
    res = telegram_crawler.crawle_channel()
    print(res)