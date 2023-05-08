import MeCab

_wakati = MeCab.Tagger("-Owakati")

question = ['日本の首都は？',
            'アゼルバイジャンの首都は？',
           ]
for q in question:
    print('Q:{}'.format(q))
    node = _wakati.parseToNode(q)
    while node:
        print('\tchar_type:{}'.format(node.char_type))
        print('\tfeature:{}'.format(node.feature))
        node = node.next

#[EOF]