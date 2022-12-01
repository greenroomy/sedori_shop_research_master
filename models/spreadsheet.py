import csv
import datetime
import yaml

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from gspread_dataframe import set_with_dataframe
from gspread_formatting import *
from gspread_formatting.dataframe import format_with_dataframe, BasicFormatter


class MyGoogleSpreadSheet(object):
    def __init__(self):
        with open('./data/config.yaml', 'r') as yaml_file:
            config_data = yaml.safe_load(yaml_file)
        self.sheet_id = config_data['ss_config']['SHEET_ID']
        self.folder_id = config_data['ss_config']['FOLDER_ID']
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
        # サービスアカウントキーを読み込む
        json_keyfile_path = './data/pelagic-region-134805-4a53d343e113.json'
        self.credentials = ServiceAccountCredentials.from_json_keyfile_name(json_keyfile_path, scope)
        # pydrive用にOAuth認証を行う
        gauth = GoogleAuth()
        gauth.credentials = self.credentials
        self.drive = GoogleDrive(gauth)

    def write_ss(self, csv_file):
        # 現在時刻を取得(シート名用)
        dt_now = datetime.datetime.now()
        sheet_name = dt_now.strftime("%Y%m%d_%H%M%S")
        file = self.drive.CreateFile({
            'title': sheet_name,
            'mimeType': 'application/vnd.google-apps.spreadsheet',
            "parents": [{"id": self.folder_id}]
        })
        file.Upload()
        # gspread用に認証
        gc = gspread.authorize(self.credentials)
        # スプレッドシートのIDを指定してワークブックを選択
        workbook = gc.open_by_key(file['id'])
        workbook.values_update(
            range='Sheet1',
            params={'valueInputOption': 'USER_ENTERED'},
            body={'values': list(csv.reader(open(csv_file, encoding='utf_8_sig')))}
        )

    # 上記のCSV形式を書き込みのではなくdfを処理するメソッド
    def write_df(self, df):
        # 現在時刻を取得(シート名用)
        dt_now = datetime.datetime.now()
        sheet_name = dt_now.strftime("%Y%m%d_%H%M%S")
        file = self.drive.CreateFile({
            'title': sheet_name,
            'mimeType': 'application/vnd.google-apps.spreadsheet',
            "parents": [{"id": self.folder_id}]
        })
        file.Upload()
        # gspread用に認証
        gc = gspread.authorize(self.credentials)
        # スプレッドシートのIDを指定してワークブックを選択
        workbook = gc.open_by_key(file['id'])
        sheet = workbook.sheet1
        # デフォルトのセルフォーマットを定義
        formatter = BasicFormatter(
            header_background_color=Color(0.3, 0.5, 0.9),
            header_text_color=Color(1, 1, 1),
            decimal_format='#,##0.00',
            freeze_headers=True
        )
        format_with_dataframe(sheet, df, formatter, include_index=False, include_column_header=True)
        # dfをSSへ反映
        set_with_dataframe(sheet, df, include_index=False, allow_formulas=True)
        # 列を1列で固定
        # set_frozen(sheet, rows=1)
        # 列の高さと幅を設定
        set_row_height(sheet, '2:' + str(len(df)), 82)
        set_column_widths(sheet, [('A', 25), ('B', 250), ('C', 70), ('L', 110), ('N', 220)])
        # テキストを上下中央に配置
        cell_formatter_entire = CellFormat(
            verticalAlignment='MIDDLE'
        )
        # 上記フォーマットを設定
        format_cell_range(sheet, 'A2:N' + str(len(df)), cell_formatter_entire)
        # 左よせ
        cell_formatter_left = CellFormat(
            horizontalAlignment='LEFT'
        )
        # 上記フォーマットを設定(B列タイトル)
        format_cell_range(sheet, 'B2:B' + str(len(df)), cell_formatter_left)
        # 上記フォーマットを設定(M列Amazon)
        format_cell_range(sheet, 'M2:M' + str(len(df)), cell_formatter_left)
        # 上記フォーマットを設定(E列URL)
        format_cell_range(sheet, 'E2:E' + str(len(df)), cell_formatter_left)


