from cgi import print_directory
from multiprocessing import connection
import warnings
warnings.filterwarnings('ignore')
from datetime import datetime, timezone, timedelta
from tokenize import group
from telethon import TelegramClient, events, sync
from .sentiment import Sentiment
import telethon
from hazm import Normalizer
normalizer = Normalizer() 
from telegram.settings import MEDIA_ROOT
# MEDIA_ROOT = "../media"
import pytz
import pickle, os
from os import listdir
from os.path import isfile, join
def utc_to_local(utc_dt):
    return utc_dt.replace(tzinfo=timezone.utc).astimezone(pytz.timezone('Asia/Tehran'))


class CrawlerpPipeline:
    
    def __init__(self) -> None:
        self.channel_id = "t_kaj"
        self.sesseion = "moein"
        self.api_id = 1688602
        self.api_hash = '047ef442931cc10db39944883cab5041'
        dir_path = os.path.dirname(os.path.realpath(__file__))
        with open(
            os.path.join(dir_path, "data/symbols/symbols.pickle"),
            "rb"
        ) as f:
            self.symbols_dict = pickle.load(f)
            self.symbols = list(self.symbols_dict.keys())
        self.sentiment = Sentiment()
        self.connection_signs = [
            "_",
            "ـ",
            "‌",
            " "
        ]

    def get_symbols(self, text):
        symbols = []
        words = text.split()
        for symbol in self.symbols:
            if len(symbol.split()) == 1:
                if symbol in words and self.symbols_dict[symbol]["is_certain"]=="1":
                   symbols.append(symbol)
                elif "#" + symbol in words and self.symbols_dict[symbol]["is_certain"]=="1":
                   symbols.append(symbol) 
            else:
                symbol = symbol.split()
                indexes = []
                for sym in symbol:
                    index = words.index(sym) if sym in words else -1
                    if index >= 0:
                        if indexes:
                            if index==indexes[-1]+1:
                                indexes.append(index)
                            else:
                                indexes = []
                                break
                        else:
                            indexes.append(index)
                    else:
                        indexes = []
                        break
                    if indexes:
                        symbols.append(' '.join(symbol)) 

                pass
        return ','.join(symbols)

    def get_sentiment(self, text):
        return self.sentiment.predict(text)

    def get_start_number_of_image(self):
        onlyfiles = [f for f in listdir(MEDIA_ROOT) if isfile(join(MEDIA_ROOT, f))]
        return len(onlyfiles) + 1

    def crawl_channel(self, limit_datetime=None):
        with TelegramClient(self.sesseion, self.api_id, self.api_hash) as client:
            channel_name = client.get_entity(self.channel_id).title
            messages = client.get_messages(self.channel_id, limit=3000)
            print("received messages...")
            grouped_images = []
            image_counter = self.get_start_number_of_image()
            for i in range(0, len(messages)):
                # print(i)
                # print(messages[i])
                temp = {}
                # if  i == 20:
                #     print("i: ")
                #     exit()
                if limit_datetime is not None and messages[i].date < limit_datetime:
                    print("exceeded from date limitations")
                    exit()

                if type(messages[i].media) == telethon.tl.types.MessageMediaDocument:
                    print("Video")
                    continue

                if messages[i].message is None:
                    print("Message is None")
                    continue

                if messages[i].grouped_id:
                    if i+1 == len(messages) or messages[i+1].grouped_id is None or\
                    messages[i].grouped_id != messages[i+1].grouped_id:
                        # print("if counter", image_counter)
                        # print("if i counter", i)
                        temp['post_id'] = messages[i].id
                        temp['channel_id'] = messages[i].peer_id.channel_id
                        temp['channel_name'] = channel_name
                        temp['datetime'] = messages[i].date
                        temp['views'] = messages[i].views
                        temp['message'] = normalizer.normalize(messages[i].message)
                        temp['symbols'] = self.get_symbols(temp['message'])
                        temp['sentiment'] = self.get_sentiment(temp['message'])
                        if type(messages[i].media) == telethon.tl.types.MessageMediaPhoto:
                            # print("if media counter", image_counter)
                            # print("if media i counter", i)
                            grouped_images.append(str(image_counter)+".jpg")
                            messages[i].download_media(str(MEDIA_ROOT)+"/"+str(image_counter)+".jpg")
                            temp['photo'] = ",".join(grouped_images)
                            image_counter += 1
                        grouped_images = []
                        yield temp

                    elif messages[i+1].grouped_id == messages[i].grouped_id:
                        # print("if=next counter", image_counter)
                        # print("if=next i counter", i)
                        grouped_images.append(str(image_counter)+".jpg")
                        messages[i].download_media(str(MEDIA_ROOT)+"/"+str(image_counter)+".jpg")
                        image_counter += 1
                    
                else:
                    temp['post_id'] = messages[i].id
                    temp['channel_id'] = messages[i].peer_id.channel_id
                    temp['channel_name'] = channel_name
                    temp['datetime'] = messages[i].date
                    temp['views'] = messages[i].views
                    temp['message'] = normalizer.normalize(messages[i].message)
                    temp['symbols'] = self.get_symbols(temp['message'])
                    temp['sentiment'] = self.get_sentiment(temp['message'])
                    if type(messages[i].media) == telethon.tl.types.MessageMediaPhoto:
                        # print("else image counter", image_counter)
                        # print("else i counter", i)
                        messages[i].download_media(str(MEDIA_ROOT)+"/"+str(image_counter)+ ".jpg")
                        temp['photo'] = str(image_counter)+ ".jpg"
                        image_counter += 1
                    yield temp

    def crawl_channel_peridcially(self):
        res = []
        now = datetime.now()
        with TelegramClient(self.sesseion, self.api_id, self.api_hash) as client:
            for message in client.iter_messages(self.channel_id):
                temp = {}
                message.date = utc_to_local(message.date).strftime('%Y-%m-%d %H:%M:%S.%f %Z%z')
                compared_date = datetime.strptime(message.date, '%Y-%m-%d %H:%M:%S.%f %Z%z') + timedelta(hours=24)
                compared_date = str(compared_date).split("+")[0]
                compared_date = datetime.strptime(compared_date, '%Y-%m-%d %H:%M:%S')
                message.date = str(message.date).split("+")[0].split(".")[0]
                message.date = datetime.strptime(message.date, '%Y-%m-%d %H:%M:%S')

                if now<compared_date:
                    temp['post_id'] = message.id
                    temp['channel_id'] = message.peer_id.channel_id
                    temp['datetime'] = message.date
                    temp['views'] = message.views
                    temp['message'] = normalizer.normalize(message.message)
                    temp['symbols'] = self.get_symbols(temp['message'])
                    temp['sentiment'] = self.get_sentiment(temp['message'])
                    res.append(temp)
                else:
                    break
            return res

if __name__ == "__main__":
    crawler_pipeline = CrawlerpPipeline()
    i=0
    print("start")
    limit_datetime = datetime(2022, 8, 4)
    limit_datetime = pytz.utc.localize(limit_datetime)
    for r in crawler_pipeline.crawl_channel(limit_datetime):
        # print("i: ", str(i))
        i += 1
        # print(r)
        # print(str(r["images_path"])+"\n"+str(r["message"])+"\n"+str(r["sentiment"]))
    