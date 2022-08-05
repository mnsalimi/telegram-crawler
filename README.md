# telegram-cralwer

Telegram channel crawling using Telethon, Django and Elastic Search.

# Requirements
<ol>
<li> python3.8 </li> 
<li> python3.8 -m pip install -r requirements.txt </li>
</ol>

# Usage
`python 3.8 manage.py makemigrations crawler` 
<br>
`python 3.8 manage.py migrate`
<br>
`python 3.8 manage.py runserver`

Telegram channel posts are crawled every 60 minutes after running server and enable celery.
To display posts browse http://127.0.0.1:8000/crawler on your browser.
You can change default channel to crawling in crawler/telegram_cralwer.py

<h5> Author: Moein Salimi </h5>