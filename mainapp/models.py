# coding: utf-8
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.schema import FetchedValue
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class BalanceFinancing(Base):
    __tablename__ = 'balance_financing'

    id = Column(Integer, primary_key=True)
    balance_rate = Column(Float)


class BandCard(Base):
    __tablename__ = 'band_card'

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('user.id'), index=True)
    id_card = Column(String(20))
    card_type = Column(String(50))
    bank_name = Column(String(256))
    logo_href = Column(String(50))

    user = relationship('User', primaryjoin='BandCard.user_id == User.id', backref='band_cards')


class BankProduct(Base):
    __tablename__ = 'bank_product'

    id = Column(Integer, primary_key=True)
    fund_name = Column(String(256))
    return_rate1 = Column(Float)
    return_rate3 = Column(Float)
    return_rate6 = Column(Float)
    return_rate_year = Column(Float)
    all_return_rate = Column(Float)
    fund_detail = Column(Text)


class ChatRecord(Base):
    __tablename__ = 'chat_record'

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('user.id'), index=True)
    chat_time = Column(String(50))
    chat_log = Column(Text)

    user = relationship('User', primaryjoin='ChatRecord.user_id == User.id', backref='chat_records')


class Future(Base):
    __tablename__ = 'futures'

    id = Column(Integer, primary_key=True)
    bank_name = Column(String(20))


class HomePage(Base):
    __tablename__ = 'home_page'

    id = Column(Integer, primary_key=True)
    name = Column(String(20))
    pic = Column(String(256))


class Information(Base):
    __tablename__ = 'information'

    id = Column(Integer, primary_key=True)
    information_name = Column(String(256))
    release_time = Column(String(20))
    read_count = Column(Integer)
    image_url = Column(String(256))
    abstract = Column(String(256))
    info_class = Column(String(20))
    detail = Column(Text)


class OptionScore(Base):
    __tablename__ = 'option_score'

    id = Column(Integer, primary_key=True)
    name = Column(String(1))
    score = Column(Integer)


class ProductClas(Base):
    __tablename__ = 'product_class'

    id = Column(Integer, primary_key=True)
    bank_id = Column(ForeignKey('futures.id'), index=True)
    trade = Column(Integer)
    product_name = Column(String(256), unique=True)
    id_saling = Column(Integer)
    rate = Column(Float)
    pro_balance = Column(Float)
    produce = Column(Text)
    is_novice = Column(Integer)
    risk_level = Column(String(20))
    paid_count = Column(Integer)

    bank = relationship('Future', primaryjoin='ProductClas.bank_id == Future.id', backref='product_class')


class Question(Base):
    __tablename__ = 'question'

    id = Column(Integer, primary_key=True)
    Q_name = Column(Text)
    answer = Column(Text)


class ReadLog(Base):
    __tablename__ = 'read_log'

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('user.id'), index=True)
    read_date = Column(DateTime, nullable=False, server_default=FetchedValue())
    info_id = Column(ForeignKey('information.id'), index=True)

    info = relationship('Information', primaryjoin='ReadLog.info_id == Information.id', backref='read_logs')
    user = relationship('User', primaryjoin='ReadLog.user_id == User.id', backref='read_logs')


class RechargeLog(Base):
    __tablename__ = 'recharge_log'

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('user.id'), unique=True)
    recharge_phone_num = Column(String(11))
    recharge_money = Column(Integer)

    user = relationship('User', primaryjoin='RechargeLog.user_id == User.id', backref='recharge_logs')


class RiskLevel(Base):
    __tablename__ = 'risk_level'

    id = Column(Integer, primary_key=True)
    f_level = Column(String(10))
    user_vount = Column(Integer)


class SysUser(Base):
    __tablename__ = 'sys_user'

    id = Column(Integer, primary_key=True)
    username = Column(String(20))
    password = Column(String(12))
    sys_identity = Column(String(20))
    phone_num = Column(String(11))


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    phone_num = Column(String(11))
    password = Column(String(256))
    invited_user_id = Column(Integer)


class UserAccount(Base):
    __tablename__ = 'user_account'

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('user.id'), unique=True)
    user_balance = Column(Float)
    pay_password = Column(String(256))
    pay_count = Column(Integer)

    user = relationship('User', primaryjoin='UserAccount.user_id == User.id', backref='user_accounts')


class UserBalanceFinance(Base):
    __tablename__ = 'user_balance_finance'

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('user.id'), unique=True)
    paid_money = Column(Float)
    income = Column(Float, nullable=False, server_default=FetchedValue())
    paid_date = Column(Float, nullable=False)

    user = relationship('User', primaryjoin='UserBalanceFinance.user_id == User.id', backref='user_balance_finances')


class UserDitail(Base):
    __tablename__ = 'user_ditail'

    id = Column(Integer, primary_key=True)
    username = Column(String(20))
    portrait = Column(String(256))
    address = Column(String(256))
    identity_status = Column(Integer)
    risk_rank = Column(String(20))
    phone_num = Column(String(11))
    user_id = Column(ForeignKey('user.id'), index=True)

    user = relationship('User', primaryjoin='UserDitail.user_id == User.id', backref='user_ditails')


class UserProduct(Base):
    __tablename__ = 'user_product'

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('user.id'), unique=True)
    product_name = Column(String(128))
    Purchased = Column(Float)
    pay_date = Column(DateTime, nullable=False, server_default=FetchedValue())
    dead_line = Column(DateTime, nullable=False)

    user = relationship('User', primaryjoin='UserProduct.user_id == User.id', backref='user_products')


class UserTradeDetail(Base):
    __tablename__ = 'user_trade_detail'

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('user.id'), unique=True)
    behavior = Column(String(20))
    trade_money = Column(Float)
    trade_time = Column(DateTime, nullable=False, server_default=FetchedValue())

    user = relationship('User', primaryjoin='UserTradeDetail.user_id == User.id', backref='user_trade_details')


class UserVipPackage(Base):
    __tablename__ = 'user_vip_package'

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('user.id'), unique=True)
    vip_name = Column(String(20))
    expires_time = Column(DateTime)
    receive_date = Column(DateTime, nullable=False, server_default=FetchedValue())
    is_expires = Column(Integer)

    user = relationship('User', primaryjoin='UserVipPackage.user_id == User.id', backref='user_vip_packages')


class VersionDetail(Base):
    __tablename__ = 'version_detail'

    id = Column(Integer, primary_key=True)
    QR_code = Column(Text)
    version_id = Column(String(20))


class VipActivity(Base):
    __tablename__ = 'vip_activity'

    id = Column(Integer, primary_key=True)
    vip_name = Column(String(20))
    vip_count = Column(Integer)
    worth = Column(Integer)
    valid_time = Column(String(20))
