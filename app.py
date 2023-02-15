from flask import Flask,request,make_response,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api,Resource
from flask_cors import CORS
import os


db = SQLAlchemy()
app = Flask(__name__)
api = Api(app)
CORS(app)

# basedir = os.path.dirname(os.path.abspath(__file__))
# database = "sqlite:///" + os.path.join(basedir,"db.sqlite")
# app.config["SQLALCHEMY_DATABASE_URI"] = database

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://admin:adminizaus@localhost/flasknote_db"
app.config["SECRET_KEY"] = "dummytestapp74"
db.init_app(app)

class MyNoteModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title_note =  db.Column(db.String(255))
    html_note = db.Column(db.Text)

    # method for save data
    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except:
            return False

# Create Database
with app.app_context():
    db.create_all()

class MyNoteInsert(Resource):
    def post(self):
        dataTitleNote = request.form["title_note"]
        dataHtmlNote = request.form["html_note"]

        mynote = MyNoteModel(
            title_note=dataTitleNote,
            html_note=dataHtmlNote
        )
        mynote.save()

        response = {
            "msg":"data berhasil dimasukan",
            "code": 200
        }

        return make_response(jsonify(response), 200)


class MyNoteList(Resource):
    def get(self):
        query = MyNoteModel.query.all()

        output = [
            {
                "id"   : data.id,
                "title_note" : data.title_note,
            } 
            for data in query
        ]

        response = {
            "code" : 200,
            "msg"  : "Query Data Success",
            "data" : output
        }

        return make_response(jsonify(response), 200)

class MyNoteView(Resource):
    def get(self,id):
        query = MyNoteModel.query.filter_by(id=id).first()

        output = {
                "id"   : query.id,
                "title_note" : query.title_note,
                "html_note" : query.html_note
        }

        response = {
            "code" : 200,
            "msg"  : "Query Data Success",
            "data" : output
        }

        return make_response(jsonify(response), 200)

class MyNoteUpdate(Resource):
    def put(self,id):
        query = MyNoteModel.query.get(id)
        editTitleNote = request.form["title_note"]
        editHtmlNote = request.form["html_note"]

        query.title_note = editTitleNote
        query.html_note = editHtmlNote
        db.session.commit()

        response = {
            "msg":"data berhasil diedit",
            "code": 200
        }
        return response, 200
    
    def delete(self,id):
        queryData = MyNoteModel.query.get(id)
        
        db.session.delete(queryData)
        db.session.commit()

        response = {
            "msg":"data berhasil dihapus",
            "code": 200
        }
        return response, 200



api.add_resource(MyNoteInsert,'/api/insertnote', methods=["POST"])
api.add_resource(MyNoteList,'/api/listnote', methods=["GET"])
api.add_resource(MyNoteView,'/api/viewnote/<id>', methods=["GET"])
api.add_resource(MyNoteUpdate,'/api/updatenote/<id>', methods=["PUT","DELETE"])


if __name__ == '__main__':
    app.run(debug=True)

