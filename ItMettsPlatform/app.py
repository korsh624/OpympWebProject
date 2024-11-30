from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
import hashlib
import os
import random

app = Flask(__name__)
app.secret_key = 'your_super_secret_key'
UPLOAD_FOLDER = 'static/images'  # Папка для изображений
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                is_admin INTEGER NOT NULL DEFAULT 0
            );
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                city TEXT NOT NULL,
                address TEXT NOT NULL,
                datetime TEXT NOT NULL,
                contacts TEXT NOT NULL,
                participants TEXT,
                image_path TEXT
            );
        ''')
        conn.commit()

def get_random_image():
    images = [img for img in os.listdir(app.config['UPLOAD_FOLDER']) if img.endswith(('.png', '.jpg', '.jpeg', '.gif'))]
    if images:
        return os.path.join('images', random.choice(images))  # Возвращаем относительный путь
    return None

# Initialize the database
init_db()

def find_user_by_email(email):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        return cursor.fetchone()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

@app.route('/')
def index():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM events')
        events = cursor.fetchall()
    return render_template('index.html', events=events, current_user=session.get('user'))

@app.route('/register', methods=['POST'])
def register():
    email = request.form.get('email')
    password = request.form.get('password')
    
    if not email or not password:
        flash('Email и пароль обязательны!')
        return redirect(url_for('index'))
    
    if find_user_by_email(email):
        flash('Пользователь с таким email уже существует')
        return redirect(url_for('index'))
    
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (email, password) VALUES (?, ?)', 
                       (email, hash_password(password)))
        conn.commit()
    
    flash('Регистрация успешна!')
    return redirect(url_for('index'))

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    
    if not email or not password:
        flash('Email и пароль обязательны!')
        return redirect(url_for('index'))
    
    user = find_user_by_email(email)
    if user and user['password'] == hash_password(password):
        session['user'] = dict(user)
        flash('Вход выполнен успешно!')
        return redirect(url_for('index'))
    
    flash('Неверный email или пароль')
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('Вы вышли из системы.')
    return redirect(url_for('index'))

@app.route('/add_event', methods=['GET', 'POST'])
def add_event():
    if request.method == 'POST':
        event = {
            'name': request.form['name'],
            'city': request.form['city'],
            'address': request.form['address'],
            'datetime': request.form['datetime'],
            'contacts': request.form['contacts'],
            'participants': '',
            'image_path': request.form.get('image_path', '')  # Путь к изображению является необязательным
        }
        
        # Если изображение не указано, выбираем случайное
        if not event['image_path']:
            event['image_path'] = get_random_image()
        
        # Проверка обязательных полей
        required_fields = [event['name'], event['city'], event['address'], event['datetime'], event['contacts']]
        
        if not all(required_fields):
            flash('Все поля обязательны для заполнения!')
            return redirect(url_for('index'))

        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO events (name, city, address, datetime, contacts, participants, image_path) VALUES (?, ?, ?, ?, ?, ?, ?)', 
                           (event['name'], event['city'], event['address'], event['datetime'], event['contacts'], event['participants'], event['image_path']))
            conn.commit()
        
        flash('Событие успешно добавлено!')
        return redirect(url_for('index'))
    
    return render_template('index.html')  # Adjust this if necessary

@app.route('/edit_event/<int:event_id>', methods=['GET', 'POST'])
def edit_event(event_id):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        if request.method == 'POST':
            updated_event = {
                'name': request.form['name'],
                'city': request.form['city'],
                'address': request.form['address'],
                'datetime': request.form['datetime'],
                'contacts': request.form['contacts'],
                'image_path': request.form.get('image_path', '')  # Путь к изображению является необязательным
            }
            if not all(updated_event.values()):
                flash('Все поля обязательны для заполнения!')
                return redirect(url_for('edit_event', event_id=event_id))
            
            # Если изображение не указано, выбираем случайное
            if not updated_event['image_path']:
                updated_event['image_path'] = get_random_image()
            
            cursor.execute('UPDATE events SET name = ?, city = ?, address = ?, datetime = ?, contacts = ?, image_path = ? WHERE id = ?', 
                           (updated_event['name'], updated_event['city'], updated_event['address'], updated_event['datetime'], updated_event['contacts'], updated_event['image_path'], event_id))
            conn.commit()
            flash('Событие успешно обновлено!')
            return redirect(url_for('index'))
        
        cursor.execute('SELECT * FROM events WHERE id = ?', (event_id,))
        event = cursor.fetchone()
    
    return render_template('edit_event.html', event=event)

@app.route('/delete_event/<int:event_id>', methods=['POST'])
def delete_event(event_id):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM events WHERE id = ?', (event_id,))
        event = cursor.fetchone()
        
        if event is None:
            flash('Мероприятие не найдено!')
            return redirect(url_for('index'))
        
        cursor.execute('DELETE FROM events WHERE id = ?', (event_id,))
        conn.commit()
    
    flash('Событие успешно удалено!')
    return redirect(url_for('index'))

@app.route('/participate/<int:event_id>', methods=['POST'])
def participate(event_id):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        user_email = session.get('user', {}).get('email')
        
        if not user_email:
            flash('Сначала войдите в систему, чтобы участвовать в мероприятии.')
            return redirect(url_for('index'))
        
        cursor.execute('SELECT participants FROM events WHERE id = ?', (event_id,))
        event = cursor.fetchone()
        
        participants = event['participants'].split(',') if event['participants'] else []
        
        if user_email in participants:
            flash('Вы уже записаны на это мероприятие.')
            return redirect(url_for('index'))
        
        participants.append(user_email)
        updated_participants = ','.join(participants)
        
        cursor.execute('UPDATE events SET participants = ? WHERE id = ?', (updated_participants, event_id))
        conn.commit()
    
    flash('Вы успешно записались на мероприятие!')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)  # Allow access over the local network