import models.mysqlconnector


class ShopScrapyPipeline:
    # Pipelineにデータが渡される時に実行される
    # itemにspiderから渡されたitemがセットされる
    def process_item(self, item, spider):
        self.save_post(item)
        return item

    # itemをDBに保存する
    def save_post(self, item):
        sqlcon = models.mysqlconnector.MySqlConnector()
        values = (item['title'], item['price'], item['jan'], item['url'])
        sql = 'INSERT INTO shop_table (title, price, jan, url) VALUES (%s, %s, %s, %s)'
        sqlcon.insert(sql, values)
        sqlcon.close()


