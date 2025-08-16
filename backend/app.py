from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import logging
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os

app = Flask(__name__)
# 增强CORS配置，允许所有来源的跨域请求
CORS(app, resources={r"/api/*": {"origins": "*"}})
logging.basicConfig(level=logging.DEBUG)

# 配置
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///game.db'
app.config['SQLALCHEMY_DATABASE_PATH'] = os.path.join(os.path.dirname(__file__), 'instance')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads/avatars'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB

db = SQLAlchemy(app)

# 确保上传目录和实例目录存在
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(os.path.join(app.instance_path), exist_ok=True)

# 数据模型
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class GameRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref=db.backref('game_records', lazy=True))

# 创建数据库表
with app.app_context():
    db.create_all()

# 获取评级
def get_rating(score):
    if score <= 10:
        return "挠痒专业户"
    elif score <= 30:
        return "普通学生"
    elif score <= 60:
        return "优秀学生"
    elif score <= 100:
        return "学习标兵"
    else:
        return "学习之神"

# 用户注册
@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'error': '用户名和密码不能为空'}), 400
    
    if User.query.filter_by(username=username).first():
        return jsonify({'error': '用户名已存在'}), 400
    
    hashed_password = generate_password_hash(password)
    user = User(username=username, password=hashed_password)
    db.session.add(user)
    db.session.commit()
    
    return jsonify({
        'id': user.id,
        'username': user.username
    })

# 用户登录
@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    user = User.query.filter_by(username=username).first()
    
    if not user or not check_password_hash(user.password, password):
        return jsonify({'error': '用户名或密码错误'}), 401
    
    return jsonify({
        'id': user.id,
        'username': user.username
    })

# 注销账号
@app.route('/api/delete-account', methods=['POST'])
def delete_account():
    data = request.json
    user_id = data.get('user_id')
    
    if not user_id:
        return jsonify({'error': '缺少用户ID'}), 400
    
    # 只删除用户信息，保留游戏记录
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': '用户不存在'}), 404
    
    db.session.delete(user)
    db.session.commit()
    
    return jsonify({'message': '账号已注销，游戏记录已保留'})

# 保存游戏记录
@app.route('/api/game-record', methods=['POST'])
def save_game_record():
    data = request.json
    user_id = data.get('user_id')
    score = data.get('score')
    
    if not user_id or score is None:
        return jsonify({'error': '缺少必要参数'}), 400
    
    rating = get_rating(score)
    record = GameRecord(user_id=user_id, score=score, rating=rating)
    db.session.add(record)
    db.session.commit()
    
    return jsonify({
        'id': record.id,
        'score': record.score,
        'rating': record.rating,
        'created_at': record.created_at.isoformat()
    })

# 获取排行榜
@app.route('/api/leaderboard')
def leaderboard():
    # 获取每个用户的最高分
    leaderboard_data = db.session.query(
        User.username,
        db.func.max(GameRecord.score).label('max_score'),
        GameRecord.rating
    ).join(GameRecord).group_by(User.id).order_by(
        db.func.max(GameRecord.score).desc()
    ).limit(10).all()
    
    result = []
    for username, max_score, rating in leaderboard_data:
        result.append({
            'username': username,
            'score': max_score,
            'rating': rating
        })
    
    return jsonify(result)

# 获取用户游戏记录
@app.route('/api/user-records/<int:user_id>')
def user_records(user_id):
    records = GameRecord.query.filter_by(user_id=user_id).order_by(
        GameRecord.created_at.desc()
    ).limit(10).all()
    
    result = []
    for record in records:
        result.append({
            'id': record.id,
            'score': record.score,
            'rating': record.rating,
            'created_at': record.created_at.isoformat()
        })
    
    return jsonify(result)

@app.route('/')
def index():
    return "Backend service is running"

@app.route('/api/play-count')
def get_play_count():
    # 直接查询GameRecord表中的记录数
    total_plays = db.session.query(GameRecord).count()
    print(f"当前总游戏次数: {total_plays}")
    return jsonify({
        'total_plays': total_plays
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
