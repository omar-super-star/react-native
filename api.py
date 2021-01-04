from flask import *
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os
app = Flask(__name__)
database_filename = "data.sqlite"
project_dir = os.path.dirname(os.path.abspath(__file__))
print(project_dir)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///{}".format(os.path.join(project_dir, database_filename))
app.config['UPLOAD_FOLDER'] =project_dir+"/static/image"
app.secret_key = "bhbnbjblkbkbkbkjb454213356165"
db = SQLAlchemy(app)

class tshirt(db.Model):
    id = db.Column(db.Integer().with_variant(db.Integer, "sqlite"), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    typetshirt=db.Column(db.Integer, db.ForeignKey('typetshirt.id'))
    price =  db.Column(db.Float(), nullable=True)
    image=  db.Column(db.String(500), nullable=True)
    url=db.Column(db.String(500), nullable=True)
class typetshirt(db.Model):
    id = db.Column(db.Integer().with_variant(db.Integer, "sqlite"), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    

@app.route("/",methods=["get"])
def get_product():
    tshirtlist=db.session.query(tshirt).all()
    datasend=[]
    for t_shirt in tshirtlist:
        datasend.append({
            "name":t_shirt.name,
            "type":db.session.query(typetshirt).filter_by(id=t_shirt.typetshirt).first().name,
            "price":t_shirt.price,
            "image":t_shirt.image,
            "url":t_shirt.url
        })
    return jsonify(datasend)

@app.route("/",methods=["POST"])
def new_order():
    print("work")
    name=request.form.get("name")
    price=request.form.get("price")
    typetshirt=request.form.get("type")
    file=request.files.get("image")
    url=request.form.get("url")
    filename=secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    p=tshirt(name=name,
              typetshirt=typetshirt,
               price=price,
              image=filename,
             url=url)
    db.session.add(p)
    db.session.commit()
    return "success"





