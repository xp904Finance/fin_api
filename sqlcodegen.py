import os

print('-开始生成Models.py--')
os.system('flask-sqlacodegen --outfile mainapp/models.py  mysql+pymysql://root:123456@49.235.55.221:3339/finance_db')

if os.path.exists('mainapp/models.py'):
    print('---成功--')
else:
    print('--失败--')