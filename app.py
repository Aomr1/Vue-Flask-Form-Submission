from flask import Flask
import config
from exts import db,mail
from blueprints import user_bp,basic_bp
from flask_cors import CORS  #Flask的跨域问题
from flask_migrate import Migrate

# 应用配置信息
app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)

mail.init_app(app)

CORS(app, supports_credentials=True) 

migrate = Migrate(app, db)

# 注册蓝图
app.register_blueprint(user_bp)
app.register_blueprint(basic_bp)


if __name__ == '__main__':
    app.run()