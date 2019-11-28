from flask import Flask

from mainapp.views.product_api import product_info

app = Flask(__name__)
if __name__ == '__main__':
    app.register_blueprint(product_info,url_prefix='/products')

    app.run('0.0.0.0', 8080, debug=True)