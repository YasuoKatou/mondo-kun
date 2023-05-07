import MeCab

class Morphological:
    _wakati = None
    def __init__(self):
        self._wakati = MeCab.Tagger("-Owakati")


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

    def point(self, db, q_data):
        dbw = db.split(',')
        qc = 0
        qn = 0
        for qw in q_data.split(','):
            qn += 1
            qc += 1 if qw in dbw else 0
        return 0 if qn == 0 else qc / qn
#[EOF]