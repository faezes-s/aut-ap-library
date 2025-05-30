from flask import jsonify
from app.application import app
from books import load_data,save_data
import uuid

@app.route("/api/v1/users")
def get_users():
    data=load_data()
    return jsonify({"users":data["users"]})


@app.route("/api/v1/users/<user_id>")
def get_user(user_id: str):
    data=load_data()
    user=next((u for u in data["users"] if u["id"]==user_id),None)
    if not user:
        raise NotFound("User not found")
    return jsonify({"user":user})


@app.route("/api/v1/users", methods=["POST"])
def create_user():
    body = request.get_json()
    if not body or "name" not in body:
        raise BadRequest("Invalid request body. 'name' is required.")

    data = load_data()

    new_user = {
        "id": str(uuid.uuid4()),
        "name": body["name"],
        "reserved_books": []
    }

    data["users"].append(new_user)
    save_data(data)

    return jsonify({"user": new_user})



@app.route("/api/v1/users/<user_id>", methods=["PUT"])
def update_user(user_id: str):
    body = request.get_json()
    if not body or "name" not in body:
        raise BadRequest("Invalid request body. 'name' is required.")

    data = load_data()
    users = data["users"]
    user = next((u for u in users if u["id"] == user_id), None)

    if not user:
        raise NotFound("User not found")

    user["name"] = body["name"]
    save_data(data)

    return jsonify({"user": user})