# 基于Vue2.0、Element-UI、Flask、MySQL实现各种表单填写存储、邮箱验证码、轮播图描述列表展示

**实现前后端分离，前端使用Vue2.0、Element-UI，后端使用Flask，数据库选用MySQL**

**实现各种表单填写存储、邮箱验证码、轮播图描述列表展示**

![表单提交页面](https://github.com/Aomr1/Vue-Flask-Form-Submission/blob/main/pic/1.png)
![表单展示页面](https://github.com/Aomr1/Vue-Flask-Form-Submission/blob/main/pic/2.png)

### 启动项目

1. 启动app.py入口文件

```python
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
```

2. 进入flask_vue文件下，输入npm run serve即可
