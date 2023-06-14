from flask import Flask,request,make_response,jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
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

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://admin:izausadmin@localhost/flasknote_db"

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
        try:
            dataTitleNote = request.json["title_note"]
            dataHtmlNote = request.json["html_note"]

            # Validate the data
            if not dataTitleNote:
                response = {
                    "code" : 400,
                    "error" : "Title is required."
                }
                return make_response(jsonify(response), 400)
            if not dataHtmlNote:
                response = {
                    "code" : 400,
                    "error" : "Content is required."
                }
                return make_response(jsonify(response), 400)
            
            #Check Note Exist
            if MyNoteModel.query.filter_by(title_note=dataTitleNote).first():
                response = {
                    "code" : 409,
                    "error" : "Item already exists."
                }
                return make_response(jsonify(response), 409)

            # Process Data
            mynote = MyNoteModel(
                title_note=dataTitleNote,
                html_note=dataHtmlNote
            )
            mynote.save()

            response = {
                "msg":"Data Successfully Inserted",
                "code": 200
            }

            return make_response(jsonify(response), 200)


        except SQLAlchemyError as e:
            db.session.rollback()
            response = {
                "code" : 500,
                "error" : str(e)
            }
            return make_response(jsonify(response), 500)
        

        except Exception as e:
            db.session.rollback()
            response = {
                "code" : 500,
                "error" : str(e)
            }
            return make_response(jsonify(response), 500)


class MyNoteList(Resource):
    def get(self):
        try :
            query = MyNoteModel.query.all()

            # Process Data
            output = [
                {
                    "id"   : data.id,
                    "title_note" : data.title_note,
                } 
                for data in query
            ]
        
            response = {
                "code" : 200,
                "data" : output
            }
            return make_response(jsonify(response), 200)
        
        except Exception as e:
            
            response = {
                "code" : 500,
                "error" : str(e)
            }
            return make_response(jsonify(response), 500)

class MyNoteView(Resource):
    def get(self,id):
        try :
            query = MyNoteModel.query.filter_by(id=id).first()

            # Check if the item exists
            if not query:
                response = {
                    "code" : 404,
                    "error" : "Note not found."
                }
                return make_response(jsonify(response), 404)

            # Process Data
            output = {
                    "id"   : query.id,
                    "title_note" : query.title_note,
                    "html_note" : query.html_note
            }

            response = {
                "code" : 200,
                "data" : output
            }

            return make_response(jsonify(response), 200)

        except Exception as e:
            
            response = {
                "code" : 500,
                "error" : str(e)
            }
            return make_response(jsonify(response), 500)

class MyNoteUpdate(Resource):
    def put(self,id):
        try:
            editTitleNote = request.json["title_note"]
            editHtmlNote = request.json["html_note"]

            query = MyNoteModel.query.get(id)

            # Check if the item exists
            if not query:
                response = {
                    "code" : 404,
                    "error" : "Note not found."
                }
                return make_response(jsonify(response), 404)

            # Validate the data
            if not editTitleNote:
                response = {
                    "code" : 400,
                    "error" : "Title is required."
                }
                return make_response(jsonify(response), 400)
            if not editHtmlNote:
                response = {
                    "code" : 400,
                    "error" : "Content is required."
                }
                return make_response(jsonify(response), 400)

            #Check Note Exist
            if MyNoteModel.query.filter_by(title_note=editTitleNote).first():
                response = {
                    "code" : 409,
                    "error" : "Note Title already exists."
                }
                return make_response(jsonify(response), 409)
                
            # Process Data
            query.title_note = editTitleNote
            query.html_note = editHtmlNote
            db.session.commit()

            response = {
                "msg":"Data Successfully Updated",
                "code": 200
            }
            return make_response(jsonify(response), 200)

        except SQLAlchemyError as e:
            db.session.rollback()
            response = {
                "code" : 500,
                "error" : str(e)
            }
            return make_response(jsonify(response), 500)
        

        except Exception as e:
            db.session.rollback()
            response = {
                "code" : 500,
                "error" : str(e)
            }
            return make_response(jsonify(response), 500)
        
    
    def delete(self,id):
        try:
            query = MyNoteModel.query.get(id)

            # Check if the item exists
            if not query:
                response = {
                    "code" : 404,
                    "error" : "Note not found."
                }
                return make_response(jsonify(response), 404)
            
            # Process Data
            db.session.delete(query)
            db.session.commit()

            response = {
                "msg":"Data Successfully Deleted",
                "code": 200
            }
            return make_response(jsonify(response), 200)

        except SQLAlchemyError as e:
            db.session.rollback()
            response = {
                "code" : 500,
                "error" : str(e)
            }
            return make_response(jsonify(response), 500)
        

        except Exception as e:
            db.session.rollback()
            response = {
                "code" : 500,
                "error" : str(e)
            }
            return make_response(jsonify(response), 500)

class MyNoteSearch(Resource):
    def get(self):
        try :
            search = request.args.get("title_note")

            query = MyNoteModel.query.filter(MyNoteModel.title_note.like('%'+search+'%') | MyNoteModel.html_note.like('%'+search+'%')).all()

            #Process Data
            output = [
                {
                    "id"   : data.id,
                    "title_note" : data.title_note,
                } 
                for data in query
            ]

            response = {
                "code" : 200,
                "data" : output
            }
            
            return make_response(jsonify(response),200)

        except SQLAlchemyError as e:
            db.session.rollback()
            response = {
                "code" : 500,
                "error" : str(e)
            }
            return make_response(jsonify(response), 500)
        

        except Exception as e:
            db.session.rollback()
            response = {
                "code" : 500,
                "error" : str(e)
            }
            return make_response(jsonify(response), 500)


api.add_resource(MyNoteInsert,'/api/notes', methods=["POST"])
api.add_resource(MyNoteList,'/api/notes', methods=["GET"])
api.add_resource(MyNoteView,'/api/note/<id>', methods=["GET"])
api.add_resource(MyNoteUpdate,'/api/note/<id>', methods=["PUT","DELETE"])
api.add_resource(MyNoteSearch,'/api/search', methods=["GET"])


if __name__ == '__main__':
    app.run(debug=True)

