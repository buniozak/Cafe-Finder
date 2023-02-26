from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask import Flask,render_template,request
import requests

app = Flask(__name__,template_folder="docs")
bootstrap = Bootstrap5(app)

##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
SQLALCHEMY_SILENCE_UBER_WARNING=1

db = SQLAlchemy(app)


##Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=True)
    img_url = db.Column(db.String(500), nullable=True)
    location = db.Column(db.String(250), nullable=True)
    seats = db.Column(db.String(250), nullable=True)
    has_toilet = db.Column(db.Boolean, nullable=True)
    has_wifi =db. Column(db.Boolean, nullable=True)
    has_sockets = db.Column(db.Boolean, nullable=True)
    can_take_calls = db.Column(db.Boolean, nullable=True)
    coffee_price =db. Column(db.String(250), nullable=True)


with app.app_context():
    db.create_all()




@app.route("/",methods = ['POST', 'GET'])
def home():
    cafes = db.session.query(Cafe).all()


    return render_template('index.html',cafes=cafes)


@app.route("/2",methods = ['POST', 'GET'])
def other_page():
    cafes = db.session.query(Cafe).all()
    cafes= cafes[10:22]
    return render_template("index_2.html",cafes=cafes)


cafes_list=[]

find_cafes_names=[]

@app.route("/search",methods = ['POST', 'GET'])
def search():
    global find_cafes_names
    cafes_all = db.session.query(Cafe).all()
    find_cafes_names = []
    cafes = db.session.query(Cafe.name).all()
    entry=request.form["search"]

    for name in cafes:
        name=str(name).lower()
        cafes_list.append(name)

    results = [name for name in cafes_list if entry in name]
    results = set(results)

    for a in results:

        my_string = a.replace('(', '').replace(')', '').replace(',', '').replace("'",'')

        my_string = my_string.upper().title()
        find_cafes_names.append(my_string)

    cafe_find=[]
    for names in find_cafes_names:
        cafes_find=Cafe.query.filter_by(name=names).all()
        if cafes_find==[]:
            del cafes_find
        else:
            for a in cafes_find:


                cafe_find.append(a)



    return render_template('index.html', cafes=cafe_find)



if __name__=="__main__":
    app.run(debug=True)