from flask import Flask, jsonify

app = Flask(__name__)

USERS = {
    "1": {"id": "1", "name": "Alice", "status": "active"},
}


@app.route("/users/<user_id>")
def get_user(user_id):
    user = USERS.get(user_id)
    if not user:
        return jsonify({"error": "not found"}), 404
    return jsonify(user)


# --- Provider states endpoint, required by the Pact verifier ---
@app.route("/_pact/provider_states", methods=["POST"])
def provider_states():
    # In a real app this would set up DB fixtures matching the given state.
    # Here our single user is always present, so there's nothing to do.
    return jsonify({"result": "state set"})


if __name__ == "__main__":
    app.run(port=5001)
