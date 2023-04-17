import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////' + os.path.join(
    os.path.dirname(app.root_path), os.getenv('DATABASE_FILE', 'data.db')
)  # 配置数据库的地址, 三个/表示相对路径, 四个/表示绝对路径
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型修改的监控


db = SQLAlchemy(app)  # 初始化数据库， 传入app
login_manager = LoginManager(app)  # 实例化扩展类
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    from watchlist.models import User

    user = User.query.get(int(user_id))
    return user


@app.context_processor
def inject_user():
    from watchlist.models import User

    user = User.query.first()
    return dict(user=user)


from watchlist import views, errors, commands
