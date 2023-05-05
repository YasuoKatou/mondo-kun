
def initDb():
    print(MONDO_DB)



if __name__ == '__main__':
    # プロジェクトのルートディレクトリを検索パスに追加する
    import sys
    import os
    sys.path.append(os.getcwd())
    from config.mondo_settings import MONDO_DB
    initDb()

#[EOF]