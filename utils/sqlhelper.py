import pymysql

# Link Linux's Mysql
# host1 = '192.168.3.45'
# port1 = 3306
# user1 = 'mysite01'
# password1 = '3t3HEp4FGbFhm2PX'
# db1 = 'mysite01'

# Link Macos's Mysql
# host1 = '127.0.0.1'
# port1 = 3306
# user1 = 'root'
# password1 = 'root1234'
# db1 = 'db_mysite'

# Link Aliyun's Mysql
host1 = 'bdm721867649.my3w.com'
port1 = 3306
user1 = 'bdm721867649'
password1 = '33Gmy2100'
db1 = 'bdm721867649_db'


# 获取列表
def get_list(sql, args):
    conn = pymysql.connect(host=host1, port=port1, user=user1, passwd=password1, db=db1, charset='utf8')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute(sql, args)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result


# 获取一个
def get_one(sql, args):
    conn = pymysql.connect(host=host1, port=port1, user=user1, passwd=password1, db=db1, charset='utf8')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute(sql, args)
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result


# 添加
def add(sql, args):
    conn = pymysql.connect(host=host1, port=port1, user=user1, passwd=password1, db=db1, charset='utf8')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute(sql, args)
    conn.commit()
    cursor.close()
    conn.close()


# 修改
def modify(sql, args):
    conn = pymysql.connect(host=host1, port=port1, user=user1, passwd=password1, db=db1, charset='utf8')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute(sql, args)
    conn.commit()
    cursor.close()
    conn.close()


# 删除
def delete(sql, args):
    conn = pymysql.connect(host=host1, port=port1, user=user1, passwd=password1, db=db1, charset='utf8')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute(sql, args)
    conn.commit()
    cursor.close()
    conn.close()
