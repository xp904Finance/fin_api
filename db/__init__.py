from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


_engine = create_engine("mysql+pymysql://root:123456@49.235.55.221:3339/finance_db")
_engine.connect()

# 基于engine生成数据库会话的Session类
_Session = sessionmaker(bind=_engine)

# 创建Session类实例对
session = _Session()