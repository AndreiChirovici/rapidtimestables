from flask import Flask, g, redirect, render_template, url_for, request, session

class User:
    def __init__(self, id, username, memword, score):
        self.id = id
        self.username = username
        self.memword = memword
        self.score = score

    def __repr__(self):
        return f'<User: {self.username}>'

# Initialising array of users
users = []
# users.append(User(id=0, username='Andrei', memword='computing', score=0))
# users.append(User(id=2, username='Chris', memword='car', score=0))

print(users)

appy = Flask(__name__)
appy.secret_key = 'averysecretkey1'

@appy.before_request
def before_request():
    g.user = None

    # 1) Checks if user is in session
    # 2) If user no longer exists but is still in session, will clear the session
    try:
        if 'user_id' in session:
            user = [x for x in users if x.id == session['user_id']][0]
            g.user = user
    except:
        return session.clear()

@appy.route('/')
@appy.route('/home')
def index():
    return render_template('index.html')

@appy.route('/about')
def about():
    return render_template('about.html')

@appy.route('/learn')
def learn():
    return render_template('learn.html')

@appy.route('/practice', methods=['GET', 'POST'])
def practice():
    if not g.user:
        return redirect(url_for('register'))

    score = g.user.score
    if request.method == 'POST':
        lastScore = int(request.form['streakLabel'])
        if lastScore > score:
            score = lastScore
            users[g.user.id].score == score
            return redirect(url_for('myaccount'))

    return render_template('practice.html')

@appy.route('/login', methods=['GET', 'POST'])
def login():
    if g.user:
        return redirect(url_for('myaccount'))

    if request.method == 'POST':
        session.pop('user_id', None)

        username = request.form['usernamelogin']
        memword = request.form['memwordlogin']

        try:
            user = [x for x in users if x.username == username][0]
            if user and user.memword == memword:
                session['user_id'] = user.id
                return redirect(url_for('myaccount'))
            else:
                return redirect(url_for('login'))
        except:
            return redirect(url_for('login'))
        
    return render_template('login.html')

@appy.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        session.pop('user_id', None)

        usernamereg = request.form['usernameregister']
        memwordreg = request.form['memwordregister']
        userid = len(users)
        users.append(User(id=userid, username=usernamereg, memword=memwordreg, score=0))
        return redirect(url_for('login'))

    return render_template('register.html')

@appy.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))

@appy.route('/myaccount')
def myaccount():
    if not g.user:
        return redirect(url_for('register'))

    return render_template('myaccount.html')


if __name__ == "__main__":
    appy.run(debug=True)