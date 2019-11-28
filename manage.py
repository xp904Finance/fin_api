from flask_cors import CORS

from mainapp import app
from mainapp.views import info_api, features_api, phone_payment_api, user_banlance_api, login_api, icon_api, my_account, \
    account_money_api, product_api, risk_level_api, portrait_api, user_vip_api


def make_app():
    app.register_blueprint(info_api.info_blue, url_prefix='/info')
    app.register_blueprint(features_api.features_tools, url_prefix="/bank")
    app.register_blueprint(login_api.user_blue, url_prefix='/user')
    app.register_blueprint(icon_api.ico, url_prefix='/ico')
    app.register_blueprint(my_account.acc_blue, url_prefix="/account")
    app.register_blueprint(product_api.product_info, url_prefix='/products')
    app.register_blueprint(risk_level_api.risk_level, url_prefix='/question')
    app.register_blueprint(portrait_api.portrait_blue, url_prefix='/portrait')
    app.register_blueprint(user_vip_api.user_vip_blue, url_prefix="/uservip")
    app.register_blueprint(account_money_api.account_blue, url_prefix="")
    app.register_blueprint(phone_payment_api.phone_payment_blue, url_prefix="")
    app.register_blueprint(user_banlance_api.balance_blue, url_prefix="")
    CORS(app)
    return app


application = make_app()
if __name__ == '__main__':
    application.run('0.0.0.0', 8080, debug=True)
