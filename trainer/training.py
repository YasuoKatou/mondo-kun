from pathlib import Path
import MeCab
import yaml

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

    def training(self):
        wakati = MeCab.Tagger("-Owakati")
        for training_file in self.getTrainningFiles():
            print(training_file)
            with training_file.open(mode='r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
            #print(data)
            for c in data['conversations']:
                r = self.decideDbSearchKey(c[0])
                print('Q:{}(DB:{}) => A:{}'.format(c[0], r['db-key'], c[1]))
                print('\t{}'.format(r['noun-list']))

if __name__ == '__main__':
    trainer = Training()
    trainer.training()


#[EOF]