import psycopg2
import requests
from bs4 import BeautifulSoup
import telegram
import secret

bot = telegram.Bot(token=secret.TELEGRAM_TOKEN)
chat_id = secret.TELEGRAM_CHAT_ID

# Connect Database
conn_setup = secret.DB_SETUP
conn = psycopg2.connect(conn_setup)
cur = conn.cursor()

# get Board title, id
searchBBS_query = 'select title, bbs_id from knut_bbs;'
cur.execute(searchBBS_query)
searchBBS_result = cur.fetchall()

def latest_notice(bbs_title):
    latest_query = 'select title from knut_article where bbs_title = \'%s\' LIMIT 1;' % bbs_title
    cur.execute(latest_query)

    if cur.fetchall is not None:
        latest_result = cur.fetchall().pop()[0]
        return latest_result
    else:
        return None


for (bbs_title, bbs_id) in searchBBS_result:
    print(bbs_id + bbs_title)
    link = 'https://www.ut.ac.kr/cop/bbs/BBSMSTR_' + bbs_id + '/selectBoardList.do'

    # URL 접근
    req = requests.get(link)
    req.encoding = 'utf-8'

    # 게시글 제목, 게시글 고유 번호 크롤링
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')
    notices = soup.select('td.left > div > div > form > input[type=submit]')
    nttId = soup.select('td.left > div > div > form > input[type=hidden]:nth-child(2)')

    for title, nid in zip(notices, nttId):
        article_title = title.get('value')
        article_id = nid.get('value')
        link = 'https://www.ut.ac.kr/cop/bbs/BBSMSTR_' + bbs_id + '/selectBoardArticle.do?nttId=' + article_id

        # 가장 최근의 게시글을 가져옴
        latest_title = latest_notice(bbs_title)
        
        try:
            # 가장 최근 게시글과 같지 않다면 (= 새 글이라면)
            # 데이터베이스에 해당 게시글을 저장, 텔레그램 채널로 메시지 전송
            if title != latest_title:
                insert_query = 'insert into knut_article values (default , %s,%s,%s) ON CONFLICT(title) DO NOTHING;'
                cur.execute(insert_query, (bbs_title, article_title, link))
                conn.commit()
                message = '[' + bbs_title + '] ' + article_title + '\n' + link
                bot.sendMessage(chat_id=chat_id, text=message)
            else:
                continue
        except Exception as e:
            print(e)