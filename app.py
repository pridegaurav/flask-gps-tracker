from flask import Flask, jsonify, request, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Global dictionary for GPS data
gps_data = {"lat": 0.0, "lng": 0.0}

@app.route("/")
def index():
    return render_template("map.html")

@app.route("/gps", methods=["GET"])
def get_gps():
    """Return latest GPS coordinates"""
    return jsonify(gps_data)

@app.route("/update_gps", methods=["POST"])
def update_gps():
    """Receive GPS data from ESP32"""
    global gps_data
    data = request.get_json()

    if not data or "lat" not in data or "lng" not in data:
        return jsonify({"error": "Invalid data"}), 400

    gps_data["lat"] = float(data["lat"])
    gps_data["lng"] = float(data["lng"])
    print(f"✅ GPS Updated: {gps_data}")
    return jsonify({"status": "ok", "data": gps_data})

if __name__ == "__main__":
    # Host on all network interfaces so ESP32 can access it
    app.run(host="0.0.0.0", port=5000)