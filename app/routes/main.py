from flask import Blueprint, render_template, request, redirect, url_for, session, flash, send_file
from app.models.user import User
from app.utils.room import rooms, handle_join_room, handle_create_room, update_room_info
from app.utils.crypto import sign_file, verify_signature, save_signature_to_file
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from cryptography.hazmat.primitives import serialization

main = Blueprint('main', __name__)

@main.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    return render_template('index.html', rooms=rooms)

@main.route('/create_room', methods=['POST'])
def create_room():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    room_name = request.form['room_name']
    password = request.form['password']
    room_id = handle_create_room(room_name, password)
    flash('Tạo phòng chat thành công! Mời bạn bè tham gia.')
    return redirect(url_for('main.room', room_id=room_id))

@main.route('/join_room', methods=['POST'])
def join_room_route():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    room_id = request.form['room_id']
    password = request.form['password']
    room = handle_join_room(room_id, password)
    if room:
        flash('Tham gia phòng chat thành công! Chúc bạn có những cuộc trò chuyện thú vị.')
        return redirect(url_for('main.room', room_id=room_id))
    flash('Mã phòng hoặc mật khẩu không chính xác!')
    return redirect(url_for('main.index'))

@main.route('/room/<room_id>', methods=['GET', 'POST'])
def room(room_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    room = rooms.get(room_id)
    if not room:
        return redirect(url_for('main.index'))
    user = User.query.get(session['user_id'])
    username = user.username if user else str(session['user_id'])
    if username not in room['members']:
        room['members'].append(username)
    files = room.get('files', [])
    user_objs = User.query.all()
    users_dict = {u.username: {'username': u.username, 'public_key': u.public_key} for u in user_objs}
    return render_template('room.html', room=room, room_id=room_id, files=files, users=users_dict)

@main.route('/upload/<room_id>', methods=['POST'])
def upload(room_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    room = rooms.get(room_id)
    if not room:
        flash('Không tìm thấy phòng chat!')
        return redirect(url_for('main.index'))
    if 'file' not in request.files:
        flash('Vui lòng chọn file để tải lên!')
        return redirect(url_for('main.room', room_id=room_id))
    file = request.files['file']
    if file.filename == '':
        flash('Bạn chưa chọn file nào!')
        return redirect(url_for('main.room', room_id=room_id))
    
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
        
    filename = secure_filename(file.filename)
    file_path = os.path.join('uploads', room_id + '_' + filename)
    file.save(file_path)
    
    user = User.query.get(session['user_id'])
    signature = sign_file(file_path, user.get_private_key())
    sig_path = file_path + '.sig'
    save_signature_to_file(signature, sig_path)
    
    file_info = {
        'filename': filename,
        'path': file_path,
        'sig': sig_path,
        'size': os.path.getsize(file_path),
        'uploaded_at': datetime.now(),
        'uploader': user.username if user else None
    }
    
    update_room_info(room_id, file_info)
    flash('Tải file lên thành công! File đã được ký số.')
    return redirect(url_for('main.room', room_id=room_id))

@main.route('/download/<room_id>/<filename>')
def download(room_id, filename):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    file_path = os.path.join('uploads', room_id + '_' + filename)
    if not os.path.exists(file_path):
        flash('File không tồn tại!')
        return redirect(url_for('main.room', room_id=room_id))
    return send_file(file_path, as_attachment=True)

@main.route('/download_sig/<room_id>/<filename>')
def download_sig(room_id, filename):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    sig_path = os.path.join('uploads', room_id + '_' + filename + '.sig')
    if not os.path.exists(sig_path):
        flash('Chữ ký không tồn tại!')
        return redirect(url_for('main.room', room_id=room_id))
    return send_file(sig_path, as_attachment=True)

@main.route('/verify/<room_id>/<filename>', methods=['POST'])
def verify(room_id, filename):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    public_pem = request.form.get('verify_public_pem')
    if not public_pem:
        flash('Bạn phải nhập public key để xác minh!')
        return redirect(url_for('main.room', room_id=room_id))
    try:
        public_key = serialization.load_pem_public_key(public_pem.encode())
    except Exception:
        flash('Public key không hợp lệ!')
        return redirect(url_for('main.room', room_id=room_id))
    file_path = os.path.join('uploads', room_id + '_' + filename)
    sig_path = file_path + '.sig'
    if not os.path.exists(file_path) or not os.path.exists(sig_path):
        flash('File hoặc chữ ký không tồn tại!')
        return redirect(url_for('main.room', room_id=room_id))
    with open(sig_path, 'rb') as f:
        signature = f.read()
    valid = verify_signature(file_path, signature, public_key)
    if valid:
        flash('Chữ ký hợp lệ! File toàn vẹn và đúng nguồn gửi.')
    else:
        flash('Chữ ký không hợp lệ hoặc file đã bị thay đổi!')
    return redirect(url_for('main.room', room_id=room_id)) 