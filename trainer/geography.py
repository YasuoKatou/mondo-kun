import pathlib
from trainer import Trainer

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

    def add_jp_pref(self):
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
        self.append_yml(self._OUT_FILE, l, ['地理'])
        print('{}都道府県の県庁所在地を追加'.format(len(l)))

if __name__ == '__main__':
    geography = Geography()
    geography.add_jp_pref()

#[EOF]