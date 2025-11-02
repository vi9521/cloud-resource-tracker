from flask import Flask, jsonify, request

app = Flask(__name__)

# Mock data
resources = [
    {"id": 1, "name": "VM Instance", "type": "Compute", "status": "Running"},
    {"id": 2, "name": "Storage Bucket", "type": "Storage", "status": "Available"},
]

@app.route('/')
def home():
    return "Cloud Resource Tracker API is running!"

# Get all resources
@app.route('/resources', methods=['GET'])
def get_resources():
    return jsonify(resources)

# Add a new resource
@app.route('/resources', methods=['POST'])
def add_resource():
    data = request.get_json()
    new_id = len(resources) + 1
    new_resource = {
        "id": new_id,
        "name": data.get("name"),
        "type": data.get("type"),
        "status": data.get("status", "Unknown")
    }
    resources.append(new_resource)
    return jsonify(new_resource), 201

# Update an existing resource
@app.route('/resources/<int:resource_id>', methods=['PUT'])
def update_resource(resource_id):
    for r in resources:
        if r["id"] == resource_id:
            data = request.get_json()
            r["name"] = data.get("name", r["name"])
            r["type"] = data.get("type", r["type"])
            r["status"] = data.get("status", r["status"])
            return jsonify(r)
    return jsonify({"error": "Resource not found"}), 404

# Delete a resource
@app.route('/resources/<int:resource_id>', methods=['DELETE'])
def delete_resource(resource_id):
    global resources
    resources = [r for r in resources if r["id"] != resource_id]
    return jsonify({"message": "Resource deleted"})

if __name__ == '__main__':
    app.run(debug=True)
