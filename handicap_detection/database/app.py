import jinja2
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///parking_database.db"
db = SQLAlchemy(app)

class Camera(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    camera_id = db.Column(db.String(100), nullable=False)

class LicensePlate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    license_plate = db.Column(db.String(100), nullable=False)
    camera_id = db.Column(db.Integer, db.ForeignKey("camera.id"), nullable=False)
    camera = db.relationship("Camera", backref="license_plates")

class HandicapStatus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    license_plate_id = db.Column(db.Integer, db.ForeignKey("license_plate.id"), nullable=False)
    is_handicapped = db.Column(db.Boolean, nullable=False)
    license_plate = db.relationship("LicensePlate", backref="handicap_status")

@app.route("/cameras", methods=["POST"])
def create_camera():
    camera_id = request.json["camera_id"]
    camera = Camera(camera_id=camera_id)
    db.session.add(camera)
    db.session.commit()
    return jsonify({"id": camera.id, "camera_id": camera.camera_id})

@app.route("/license-plates", methods=["POST"])
def create_license_plate():
    license_plate = request.json["license_plate"]
    camera_id = request.json["camera_id"]
    camera = Camera.query.get(camera_id)
    if camera is None:
        return jsonify({"error": "Camera not found"}), 404
    license_plate = LicensePlate(license_plate=license_plate, camera=camera)
    db.session.add(license_plate)
    db.session.commit()
    return jsonify({"id": license_plate.id, "license_plate": license_plate.license_plate, "camera_id": license_plate.camera_id})

@app.route("/handicap-status", methods=["POST"])
def create_handicap_status():
    license_plate_id = request.json["license_plate_id"]
    is_handicapped = request.json["is_handicapped"]
    license_plate = LicensePlate.query.get(license_plate_id)
    if license_plate is None:
        return jsonify({"error": "License plate not found"}), 404
    handicap_status = HandicapStatus(license_plate=license_plate, is_handicapped=is_handicapped)
    db.session.add(handicap_status)
    db.session.commit()
    return jsonify({"id": handicap_status.id, "license_plate_id": handicap_status.license_plate_id, "is_handicapped": handicap_status.is_handicapped})

@app.route("/license-plates/<string:license_plate>", methods=["GET"])
def get_license_plate(license_plate):
    license_plate = LicensePlate.query.filter_by(license_plate=license_plate).first()
    if license_plate is None:
        return jsonify({"error": "License plate not found"}), 404
    handicap_status = license_plate.handicap_status
    return jsonify({"id": license_plate.id, "license_plate": license_plate.license_plate, "camera_id": license_plate.camera_id, "is_handicapped": handicap_status.is_handicapped})

if __name__ == "__main__":
    app.run(debug=True)