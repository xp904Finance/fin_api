from flask_cors import CORS

from mainapp import app
from mainapp.views import info_api,features_api

if __name__ == '__main__':
    app.register_blueprint(info_api.info_blue, url_prefix='/user')
    app.register_blueprint(features_api.features_tools, url_prefix="/bank")
    CORS(app)

    app.run('0.0.0.0', 8080, debug=True)
