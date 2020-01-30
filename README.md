# knut-bot
[한국교통대학교](https://ut.ac.kr) 새 글 알림봇(텔레그램)  
[텔레그램 채널](https://t.me/knut_notice)

현재 지원하는 게시판
- 학사안내
- 일반소식
- 장학안내
- 행사안내

## Requirements
- Python3
- PostgreSQL
- secret.py
	```Python3
	TELEGRAM_TOKEN = 'Your Telegram Bot Token'
	TELEGRAM_CHAT_ID = 'Your Telegram Channel ID or Telegram ID to send notice message'
	
	DB_SETUP = "host='Your Database Server IP dbname='Your Database Name' user='Database User Id' password='Database User Password'"
	```

## Build
```
git clone https://github.com/github-id/knut-bot

cd knut-bot

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
```
❗ Command "python setup.py egg_info" failed with error code 1 in /tmp/pip-build-he14psys/psycopg2/


💡 sudo apt-get install postgresql python-psycopg2 libpq-dev
```

## Database
- PostgreSQL 11


### knut_bbs
| Column   | Type                   | Collation | Nullable | Default                                 |
|----------|------------------------|-----------|----------|-----------------------------------------|
| pk_id    | integer                |           | not null | nextval('knut_bbs_pk_id_seq'::regclass) |
| title    | character varying(100) |           | not null |                                         |
| category | character varying(100) |           |          |                                         |
| bbs_id   | character varying(200) |           | not null |                                         |
```SQL
create table knut_bbs (
	pk_id serial PRIMARY KEY,
	title varchar(100) UNIQUE not null,
	category varchar(100),
	bbs_id varchar(200) UNIQUE not null
);
```

### knut_article
| Column    | Type                   | Collation | Nullable | Default                                     |
|-----------|------------------------|-----------|----------|---------------------------------------------|
| pk_id     | integer                |           | not null | nextval('knut_article_pk_id_seq'::regclass) |
| bbs_title | character varying(100) |           |          |                                             |
| title     | character varying(300) |           | not null |                                             |
| link      | character varying(300) |           | not null |                                             |

```SQL
create table knut_article (
	pk_id serial PRIMARY KEY,
	bbs_title varchar(100) REFERENCES knut_bbs (title),
	title varchar(300) not null,
	link varchar(300) not null
);
```
