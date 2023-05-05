from pathlib import Path

class Trainer:
    def __init__(self):
        pass

    def outFile(self, file_name):
        p = Path(__file__).parent.parent
        p = p / 'data' / file_name
        return p

    def append_yml(self, file_name, qa_list, categories):
        p = self.outFile(file_name)
        with p.open(mode='a', encoding='utf-8') as f:
            f.write('categories:\n')
            for category in categories:
                f.write('- {}\n'.format(category))
            f.write('conversations:\n')
            for items in qa_list:
                f.write('- - {}\n'.format(items[0]))
                f.write('  - {}\n'.format(items[1]))

if __name__ == '__main__':
    pass

#[EOF]