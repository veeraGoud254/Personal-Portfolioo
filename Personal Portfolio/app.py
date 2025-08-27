from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///portfolio.db'
db = SQLAlchemy(app)

# ---------- Database Models ----------
class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    link = db.Column(db.String(200))

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)

# ---------- Routes ----------
@app.route('/')
def home():
    return render_template("home.html")

@app.route('/projects')
def projects():
    all_projects = Project.query.all()
    return render_template("projects.html", projects=all_projects)

@app.route('/blog')
def blog():
    all_posts = Blog.query.all()
    return render_template("blog.html", posts=all_posts)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        message = request.form['message']
        print(f"New Message from {name}: {message}")  # Can also save to DB
        return redirect(url_for('home'))
    return render_template("contact.html")

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        link = request.form['link']
        
        new_project = Project(title=title, description=description, link=link)
        db.session.add(new_project)
        db.session.commit()
        
        return redirect(url_for('projects'))  # Go to projects page after saving
    
    return render_template("admin.html")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
