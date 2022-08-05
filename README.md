# telegram-cralwer

Telegram channel crawling using Telethon, Django and Elastic Search.

# Requirements
<li> python3.8 
<li> python3.8 -m pip install -r requirements.txt

# Usage
`python 3.8 manage.py makemigrations crawler`
`python 3.8 manage.py migrate`
`python 3.8 manage.py runserver`

Telegram channel posts are crawled every 60 minutes after running server and enable celery.
To display posts browse http://127.0.0.1:8000/crawler on your browser.
You can change default channel to crawling in crawler/telegram_cralwer.py

<h5> Author: Moein Salimi </h5>