from flask import Flask, render_template, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:junaid@localhost/test"
db = SQLAlchemy(app)                                # username:password@localhost/dbname

class Task(db.Model):
    __tablename__ = 'tasks'
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"
    
class Users(db.Model):
    __tablename__ = 'usertable'
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    def __repr__(self):
        return f"(name='{self.name}', email='{self.email}', password='{self.password}')"


with app.app_context():
    db.create_all()


@app.route('/', methods=['GET', 'POST'])
def task():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        if title and desc:
            todo = Task(title=title, desc=desc)
            db.session.add(todo)
            db.session.commit()
    allTodo = Task.query.all()
    # return jsonify({
    #     "sno": allTodo.sno,
    #     "title": allTodo.title,
    #     "desc": allTodo.desc
    # })
    return render_template("index.html", allTodo = allTodo)




# Deletion
@app.route('/delete/<int:sno>', methods=['DELETE'])
def delete(sno):
    todo = Task.query.get(sno)
    if not todo:
        return jsonify({"error": "Todo not found"}), 404
    db.session.delete(todo)
    db.session.commit()
    print("data deleted")
    return jsonify({"message": "Todo deleted successfully"})




# Updation
@app.route('/update/<int:sno>', methods=['GET', 'PUT'])
def update(sno):
    if request.method == 'PUT':
        todo = Task.query.get(sno)
        print(todo)
        data = request.get_json()   # Parse JSON data from the request
        print(data)
        if 'title' in data:
            todo.title = data['title']
        if 'desc' in data:
            todo.desc = data['desc']
        db.session.commit()
        return jsonify({"success": True})
    
    todo = Task.query.get(sno)
    return render_template('update.html', todo = todo)


# signup route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        if name and email and password:
            data = Users(name=name, email=email, password=password)
            print(data)
            db.session.add(data)
            db.session.commit()
            return redirect('/regsuccess')
    return render_template("signup.html")

@app.route('/regsuccess')
def regsuccess():
    return render_template("regsuccess.html")

# singin route
@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        data = Users.query.all()
        for task in data:
            if task.email == email and task.password == password:
                return redirect('/loginsuccess')
            
        return render_template('signin.html', error='Invalid user')
    return render_template('signin.html')

@app.route('/profile')
def loginSuccess():
    return render_template("profile.html")




    
if __name__ == '__main__':
    app.run(debug=True, port=3000)
