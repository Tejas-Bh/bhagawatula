from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_admin.form import Select2Field
from flask_login import UserMixin, LoginManager, current_user, login_user, logout_user, login_required
from werkzeug.security import check_password_hash
from secrets import token_urlsafe

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = token_urlsafe(32)
app.config['FLASK_ADMIN_SWATCH'] = "flatly"
db = SQLAlchemy(app)
login = LoginManager(app)

@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(120), unique=True)

    def __init__(self, username, password):
        self.username = username
        self.password = password
class Tickets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    description = db.Column(db.String(10000000))
    date_created  = db.Column(db.DateTime,  default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime,  default=db.func.current_timestamp(),
                                        onupdate=db.func.current_timestamp())
    status = db.Column(db.String(50), default="open")
class About(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
#     status = db.relationship('Status')

# class Status(db.Model):
#     status = db.Column(db.String, db.ForeignKey('tickets.id'), nullable=False, unique=True, primary_key=True)

with app.app_context():
    db.create_all()

class TicketView(ModelView):
    can_create = True
    column_list = ('id', 'title', 'description', 'date_created', 'date_modified', 'status')
    form_excluded_columns = ['date_created', 'date_modified']
    form_overrides = {
        'status': Select2Field
    }
    form_args = {
        'status': {
            'choices': [
                ('Open', 'Open'),
                ('Work in Progress', 'Work in Progress'),
                ('Closed', 'Closed'),
                ('Pending', 'Pending'),
                ('Reopened', 'Reopened')
            ]
        }
    }
    with app.app_context():
        if current_user == User.query.filter_by(id=1).first():
            can_delete = True
        else: can_delete = False
    def is_accessible(self):
        return current_user.is_authenticated
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("home"))

class AboutView(ModelView):
    pass

class NewAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("home"))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))

@app.route('/login', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        name = request.form.get('name')
        password = request.form.get('password')

        user = User.query.filter_by(username=name).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user)
                if current_user == User.query.filter_by(id=1).first():
                    TicketView.can_delete = True
                return redirect("/admin")
            else:
                flash("Incorrect password, please try again.")
        else:
            flash("User not found, please try again.")

    return render_template("login.html")

@app.route("/admin/about")
def about():
    if current_user.is_authenticated:
        return render_template("about.html")
    else:
        return redirect(url_for("home"))

@app.route("/")
def bhagawatula():
    return render_template("bhagawatula.html")

admin = Admin(app, 'Austin Hindu Temple', index_view=NewAdminIndexView(), template_mode="bootstrap3")
admin.add_view(TicketView(Tickets, db.session))
# admin.add_view(AboutView(About, db.session))

if __name__ == "__main__":
    app.run()
