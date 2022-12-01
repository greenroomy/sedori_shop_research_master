import mysql.connector
import sys
import pandas
import datetime
import csv


class MySqlConnector(object):
    def __init__(self):
        self.user = 'root'
        self.password = 'jpt01130'
        self.host = 'localhost'
        self.database = 'shop_db'

        try:
            self.connector = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            # コネクションの設定
            self.connector.ping(reconnect=True)
            self.connector.autocommit = False
            # カーソル情報をクラス変数に格納
            self.cursor = self.connector.cursor(dictionary=True)
        except mysql.connector.errors.ProgrammingError as e:
            print(e)
            sys.exit(1)

    def fetch(self, sql):
        try:
            self.cursor.execute(sql)
            rows = self.cursor.fetchall()
            return rows
        except mysql.connector.error as e:
            print(e)
            sys.exit(1)

    def insert(self, sql, value):
        try:
            self.cursor.execute(sql, value)
            self.connector.commit()
        except mysql.connector.errors.ProgrammingError as e:
            self.connector.rollback()
            print(e)
            sys.exit(1)

    def update(self, sql):
        try:
            self.cursor.execute(sql)
            self.connector.commit()
        except mysql.connector.errors.ProgrammingError as e:
            self.connector.rollback()
            print(e)
            sys.exit(1)

    def delete(self, sql):
        try:
            self.cursor.execute(sql)
            self.connector.commit()
        except mysql.connector.errors.ProgrammingError as e:
            self.connector.rollback()
            print(e)
            sys.exit(1)

    def close(self):
        self.cursor.close()
        self.connector.close()

    def initialize_table(self):
        self.cursor.execute(
            '''
            DROP TABLE IF EXISTS shop_table, price_table
            '''
        )
        self.cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS shop_table(
            id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            price INT,
            jan VARCHAR(32),
            url VARCHAR(255) NOT NULL);
            '''
        )
        self.cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS price_table(
                id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
                jan VARCHAR(32),
                asin VARCHAR(255),
                lowest_price INT,
                roi FLOAT,
                unit_cost FLOAT,
                profit FLOAT,
                fba_fee FLOAT,
                curt VARCHAR(32),
                amazon_url VARCHAR(255),
                keepa_graph VARCHAR(255));
            '''
        )
        self.cursor.close()

    def bind_table(self):
        sql = '''
                SELECT 
                    shop_table.id,
                    shop_table.title,
                    shop_table.price,
                    shop_table.jan,
                    shop_table.url,
                    price_table.asin,
                    price_table.lowest_price,
                    price_table.fba_fee,
                    price_table.curt,
                    price_table.amazon_url,
                    price_table.keepa_graph
                FROM
                    shop_table
                LEFT OUTER JOIN
                    price_table
                ON
                    shop_table.jan=price_table.jan
                '''
        self.cursor.execute(sql)
        merge_dict = self.cursor.fetchall()
        print('merge_list')
        print(merge_dict)
        return merge_dict

    def export_to_csv(self):
        sql = '''
                SELECT 
                    shop_table.id,
                    shop_table.title,
                    shop_table.price,
                    shop_table.jan,
                    shop_table.url,
                    price_table.asin,
                    price_table.lowest_price,
                    price_table.roi,
                    price_table.unit_cost,
                    price_table.profit,
                    price_table.fba_fee,
                    price_table.curt,
                    price_table.amazon_url,
                    price_table.keepa_graph
                FROM
                    shop_table
                LEFT OUTER JOIN
                    price_table
                ON
                    shop_table.jan=price_table.jan
                '''
        df = pandas.read_sql(sql, self.connector)
        dt_now = datetime.datetime.now()
        file_path_name = 'result/' + dt_now.strftime("%Y%m%d_%H%M%S") + '.csv'
        df.to_csv(file_path_name, header=True, index=False, quoting=csv.QUOTE_NONE, escapechar='\\')
        return file_path_name

    # 上記のCSVではなくdataframeを返すメソッド
    def export_to_df(self):
        sql = '''
                SELECT 
                    shop_table.id,
                    shop_table.title,
                    shop_table.price,
                    shop_table.jan,
                    shop_table.url,
                    price_table.asin,
                    price_table.lowest_price,
                    price_table.roi,
                    price_table.unit_cost,
                    price_table.profit,
                    price_table.fba_fee,
                    price_table.curt,
                    price_table.amazon_url,
                    price_table.keepa_graph
                FROM
                    shop_table
                LEFT OUTER JOIN
                    price_table
                ON
                    shop_table.jan=price_table.jan
                '''
        df = pandas.read_sql(sql, self.connector)
        # dt_now = datetime.datetime.now()
        # file_path_name = 'result/' + dt_now.strftime("%Y%m%d_%H%M%S") + '.csv'
        # df.to_csv(file_path_name, header=True, index=False, quoting=csv.QUOTE_NONE, escapechar='\\')
        return df




