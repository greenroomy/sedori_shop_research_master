import models.research
import models.amazon
import models.mysqlconnector
import models.keepa
import models.spreadsheet


def amazon_research():
    research = models.research.Research()
    jan_list = research.get_jan_list()
    asin_dict = research.get_asin(jan_list)
    asin_list = list(asin_dict.values())
    result = research.get_price(asin_dict)
    research.bulk_update_db('lowest_price', result[0])
    research.bulk_update_db('curt', result[1])
    amazon = models.amazon.Amazon()
    spapi = models.amazon.SpApiMethod()
    amazon_url_dict = amazon.make_amazon_url(asin_list)
    # reseach.get_priceで取得したASINとlowest_priceから手数料を取得
    fba_fee_asin_dict = spapi.get_fba_fees(result[0])
    research.bulk_update_db('fba_fee', fba_fee_asin_dict)
    research.bulk_update_db('amazon_url', amazon_url_dict)
    keepa = models.keepa.MyKeepa()
    keepa_graph_url = keepa.get_graph_image(asin_list)
    research.bulk_update_db('keepa_graph', keepa_graph_url)


def calc_proccess(parameters):
    sqlcon = models.mysqlconnector.MySqlConnector()
    # shop_tableとprice_tableを結合
    merge_dict = sqlcon.bind_table()
    roi = models.research.Roi(parameters)
    roi.get_roi(merge_dict)


def sql_to_ss():
    # テーブルからCSVへエクスポート
    sqlcon = models.mysqlconnector.MySqlConnector()
    csv_file = sqlcon.export_to_csv()
    # CSVからSSへ書き込み
    ss = models.spreadsheet.MyGoogleSpreadSheet()
    ss.write_ss(csv_file)


# 上記のcsvではなくdataframeで処理するメソッド
def df_to_ss():
    # テーブルからDFへエクスポート
    sqlcon = models.mysqlconnector.MySqlConnector()
    df = sqlcon.export_to_df()
    # CSVからSSへ書き込み
    ss = models.spreadsheet.MyGoogleSpreadSheet()
    ss.write_df(df)


