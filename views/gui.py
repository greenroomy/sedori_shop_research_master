import tkinter as tk
import tkinter.ttk as ttk


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master.geometry('320x300')
        self.master.title('全頭リサーチ')
        # フレームの生成
        self.frame = tk.Frame(self.master, width=280, height=140, padx=10, pady=10)
        self.url_value = ''
        self.max_page_value = ''
        self.base_times_value = ''
        self.add_times_value = ''
        # self.commission_value = ''
        # self.shipment_value = ''
        self.coupon_price_value = ''
        self.coupon_percent_value = ''
        self.roi_extract = ''
        self.price_extract = ''
        self.create_widgets()

    def create_widgets(self):
        # ラベル、テキストボックス、ボタンの生成
        # 1行目
        tk.Label(self.frame, text='URL').grid(column=0, row=0)
        self.url = ttk.Entry(self.frame, width=22)
        self.url.grid(column=1, row=0, columnspan=3)
        # 2行目
        tk.Label(self.frame, text='Max page').grid(column=0, row=1)
        self.max_page = ttk.Entry(self.frame, width=4)
        self.max_page.insert(0, 15)
        self.max_page.grid(column=1, row=1)
        # 3行目
        tk.Label(self.frame, text='基礎倍率').grid(column=0, row=2)
        self.base_times = ttk.Entry(self.frame, width=4)
        self.base_times.insert(0, 10)
        self.base_times.grid(column=1, row=2)
        # 4行目
        tk.Label(self.frame, text='追加倍率').grid(column=0, row=3)
        self.add_times = ttk.Entry(self.frame, width=4)
        self.add_times.insert(0, 0)
        self.add_times.grid(column=1, row=3)
        # 5行目
        tk.Label(self.frame, text='クーポン(円)').grid(column=0, row=4)
        self.coupon_price = ttk.Entry(self.frame, width=4)
        self.coupon_price.insert(0, 0)
        self.coupon_price.grid(column=1, row=4)
        tk.Label(self.frame, text='円').grid(column=2, row=4, sticky=tk.W)
        # 6行目
        tk.Label(self.frame, text='クーポン(%)').grid(column=0, row=5)
        self.coupon_percent = ttk.Entry(self.frame, width=4)
        self.coupon_percent.insert(0, 0)
        self.coupon_percent.grid(column=1, row=5)
        tk.Label(self.frame, text='%').grid(column=2, row=5, sticky=tk.W)
        # # 7行目
        # tk.Label(self.frame, text='手数料').grid(column=0, row=6)
        # self.commission = ttk.Entry(self.frame, width=4)
        # self.commission.insert(0, 10)
        # self.commission.grid(column=1, row=6)
        # tk.Label(self.frame, text='%').grid(column=2, row=6, sticky=tk.W)
        # # 8行目
        # tk.Label(self.frame, text='配送料').grid(column=0, row=7)
        # self.shipment = ttk.Entry(self.frame, width=4)
        # self.shipment.insert(0, 500)
        # self.shipment.grid(column=1, row=7)
        # tk.Label(self.frame, text='円').grid(column=2, row=7, sticky=tk.W)
        #区切り線を設置
        style = ttk.Style()
        # style.configure("blue.TSeparator", background="blue")
        border = ttk.Separator(self.frame, orient="horizontal")
        border.grid(column=0, row=6, pady=5, sticky='ew')
        # 8行目
        tk.Label(self.frame, text='抽出条件').grid(column=0, row=7)
        # 9行目
        tk.Label(self.frame, text='ROI').grid(column=0, row=8)
        self.roi_extract = ttk.Entry(self.frame, width=4)
        self.roi_extract.insert(0, 5)
        self.roi_extract.grid(column=1, row=8)
        tk.Label(self.frame, text='%以上').grid(column=2, row=8, sticky=tk.W)
        # 10行目
        tk.Label(self.frame, text='価格').grid(column=0, row=9)
        self.price_extract = ttk.Entry(self.frame, width=4)
        self.price_extract.insert(0, 10)
        self.price_extract.grid(column=1, row=9)
        tk.Label(self.frame, text='円以上').grid(column=2, row=9, sticky=tk.W)
        # 9行目(実行ボタン)
        tk.Button(self.frame, text="実行", command=self.click_button).grid(column=3, row=10)
        # btn = tk.Button(self.frame, text="実行")
        # btn.grid(column=3, row=10)
        # btn.bind('<Return>', self.click_button)
        # フレームの配置
        self.frame.grid(column=0, row=0, sticky=tk.NSEW)

    # 実行ボタンクリック時
    def click_button(self):
        self.url_value = self.url.get()
        self.max_page_value = int(self.max_page.get())
        self.base_times_value = int(self.base_times.get())
        self.add_times_value = int(self.add_times.get())
        self.coupon_price_value = int(self.coupon_price.get())
        self.coupon_percent_value = int(self.coupon_percent.get())
        self.roi_extract = int(self.roi_extract.get())
        self.price_extract = int(self.price_extract.get())
        self.master.destroy()









