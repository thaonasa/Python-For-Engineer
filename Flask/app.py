from flask import Flask, render_template, request, redirect, url_for, flash
from create_db import db, User
from forms import AddUserForm, EditUserForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

# Khởi tạo database với ứng dụng
db.init_app(app)

# Trang chính hiển thị danh sách người dùng
@app.route('/')
def index():
    users = User.query.all()
    return render_template('index.html', users=users)

# Thêm người dùng mới
@app.route('/add', methods=['GET', 'POST'])
def add_user():
    form = AddUserForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data, email=form.email.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Thêm người dùng thành công', 'success')
        return redirect(url_for('index'))
    return render_template('add_user.html', form=form)

# Chỉnh sửa người dùng
@app.route('/edit/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    form = EditUserForm(obj=user)
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        db.session.commit()
        flash('Cập nhật người dùng thành công', 'success')
        return redirect(url_for('index'))
    return render_template('edit_user.html', form=form)

# Xóa người dùng
@app.route('/delete/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('Xóa người dùng thành công', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Tạo bảng trong database
    app.run(debug=True)
