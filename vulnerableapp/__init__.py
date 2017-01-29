from flask import Flask, render_template, request, redirect,url_for, session

app = Flask(__name__)
app.secret_key = '123'
if app:
    import psycopg2
    from psycopg2.extras import DictCursor


if __name__ == "__main__":
    app.run()

'''
    Definig routes.
    Small application, separate route module is not introduced
'''

@app.route("/")
def landing():
    if 'user' in session.keys():
        session['user_messages'] = user_messages(session['user'][0])
    return render_template('landing.html')

@app.route("/message/<user_id>/<message>")
def post_message(user_id, message):
    message_create(user_id, message)
    return render_template('landing.html')

@app.route("/messages", methods=['POST', 'GET'])
def messages():
    print request.form
    print request.method

    if request.method == 'POST':
        # parent_id = request.form['parent_id'] or None
        message = request.form['message']
        # this is vulnerability
        # email = request.form['email']
        user_id = request.form['id']
        session['other_messages'] = message_create(user_id, message)
        session['user_messages'] = user_messages(user_id)
    if request.method == 'GET':
        user_messages(session['email'])
    return redirect(url_for('landing'))

    

@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if email and password:
            user_register(email, password)
            return redirect(url_for('landing'))
    return redirect(url_for('landing'))

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if email and password:
            session['user'] = user_login(email, password)
            session['email'] = request.form['email']
            session['user_messages'] = user_messages(session['user']['id'])
            redirect(url_for('landing'))
    return redirect(url_for('landing'))

@app.route('/logout', methods=['get'])
def logout():
    if session['email']:
        session.pop('email', None)
        session.pop('user', None)
    return redirect(url_for('landing'))


# maybe this database stuff could be moved.........
def user_login(email, password):
    SQL = " SELECT * FROM users WHERE email=%s and password=%s"
    data = (email, password)
    conn = psycopg2.connect("dbname=broccoli user=possibly")
    cursor = conn.cursor(cursor_factory=DictCursor)
    try:
        cursor.execute(SQL, data)
        result = cursor.fetchone()
    except:
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()
    return result

def user_register(email, password):
    SQL = "INSERT INTO users (email, password) VALUES (%s, %s) RETURNING *"
    data = (email, password)
    conn = psycopg2.connect("dbname=broccoli user=possibly")
    cursor = conn.cursor(cursor_factory=DictCursor)
    try:
        cursor.execute(SQL, data)
        result = cursor.fetchone()
    except:
        conn.rollback()
        raise
    finally:
        conn.commit()
        cursor.close()
        conn.close()
    return result

def user_messages(user_id):
    SQL = " SELECT * FROM messages WHERE user_id=%s"
    data = [user_id]
    conn = psycopg2.connect("dbname=broccoli user=possibly")
    cursor = conn.cursor(cursor_factory=DictCursor)
    try:
        cursor.execute(SQL, data)
        result = cursor.fetchall()
    except:
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()
    return result

def message_create(user_id, message, parent_id=None):
    SQL = "INSERT INTO messages (user_id, message) VALUES (%s, %s) RETURNING *"
    data = [user_id, message]
    
    if parent_id:
        SQL = "INSERT INTO messages (user_id, message, parent_id) VALUES (%s, %s, %s) RETURNING *"
        data = data + [parent_id]

    conn = psycopg2.connect("dbname=broccoli user=possibly")
    cursor = conn.cursor(cursor_factory=DictCursor)
    try:
        cursor.execute(SQL, data)
        result = cursor.fetchall()
    except:
        conn.rollback()
        raise
    finally:
        conn.commit()
        cursor.close()
        conn.close()
    return result
