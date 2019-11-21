from flask_cors import CORS

from mainapp import app
from mainapp.views import info_api

if __name__ == '__main__':
    app.register_blueprint(info_api.info_blue, url_prefix='/user')
    CORS(app)

    app.run('0.0.0.0', 8080, debug=True)
