import models.amazon
import models.mysqlconnector


class Research(object):
    def __init__(self):
        self.amazon = models.amazon.Amazon()
        self.spapimethod = models.amazon.SpApiMethod()
        self.sqlcon = models.mysqlconnector.MySqlConnector()

    def get_jan_list(self):
        sql = 'SELECT jan FROM shop_table'
        jan_dict = self.sqlcon.fetch(sql)
        jan_list = [x for row in jan_dict for x in row.values()]
        # jan_list = []
        # for row in jan_dict:
        #     for jan in row.values():
        #         jan_list.append(jan)
        return jan_list

    def get_asin(self, jan_list):
        get_asin_dict = {}
        for jan in jan_list:
            if jan:
                asin = self.spapimethod.jan2asin(jan)
                get_asin_dict.update(asin)
                print('JAN:', jan)
            else:
                asin = {None: None}
                get_asin_dict.update(asin)
                # JANがなければNoneを入れる
                jan = None
            # 取得したJanとASINをDBへ保存
            # self.insert_db(jan, asin[jan])
            sql = 'INSERT INTO price_table (jan, asin) VALUES (%s, %s)'
            value = (jan, asin[jan])
            self.sqlcon.insert(sql, value)

        print('get_asin_dictの要素数: ' + str(len(get_asin_dict)))
        print('get_asin_listの内容\n' + str(get_asin_dict))
        return get_asin_dict

    def get_price(self, asin_dict):
        # asin_dictからASINのリストを作成
        asin_list = list(asin_dict.values())
        # リストからNoneを削除
        filtered_asin_list = [e for e in asin_list if e is not None]
        print('asin_listからNoneを削除したリスト数は' + str(len(filtered_asin_list)))
        print('Noneを削除したリスト')
        print(filtered_asin_list)
        # リストを20個づつに分割
        full_lowest_prices = {}
        full_by_box = {}
        for i in range(0, len(filtered_asin_list), 20):
            result = self.spapimethod.get_lowest_prices_batch(filtered_asin_list[i: i+20])
            full_lowest_prices.update(result[0])
            full_by_box.update(result[1])
        print('full_lowest_prices')
        print(full_lowest_prices)
        print('full_buy_box')
        print(full_by_box)
        return full_lowest_prices, full_by_box
        # self.update_db(full_lowest_prices)

    def insert_db(self, jan, asin):
        db = self.operation.get_database()
        cursor = db.cursor()
        cursor.execute('USE shop_db')
        cursor.execute(
            'INSERT INTO price_table (jan, asin) VALUES (%s, %s)', (jan, asin)
        )
        db.commit()

    def bulk_update_db(self, set_key, di):
        for k, v in di.items():
            if v is None:
                pass
            elif isinstance(v, (int, float)):
                sql = '''
                UPDATE price_table SET {} = {} WHERE asin='{}' LIMIT 1
                '''.format(set_key, v, k)
                self.sqlcon.update(sql)
            else:
                sql = '''
                UPDATE price_table SET {} = '{}' WHERE asin='{}' LIMIT 1
                '''.format(set_key, v, k)
                self.sqlcon.update(sql)


class Roi(Research):
    def __init__(self, parameters):
        super().__init__()
        self.base_times = parameters[0]
        self.add_times = parameters[1]
        self.coupon_price = parameters[2]
        self.coupon_percent = parameters[3]
        self.commission = parameters[4]
        self.shipment = parameters[5]

    def get_roi(self, merge_dict):
        for row in merge_dict:
            price = row['price']
            lowest_price = row['lowest_price']
            jan = row['jan']
            fba_fee = row['fba_fee']
            if price is not None and lowest_price is not None and fba_fee is not None:
                roi_list = self.calc_roi(price, lowest_price, fba_fee)
                sql = '''UPDATE price_table SET roi={},unit_cost={},profit={} WHERE jan='{}' LIMIT 1'''\
                    .format(roi_list[0], roi_list[1], roi_list[2], jan)
                self.sqlcon.update(sql)
                print('ROI', roi_list)

    def calc_roi(self, price, lowest_price, fba_fee):
        tax_excluded_price = (price-self.coupon_price)*(1-self.coupon_percent/100)/1.1
        unit_cost = ((tax_excluded_price*(1-self.base_times/100))*(1-self.add_times/100))*1.1
        # estimate_commission = (lowest_price*(self.commission/100))*1.1
        # profit = lowest_price - unit_cost - estimate_commission - self.shipment
        profit = lowest_price - unit_cost - fba_fee
        roi = (profit/lowest_price)*100
        return roi, unit_cost, profit












