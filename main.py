from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import tkinter as tk

from views.gui import Application
import control.controller
import models.mysqlconnector


def main():
    # url = 'https://store.shopping.yahoo.co.jp/y-lohaco/search.html?p=&X=4#CentSrchFilter1'
    # maxpage = 2
    sqlcon = models.mysqlconnector.MySqlConnector()
    sqlcon.initialize_table()
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()
    settings = get_project_settings()
    process = CrawlerProcess(settings)
    process.crawl('shop_scrapy_spider', url=app.url_value, maxpage=app.max_page_value)
    process.start()
    parameters = [
        app.base_times_value,
        app.add_times_value,
        app.coupon_price_value,
        app.coupon_percent_value,
        app.roi_extract,
        app.price_extract
    ]
    print('parameters', parameters)
    control.controller.amazon_research()
    control.controller.calc_proccess(parameters)
    # control.controller.sql_to_ss()
    control.controller.df_to_ss()


if __name__ == '__main__':
    main()
