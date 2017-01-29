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
    return render_template('landing.html')

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
            user_login(email, password)
            session['email'] = request.form['email']
            redirect(url_for('landing'))
    return redirect(url_for('landing'))

@app.route('/logout', methods=['get'])
def logout():
    if session['email']:
        session.pop('email', None)
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
        cursor.close()
        conn.close()
    return result
