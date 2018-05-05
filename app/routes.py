from flask import jsonify, request
from app import app, db
from app.models import Doctor, Review
from sqlalchemy.exc import ProgrammingError, IntegrityError


@app.route('/doctors', methods=["POST", "GET"])
def add_or_get_doctor():
    """
    POST: Add a doctor to the database given the name
    GET: List all doctors and their reviews
    :return: a json object of the post or get request
    """
    if request.method == "POST":
        try:
            # Create a doctor obj by accessing the json found in the request
            name = request.json['doctor']['name']
            new_doctor = Doctor(name=name)

            doctor_dict = dict()
            doctor_dict['id'] = new_doctor.id
            doctor_dict['name'] = new_doctor.name

            # Add the doctor and commit it to the database
            db.session.add(new_doctor)
            db.session.commit()

            return jsonify({'Added': doctor_dict})

        except ProgrammingError:
            return 'Tried Posting information when the db was no created'

    elif request.method == "GET":
        try:
            # List all the doctors
            results = dict()
            # all doctors
            all_doctors = Doctor.query.all()
            for doctor in all_doctors:
                doctor_dict = dict()
                doctor_dict['name'] = doctor.name
                doctor_dict['id'] = doctor.id
                doctor_dict['reviews'] = []
                results[doctor.id] = doctor_dict

            # all reviews
            all_reviews = Review.query.all()
            for review in all_reviews:
                review_dict = dict()
                review_dict['id'] = review.id
                review_dict['doctor_id'] = review.doctor_id
                review_dict['description'] = review.description

                for doctor_json in results:
                    if review.doctor_id == results[doctor_json]['id']:
                        results[doctor_json]['reviews'].append(review_dict)

            return jsonify(results)

        except ProgrammingError:
            return 'Error: Tried retrieving information when the db was not created'


@app.route('/doctors/<did>/reviews', methods=["POST", "GET"])
def add_review_to_doctor(did):
    """
    POST: Add a review to an existing doctor with a certain id
    GET: Retrieve all the reviews for a doctor
    :param did: The doctor id used
    :return: a json object of the post or get request
    """
    if request.method == "POST":
        try:
            # Check if doctor exist
            Doctor.query.get(did)
            description = request.json['review']['description']
            review = Review(doctor_id=did, description=description)

            db.session.add(review)
            db.session.commit()

            review_dict = dict()
            review_dict['id'] = review.id
            review_dict['did'] = review.doctor_id
            review_dict['description'] = review.description

            # Try to return a success message instead
            return jsonify(review_dict)

        except IntegrityError:
            return 'Error: Tried adding a review to a doctor that does not exist'

    elif request.method == "GET":
        if Doctor.query.get(did) is not None:
            results = dict()
            all_review = Review.query.filter_by(doctor_id=did).all()
            for review in all_review:
                review_dict = dict()
                review_dict['id'] = review.id
                review_dict['doctor_id'] = review.doctor_id
                review_dict['description'] = review.description
                results[review.id] = review_dict

            return jsonify(results)

        else:
            return 'No reviews were found fod this doctor, or doctor does not exist'


@app.route('/doctors/<did>/reviews/<rid>', methods=["DELETE", "GET"])
def delete_or_get_review_from_doctor(did, rid):
    """
    DELETE: Delete a certain review from a given doctor
    GET:  Retrieve a certain review from a given doctor
    :param did: doctor id
    :param rid: review id
    :return: a json object of the post or get request
    """
    if request.method == "DELETE":
        results = dict()

        review = Review.query.get(rid)
        doctor = Doctor.query.get(did)
        if review is not None and doctor is not None:
            review_dict = dict()
            review_dict['id'] = review.id
            review_dict['did'] = review.doctor_id
            review_dict['description'] = review.description

            results['Deleted Review'] = review_dict

            db.session.delete(review)
            db.session.commit()

            return jsonify(results)
        else:
            return 'Review does not exist'

    elif request.method == "GET":
        doctor = Doctor.query.get(did)
        if doctor is not None:
            doctor_dict = dict()
            doctor_dict['id'] = doctor.id
            doctor_dict['name'] = doctor.name
        else:
            return 'Doctor does not exist'

        review = Review.query.get(rid)
        if review is not None:
            review_dict = dict()
            review_dict['id'] = review.id
            review_dict['did'] = review.doctor_id
            review_dict['description'] = review.description
            review_dict['doctor'] = doctor_dict

            return jsonify(review_dict)
        else:
            return 'Review does not exist'


@app.route('/doctors/<did>', methods=["GET", "DELETE"])
def get_or_delete_doctor(did):
    """
    GET: Retrieve a doctor with the given id
    DELETE: Delete a doctor with the given id
    :param did: doctor id
    :return: json object of post or get request
    """
    if request.method == "GET":
        # Retrieve doctor with did
        doctor = Doctor.query.get(did)
        if doctor is not None:
            doctor_dict = dict()
            doctor_dict['name'] = doctor.name
            doctor_dict['id'] = doctor.id
            doctor_dict['reviews'] = []

            all_review = Review.query.filter_by(doctor_id=did).all()
            for review in all_review:
                review_dict = dict()
                review_dict['id'] = review.id
                review_dict['doctor_id'] = review.doctor_id
                review_dict['description'] = review.description
                doctor_dict['reviews'].append(review_dict)

            return jsonify(doctor_dict)

        else:
            return 'Tried to retrieve a doctor that does not exist'

    elif request.method == "DELETE":
        doctor = Doctor.query.get(did)
        if doctor is not None:
            doctor_dict = dict()
            doctor_dict['name'] = doctor.name
            doctor_dict['id'] = doctor.id

            db.session.delete(doctor)
            db.session.commit()

            delete_did = dict()
            delete_did['Deleted'] = doctor_dict

            return jsonify(delete_did)

        else:
            return 'Tried to delete a doctor that does not exist'
