import pathlib
from trainer import Trainer
import requests
from bs4 import BeautifulSoup

class Geography(Trainer):

    _OUT_FILE = 'geography.yml'

    def __init__(self):
        p = self.outFile(self._OUT_FILE)
        if p.exists():
            p.unlink()
            print('[{}]を削除しました.'.format(self._OUT_FILE))

    _JP_PREF = {
        '北海道':'札幌',
        '青森':'', '岩手':'盛岡', '宮城':'仙台', '秋田':'', '山形':'', '福島':'',
        '茨城':'水戸', '栃木':'宇都宮', '群馬':'前橋','埼玉':'さいたま', '千葉':'', '東京都':'新宿区', '神奈川':'横浜',
        '新潟':'', '富山':'', '石川':'金沢', '福井':'', '山梨':'甲府', '長野':'', '岐阜':'', '静岡':'', '愛知':'名古屋',
        '三重':'津', '滋賀':'大津', '京都':'', '大阪':'', '兵庫':'神戸', '奈良':'', '和歌山':'',
        '鳥取':'', '島根':'松江', '岡山':'', '広島':'', '山口':'', '徳島':'', '香川':'高松', '愛媛':'松山', '高知':'',
        '福岡':'', '佐賀':'', '長崎':'', '熊本':'', '大分':'', '宮崎':'', '鹿児島':'', '沖縄':'那覇',
    }

    def add_jp_pref(self, categories=[]):
        l = []
        for p, c in self._JP_PREF.items():
            c_sufix = '市'
            if p == '東京都':
                p_sufix = ''
                c_sufix = ''
            elif p == '北海道':
                p_sufix = ''
            elif p == '大阪' or p == '京都':
                p_sufix = '府'
            else:
                p_sufix = '県'
            l.append([
                '{}{}の県庁所在地は？'.format(p, p_sufix),
                '{}{}です。'.format(c if c else p, c_sufix)])
        self.append_yml(self._OUT_FILE, l, categories)
        print('{}都道府県の県庁所在地を追加'.format(len(l)))

    _JP_7AREA = {
        '北海道': ['北海道'],
        '東北': ['青森県', '岩手県', '秋田県', '宮城県', '山形県', '福島県'],
        '関東': ['茨城県', '栃木県', '群馬県', '埼玉県', '千葉県', '東京都', '神奈川県'],
        '中部': ['新潟県', '富山県', '石川県', '福井県', '山梨県', '長野県', '岐阜県', '静岡県', '愛知県'],
        '近畿': ['三重県', '滋賀県', '京都府', '大阪府', '兵庫県', '奈良県', '和歌山県'],
        '中国四国': ['鳥取県', '島根県', '岡山県', '広島県', '山口県', '徳島県', '香川県', '愛媛県', '高知県'],
        '九州沖縄': ['福岡県', '佐賀県', '長崎県', '熊本県', '大分県', '宮崎県', '鹿児島県', '沖縄県']
    }

    def add_jp_7group(self, categories=[]):
        l = []
        for an, ps in self._JP_7AREA.items():
            #print('\t{}地方 : {}'.format(an, ','.join(ps)))
            l.append([
                '{}地方は？'.format(an),
                '{}です。'.format(' '.join(ps))])
        self.append_yml(self._OUT_FILE, l, categories)
        print('{}地方を追加'.format(len(l)))

    _SOURCE_HTML = './_geography_source.html'
    def make_source_html(self, url):
        html = requests.get(url)
        soup = BeautifulSoup(html.content, "html.parser")
        p = pathlib.Path(self._SOURCE_HTML)
        p.write_text(str(soup))

    def make_geography_02(self, categories=[]):
        p = pathlib.Path(self._SOURCE_HTML)
        s = p.read_text()
        soup = BeautifulSoup(s, "html.parser")
        l = []
        tn = 0
        for t in soup.find_all('table'):
            tn += 1
            if tn == 1:     # 地域のインデックス
                continue
            #print(t)
            for e in t.contents:
                if e.name != 'tr':
                    continue
                cl = 0
                n1 = ''
                n2 = ''
                th = False
                for td in e.contents:
                    if td.name != 'td':
                        continue
                    cl += 1
                    if cl == 1 and td.text == '国名':
                        th = True
                        break
                    if cl == 1:
                        n1 = td.text.strip()
                    elif cl == 2:
                        n2 = td.text.strip()
                if th:
                    continue
                #wk = n1.split(' ')
                #if len(wk) > 1:
                #    n1 = wk[-1]
                #print('\t{} : {}'.format(n1, n2))
                l.append([
                    '{}の首都は？'.format(n1),
                    '{}です。'.format(n2)])
        self.append_yml(self._OUT_FILE, l, categories)
        print('{}国と首都を追加'.format(len(l)))

if __name__ == '__main__':
    # 地理データを作成
    geography = Geography()
    # 47都道府県
    geography.add_jp_pref(['地理'])
    # ７分割地方の都道府県
    geography.add_jp_7group()
    # 世界の首都を追加
    #_DATA_URL02 = 'https://sekaichizu.net/book/world.html'
    #geography.make_source_html(_DATA_URL02)
    geography.make_geography_02()
#[EOF]