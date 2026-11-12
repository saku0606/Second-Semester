# SQLite
#  簡易RDB。
#  Android,macOS,Pythonでは
# デフォルトで組み込まれている。
import sqlite3
 
# DB接続
con = sqlite3.connect('0618_basic_db\\sample.db')
# sqliteはファイルでデータを管理する。
 
# このconnectionを用いて、
# DBを操作していく。
 
# DB操作用のオブジェクト(カーソル)を取得
cur = con.cursor()
 
# SQL文作成
sql = '''\
CREATE TABLE IF NOT EXISTS user(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name STRING
)\
'''
 
# SQL実行はexecute
cur.execute(sql)
 
# commitで確定
con.commit()
 
# DB切断
con.close()
 
# DB接続　※with構文で自動close
with sqlite3.connect('0618_basic_db\\sample.db') as con:
    # DB操作用のオブジェクト(カーソル)を取得
    cur = con.cursor()
 
    # SQL文作成
    sql = "INSERT INTO user(name) VALUES('a')"
 
    # SQL実行はexecute
    cur.execute(sql)
 
    # commitで確定
    # con.commit()
 
    # rollbackでキャンセル
    con.rollback()
 
    # データ取得(SELECT)は、
    # execute後、curで結果を取得する。
    cur.execute('SELECT * FROM user')
    for row in cur:
        print(row)
    # SELECTはcommit/rollback不要
 
    # 6/22 ここから
 
    # 単一行を取得するにはfetchone
    # 戻り値はタプル。
    # COUNT(*)等、スカラー(単一)値の場合には、
    # 1要素のタプル。
    cur.execute('SELECT * FROM user WHERE id=2')
    row = cur.fetchone()
    print(row)
 
    cur.execute('SELECT COUNT(*) FROM user')
    count, = cur.fetchone()
    print(count)
 
    # update
    cur.execute("UPDATE user SET name='b' WHERE id=1")
    con.commit()
 
    # delete
    cur.execute("DELETE from user WHERE id=2")
    con.commit()
 