import psycopg2
from psycopg2.extras import DictCursor

from utils.morphological import Morphological
from config.mondo_settings import MONDO_DB, MONDO_KUN

class Mondo:
    _morphological = None
    def __init__(self):
        self._morphological = Morphological()

    def getDefaultResponse(self):
        if 'default_response' in MONDO_KUN:
            s = MONDO_KUN['default_response']
            if type(s) is list:
                return ''.join(s)
            else:
                return str(s)
        return '見つかりません.'

    _SQL_GET_ANS_LIST = 'select answer, morphological from q_and_a where list_up_key = %s'
    def get_response(self, q_data):
        sk = self._morphological.decideDbSearchKey(q_data)
        ans = {'point': 0, 'string': None}
        with psycopg2.connect(MONDO_DB['dsn']) as conn:
            with conn.cursor(cursor_factory=DictCursor) as cur:
                cur.execute(self._SQL_GET_ANS_LIST, (sk['db-key'], ))
                for row in cur:
                    pt = self._morphological.point(row['morphological'], sk['noun-list'])
                    if ans['point'] < pt:
                        ans['point'] = pt
                        ans['string'] = row['answer']

        return ans['string'] if ans['string'] else self.getDefaultResponse()

if __name__ == '__main__':

    mondo = Mondo()

    while True:
        try:
            bot_input = mondo.get_response(input('input : '))
            print('response : [{}]'.format(bot_input))
        except(KeyboardInterrupt, EOFError, SystemExit):
            break

#[EOF]