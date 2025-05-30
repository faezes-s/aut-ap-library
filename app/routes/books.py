from app.application import app
from flask import jsonify
import json


DB_PATH="db.json"
def load_data():
    with open(DB_PATH,"r") as f:
        return json.load(f)
def save_data(data):
    with open (DB_PATH,"w") as f:
        json.dump(data,f,indent=4)

@app.route("/api/v1/books",methods=["GET"])
def get_books():
    data=load_data()
    books=data.get("books",[])
    return jsonify({"books": books})


@app.route("/api/v1/books/<book_id>",methods=["GET"])
def get_book(book_id: str):
    data=load_data()
    books=data.get("books",[])


    for book in books:
        if book["id"]==book_id:
            return jsonify({"book":book})

    return jsonify({"error":"Book is not found"}),404



@app.route("/api/v1/books", methods=["POST"])
def create_book():
    data=load_data()
    books=data.get("books",[])
    book_data= request.get_json()

    required_fields=["title","author","isbn"]
    if not book_data or any(field not in book_data for field in required_fields):
        return jsonify ({"error":"Invalid request body"}),400

    new_id=str(max([int(book["id"]) for book in books] + [0]) +1)
    new_book={
        "id":new_id,
        "title":book_data["title"],
        "author":book_data["author"],
        "isbn":book_data["isbn"],
        "is_reserved":False,
        "reserved_by":None
    }

    books.append(new_book)
    data["books"]=books
    save_data(data)

    return jsonify({"book":new_book}),201

    


@app.route("/api/v1/books/<book_id>", methods=["DELETE"])
def delete_book(book_id: str):
    data=load_data()
    books=data.get("books",[])

    for book in books:
        if book["id"]==book_id:
            if book["is_reserved"]:
                return jsonify({"message": "can not delete a reserved book"}),400
            books.remove(book)
            data["books"]=books
            save_data(data)
            return jsonify({"message":"book is deleted"})
    return jsonify({"message":"book is not found"}),404













