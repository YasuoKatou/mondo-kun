from pathlib import Path
import MeCab
import yaml
import psycopg2
from psycopg2.extras import DictCursor

class Training:
    _wakati = None
    def __init__(self):
        self._wakati = MeCab.Tagger("-Owakati")

    def getTrainningFiles(self):
        p = Path(__file__).parent.parent
        p = p / 'data'
        return p.glob('*.yml')

    _CHAR_TYPE_NOUN = [2, 8]     # 名詞
    def decideDbSearchKey(self, question):
        node = self._wakati.parseToNode(question)
        word = None
        hinsi = []
        nl = []
        while node:
            if node.char_type in self._CHAR_TYPE_NOUN:
                if node.surface != word:
                    nl.append(node.surface)
                wk = []
                c = 0
                for n in node.feature.split(','):
                    if c < 4:
                        if n != '*':
                            wk.append(n)
                    else:
                        break
                    c += 1
                if len(hinsi) < len(wk):
                    hinsi = wk
                    word = node.surface
            node = node.next
        assert word, 'check noun (source:{})'.format(question)
        return {
                'db-key': 'NOUN:{}'.format(word),
                'noun-list': ','.join(['NOUN:{}'.format(w) for w in nl])
            }

    _SQL_FIND_CATEGORY_ID = 'select id from categories where name = %s'
    _SQL_APPEND_CATEGORY  = 'insert into categories (name) values (%s) returning id'
    def appendCategory(self, cursor, name):
        '''
        カテゴリ名を追加する
        '''
        # 登録済みを確認
        cursor.execute(self._SQL_FIND_CATEGORY_ID, (name, ))
        r = cursor.fetchone()
        if r:
            return r['id']
        # 新規に追加
        r = cursor.execute(self._SQL_APPEND_CATEGORY, (name, ))
        r = cursor.fetchone()
        assert r, 'returning id error'
        return r['id']

    _SQL_DELETE_BY_CID = 'delete from q_and_a where category_id = %s'
    def clearCategory(self, cursor, cid):
        '''
        問答テーブルをカテゴリIDで削除する
        '''
        cursor.execute(self._SQL_DELETE_BY_CID, (cid, ))
        rc = cursor.rowcount
        print('delete count:{} (category id:{})'.format(rc, cid))

    _SQL_APPEND_QA = \
        'insert into q_and_a (category_id, question, answer, ' \
        'list_up_key, morphological) values (%s, %s, %s, %s, %s)'
    def appendQA(self, cursor, cid, row):
        cursor.execute(self._SQL_APPEND_QA,
            (cid, row['question'], row['answer'],
             row['list_up_key'], row['morphological'], ))
        return cursor.rowcount

    def saveToDb(self, trData):
        with psycopg2.connect(MONDO_DB['dsn']) as conn:
            cursor = conn.cursor(cursor_factory=DictCursor)
            for cn in trData['categories']:
                cid = self.appendCategory(cursor, cn)
                #print('category name:{}(id:{})'.format(cn, cid))
                self.clearCategory(cursor, cid)
                cnt = 0
                for row in trData['recs']:
                    cnt += self.appendQA(cursor, cid, row)
            cursor.close()
            print('category name:{}(id:{}, rows:{})'.format(cn, cid, cnt))

    def training(self):
        wakati = MeCab.Tagger("-Owakati")
        for training_file in self.getTrainningFiles():
            print(training_file)
            with training_file.open(mode='r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
            trData = {'categories': data['categories'], 'recs': []}
            for c in data['conversations']:
                r = self.decideDbSearchKey(c[0])
                trData['recs'].append({
                    'question': c[0],
                    'answer': c[1],
                    'list_up_key': r['db-key'],
                    'morphological': r['noun-list']
                })
                #print('Q:{}(DB:{}) => A:{}'.format(c[0], r['db-key'], c[1]))
                #print('\t{}'.format(r['noun-list']))

            self.saveToDb(trData)

if __name__ == '__main__':
    import os
    import sys

    sys.path.append(os.getcwd())
    from config.mondo_settings import MONDO_DB

    trainer = Training()
    trainer.training()

#[EOF]