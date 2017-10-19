import sqlite3
from bs4 import BeautifulSoup


def main():
    cx = sqlite3.connect('../bilbili.db')
    cu = cx.cursor()
    cu.execute('create table rooms (id integer primary key AUTOINCREMENT, url integer, name nvarchar(15))')
    cx.commit()

    f = open('rank.html', 'r', encoding="utf-8")
    html = f.read()
    soup = BeautifulSoup(html, 'html.parser')
    trs = soup.find_all('tr')
    for tr in trs:
        url = int(tr.a['href'][1:])
        uper = tr.a.span.get_text()
        cu.execute('create table tt%s (id integer primary key AUTOINCREMENT, name nvarchar(15), comment text, time integer)' % url)
        cu.execute('create table ss%s (id integer primary key AUTOINCREMENT, number integer, time integer)' % url)
        cu.execute("insert into rooms (url, name) values (%s, '%s')" % (url, uper))
    cx.commit()

    cu.close()
    cx.close()

if __name__ == '__main__':
    main()
