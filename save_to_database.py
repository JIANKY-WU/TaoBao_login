import pymysql

class Save_to_Mysql():
    def __init__(self):
        self.host='localhost'
        self.user='root'
        self.password='root'
        self.database='TaoBao'

    def save(self,item):
        connection=pymysql.connect(self.host,self.user,self.password,self.database)
        cursor=connection.cursor()
        sql='create table if not exists taobao(id int not null auto_increment,title varchar(120),price float,primary key (id))\
        default charset=utf8'
        cursor.execute(sql)
        sql='insert ignore into taobao (title,price,img_url) value("{0}","{1}","{2}")'.format(item["title"],item["price"],item['img_url'])
        cursor.execute(sql)
        connection.commit()
        connection.close()