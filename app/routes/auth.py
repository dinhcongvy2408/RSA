from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.models.user import User, db
from app.utils.crypto import generate_keys

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if User.query.filter_by(username=username).first():
            flash('Tên người dùng đã tồn tại trong hệ thống!')
            return redirect(url_for('auth.register'))
        user = User(username=username)
        user.set_password(password)
        # Tạo key mặc định cho user mới
        private_key, private_pem, public_pem = generate_keys()
        user.set_keys(private_pem, public_pem)
        db.session.add(user)
        db.session.commit()
        flash('Đăng ký tài khoản thành công! Vui lòng đăng nhập để tiếp tục.')
        return redirect(url_for('auth.login'))
    return render_template('register.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            flash('Đăng nhập thành công! Chào mừng bạn đến với hệ thống.')
            return redirect(url_for('main.index'))
        flash('Tên đăng nhập hoặc mật khẩu không chính xác!')
    return render_template('login.html')

@auth.route('/logout')
def logout():
    session.clear()
    flash('Bạn đã đăng xuất khỏi hệ thống!')
    return redirect(url_for('auth.login')) 