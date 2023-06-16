from flask import Flask, render_template , flash,request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime

app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:nanashi7011@localhost/users"

app.config["SECRET_KEY"] = "nanashi@7011"


db = SQLAlchemy(app)
migrate = Migrate(app,db)
#model
class Users(db.Model):

    app.app_context().push()
    id = db.Column(db.Integer, primary_key = True) 
    name = db.Column( db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    fav_ani = db.Column(db.String(120))

    def __repr__(self) -> str:
        return '<Name %r>' % self.name

class UserForm(FlaskForm):
    name = StringField("Name" , validators=[DataRequired()])
    email = StringField("Email" , validators=[DataRequired()])
    fav_ani = StringField("Enter your favourite anime ")
    submit = SubmitField("Submit") 
#create a form class
class name_form(FlaskForm):
    name = StringField("what's your Name" , validators=[DataRequired()])
    age = StringField("what's your Age" , validators=[DataRequired()])
    submit = SubmitField("Submit") 
    # fav_ani = StringField("Enter your favourite anime")


@app.route('/delete/<int:id>')
def delete(id):
    name = None
    form = UserForm()
    user_to_delet = Users.query.get_or_404(id)
    try:
        db.session.delete(user_to_delet)
        db.session.commit()
        flash("User deleted successfully !!")
        our_users = Users.query.order_by(Users.date_added)
        return render_template("add_user.html", form= form, name=name ,our_users= our_users , )

    except:
        flash("Problem deleting the user <bold> try again <bold>")
        our_users = Users.query.order_by(Users.date_added)
        return render_template("add_user.html", form= form, name=name ,our_users= our_users , ) 
@app.route('/')
def index(): 
    return render_template("index.html")


@app.route('/about.html')
def about():
    return render_template("about.html")


@app.route('/contactus.html')
def contact_us():
    return "<h1>Hello fellow users</h1>"


@app.errorhandler(404)
def page_error(e):
    return render_template("404.html"), 404

@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
    name = None
    fav_ani = None
    form = UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None :
            user = Users(name=form.name.data, email = form.email.data , fav_ani = form.fav_ani.data)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.email.data = ''
        form.fav_ani.data = ''
        flash('User added successfully')
    our_users = Users.query.order_by(Users.date_added)
    return render_template("add_user.html", form= form, name=name ,our_users= our_users , )

@app.route('/name', methods=['GET','POST'])
def name():
    name = None
    age = None
    form = name_form()
    if form.validate_on_submit():
        name =  form.name.data
        age = form.age.data
        form.name.data =  ''
        form.age.data = " "
        flash("Form submitted Successfully")
        
    return render_template("name.html", name = name, form=form, age = age,)


@app.route('/update/<int:id>',methods=["GET","POST"])
def update(id):
    form = UserForm()
    name_two_update = Users.query.get_or_404(id)
    if request.method =="POST":
        name_two_update.name = request.form["name"]
        name_two_update.email = request.form["email"]
        name_two_update.fav_ani = request.form["fav_ani"]
        try:
            db.session.commit()
            flash("User Update Successfully !")

            return render_template("update.html",form=form, name_to_update=name_two_update)
        except:
             flash("There's was some problem ! Try Again !")

             return render_template("update.html",form=form, name_to_update=name_two_update)

    else:
        return render_template("update.html",form=form, name_to_update=name_two_update)

if __name__ == "__main__":
    app.run(debug=True)
