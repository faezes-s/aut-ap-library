from datetime import datetime

from flask import jsonify, request

from app import save_data
from app.application import app
from books import load_data , save_data


@app.route("/api/v1/books/<book_id>/reserve", methods=["POST"])
def reserve_book(book_id: str):

    data=load_data()
    books=data["books"]
    users=data["users"]
    user_id=request.headers.get("user_id")
    if not user_id:
        return jsonify({"error":"Missing user_id in headers"}),400
    book=next((b for b in books if b["id"]==book_id),None)
    if not book:
        return jsonify({"error":"Book not found"}),404
    if book["is_reserved"]:
        return jsonify ({"error":"Book is already reserved"}),400
    user=next((u for u in users if u["id"]==user_id),None)
    if not user:
        return jsonify({"error":"User is not found"}),404
    book["is_reserved"]=True
    book["reserved_by"]=user_id
user["reserved_books"].append(book_id)
     save_data(data)
     return jsonify({
         "book_id":book_id,
         "user_id":user_id,
         "reservation_date":datetime.now().isoformat()
     })

@app.route("/api/v1/books/<book_id>/reserve", methods=["DELETE"])
def cancel_reservation(book_id: str):
    user_id = request.headers.get("user_id")
    if not user_id:
        raise BadRequest("user_id header is missing")

    data = load_data()
    users = data["users"]
    books = data["books"]

    user = next((u for u in users if u["id"] == user_id), None)
    if not user:
        raise NotFound("User not found")

    book = next((b for b in books if b["id"] == book_id), None)
    if not book:
        raise NotFound("Book not found")

    if not book["is_reserved"] or book["reserved_by"] != user_id:
        raise BadRequest("Book is not reserved by this user")

    # لغو رزرو
    book["is_reserved"] = False
    book["reserved_by"] = None
    if book_id in user["reserved_books"]:
        user["reserved_books"].remove(book_id)

    save_data(data)

    return jsonify({"message": "Reservation cancelled successfully"})


@app.route("/api/v1/users/<user_id>/reservations")
def get_user_reservations(user_id: str):
    requesting_user_id = request.headers.get("user_id")
    if not requesting_user_id:
        raise BadRequest("user_id header is missing")

    if requesting_user_id != user_id:
        raise Forbidden("You are not allowed to access this user's reservations")

    data = load_data()
    users = data["users"]
    books = data["books"]

    user = next((u for u in users if u["id"] == user_id), None)
    if not user:
        raise NotFound("User not found")

    reserved_book_ids = user.get("reserved_books", [])
    reserved_books = [book for book in books if book["id"] in reserved_book_ids]

    return jsonify(reserved_books)