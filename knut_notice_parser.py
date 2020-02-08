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
def getBoardInfo():
    searchBBS_query = 'select title, bbs_id from knut_bbs where category =  \'%s\' or category = \'%s\';' % ('공지사항', '학사정보')
    cur.execute(searchBBS_query)
    searchBBS_result = cur.fetchall()
    return searchBBS_result

def getArticle(article_title):
    search_query = 'select count(title) from knut_article where title = \'%s\';' % article_title
    cur.execute(search_query)

    result = cur.fetchone()[0]
    if result:
        return False
    else:
        return True

def getNotice():
    board = getBoardInfo()
    for (bbs_title, bbs_id) in board:
        link = 'https://www.ut.ac.kr/cop/bbs/BBSMSTR_' + bbs_id + '/selectBoardList.do'

        # URL 접근
        req = requests.get(link)
        req.encoding = 'utf-8'

        # 게시판 첫 페이지 게시글 제목, 게시글 고유 번호 크롤링
        html = req.text
        soup = BeautifulSoup(html, 'html.parser')
        notices = soup.select('td.left > div > div > form > input[type=submit]')
        nttId = soup.select('td.left > div > div > form > input[type=hidden]:nth-child(2)')

        for title, nid in zip(notices, nttId):
            article_title = title.get('value')
            article_id = nid.get('value')
            link = 'https://www.ut.ac.kr/cop/bbs/BBSMSTR_' + bbs_id + '/selectBoardArticle.do?nttId=' + article_id

            # 데이터베이스에 중복된 게시글이 없다면 데이터베이스에 저장 후 텔레그램 채널로 메시지 전송
            if getArticle(article_title):
                try:
                    insert_query = 'insert into knut_article values (default , %s,%s,%s,%s) ON CONFLICT(title) DO NOTHING;'
                    cur.execute(insert_query, (bbs_title, article_title, link, article_id))
                    conn.commit()
                    message = '[' + bbs_title + '] ' + article_title + '\n' + link
                    bot.sendMessage(chat_id=chat_id, text=message)
                except Exception as e:
                    print(e)

if __name__ == "__main__":
    getNotice()