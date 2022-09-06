
import os
import re
import pickle
import pytz
import telethon
import warnings
warnings.filterwarnings('ignore')
from os import listdir
from hazm import Normalizer
from .sentiment import Sentiment
from os.path import isfile, join
from telethon import TelegramClient
from telegram.settings import MEDIA_ROOT
from datetime import datetime, timezone, timedelta


def utc_to_local(utc_dt):
    return utc_dt.replace(tzinfo=timezone.utc).astimezone(pytz.timezone('Asia/Tehran'))


class CrawlerPipeline:
    
    def __init__(self) -> None:
        self.normalizer = Normalizer() 
        self.channel_id = "ariyaz_1"
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
        self.flag_words = [
            "+۱",
            "+۲",
            "+۳",
            "+۴",
            "+۵",
            "+۶",
            "-۱",
            "-۲",
            "-۳",
            "-۴",
            "-۵",
            "-۶",
            "سرخطی",
            "رالی",
            "کانال",
            "نماد",
            "نمادهای",
            "سهم",
            "سهم‌های",
            "سهمهای",
            "سهام",
            "سهام‌های",
            "سهامهای",
            "شرکت",
            "شرکت‌های",
            "شرکتهای",
            "تکنیکال",
            "بنیادی",
            "فاندامنتال",
            "تک‌سهم",
            "تکسهم",
            "بازدهی",
            "بازده",
            "سود",
            "ضرر",
            "نوسان",
            "مقاومت",
            "مقاومتی",
            "حمایتی",
            "سقف",
            "کف",
            "کف‌سازی",
            "کفسازی",
            "صف",
            "مثبت",
            "منفی",
            "واچ‌لیست",
        ]
        self.emoj = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002500-\U00002BEF"  # chinese char
        u"\U00002702-\U000027B0"
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U00010000-\U0010ffff"
        u"\u2640-\u2642" 
        u"\u2600-\u2B55"
        u"\u200d"
        u"\u23cf"
        u"\u23e9"
        u"\u231a"
        u"\ufe0f"  # dingbats
        u"\u3030"
                      "]+", re.UNICODE)
        
    def get_symbols(self, text):
        symbols = []
        words = text.split()
        for symbol in self.symbols:
            
            if len(symbol.split()) == 1:
                
                if symbol in words and self.symbols_dict[symbol]["is_certain"]=="1":
                   symbols.append(symbol)
                
                elif "#" + symbol in words and self.symbols_dict[symbol]["is_certain"]=="1":
                   symbols.append(symbol)
                
                elif "#" + symbol in words and self.symbols_dict[symbol]["is_certain_with_rules"]=="1"\
                or self.symbols_dict[symbol]["is_certain_with_rules"]=="":
                    if "#" + symbol in words:
                        symbol_index = words.index("#" + symbol)
                        # print("#:" + symbol + str(words) +"\n" + str(symbol_index))
                        start =\
                            symbol_index-2 if symbol_index-2>=0\
                            else symbol_index-1 if symbol_index-1>=0\
                            else 0
                        end =\
                            len(words) if symbol_index==len(words)-1\
                            else symbol_index+2 if symbol_index==len(words)-2\
                            else symbol_index+3
                        # print("start#: ", start)
                        # print("end#: ", end)
                        suspect_words = words[start:end]
                        for flag_word in self.flag_words:
                            if "#" + flag_word in suspect_words and suspect_words.index(flag_word)>=0:
                                # print("#SUSPECT text: ", text)
                                # print("#SUSPECT symbol: ", "#" + symbol)
                                # print("#SUSPECT WORD: ", flag_word)
                                symbols.append(symbol)
                
                elif symbol in words and self.symbols_dict[symbol]["is_certain_with_rules"]=="1"\
                or self.symbols_dict[symbol]["is_certain_with_rules"]=="":
                    
                    if symbol in words:
                        symbol_index = words.index(symbol)
                        # print(symbol + str(words) +"\n" + str(symbol_index))
                        start =\
                            symbol_index-2 if symbol_index-2>=0\
                            else symbol_index-1 if symbol_index-1>=0\
                            else 0
                        end =\
                            len(words) if symbol_index==len(words)-1\
                            else symbol_index+2 if symbol_index==len(words)-2\
                            else symbol_index+3
                        # print("start: ", start)
                        # print("end: ", end)
                        suspect_words = words[start:end]
                        for flag_word in self.flag_words:
                            if flag_word in suspect_words and suspect_words.index(flag_word)>=0:
                                # print("SUSPECT text: ", text)
                                # print("SUSPECT symbol: ", symbol)
                                # print("SUSPECT WORD: ", flag_word)
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
                        temp['post_id'] = messages[i].id
                        temp['channel_id'] = messages[i].peer_id.channel_id
                        temp['channel_name'] = channel_name
                        temp['datetime'] = messages[i].date
                        temp['views'] = messages[i].views
                        temp['message'] = re.sub(self.emoj, '', normalizer.normalize(messages[i].message))
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
                    temp['message'] = re.sub(self.emoj, '', normalizer.normalize(messages[i].message))
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
                    temp['message'] = re.sub(self.emoj, '', normalizer.normalize(message.message))
                    temp['symbols'] = self.get_symbols(temp['message'])
                    temp['sentiment'] = self.get_sentiment(temp['message'])
                    res.append(temp)
                else:
                    break
            return res

if __name__ == "__main__":
    pass