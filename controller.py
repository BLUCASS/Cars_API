from flask import Flask, jsonify, make_response, request
from model import engine, Vehicle
from sqlalchemy.orm import sessionmaker


# CREATING THE APP
app = Flask(__name__)

# CREATING THE SESSION FOR THE DATABASE
Session = sessionmaker(bind=engine)
session = Session()


# CREATING THE ROUTES FOR THE APP
@app.route('/', methods=['GET'])
def home() -> str:
    """This function will only show to the users that they are on the main page"""
    return make_response("YOU ARE ON THE MAIN PAGE!")


@app.route("/cars/add", methods=['POST'])
def add_car() -> str:
    """It receives a car, input from the user and try to insert it into the db.
    Whether it was successfully or not, the user will read the messsage."""
    data = request.json
    db_management = DbManagement()
    if db_management.add_car_into_db(data):
        return make_response(f"{data['name'].upper()} ADDED SUCCESFULLY")
    return make_response(f"CAR NOT ADDED")

@app.route('/cars/remove', methods=['POST'])
def remove_car() -> str:
    """It receives an ID from the user, and try to delete it from the db."""
    data = request.json
    if DbManagement().remove_car(data):
        return make_response("CAR REMOVED")
    return make_response("CAR NOT REMOVED")

@app.route('/cars/show', methods=['GET'])
def show_cars() -> str:
    """It will return a list with all the cars inserted into the database."""
    cars = DbManagement().show_cars()
    if cars != False:
        return make_response(jsonify(cars))
    return make_response("YOU DO NOT HAVE CARS TO SHOW")


class DbManagement:
    """This class will exclusively deal with the database"""
    def add_car_into_db(self, data) -> bool:
        """This function receives a car and insert it into the database"""
        vehicle = Vehicle(brand=data["brand"],
                        name=data["name"],
                        year=data["year"])
        try:
            session.add(vehicle)
        except:
            session.rollback()
            session.close()
            return False
        else:
            session.commit()
            session.close()
            return True
    
    def remove_car(self, id) -> bool:
        """This function removes a car from the database, receiving its id
        as a parameter."""
        try:
            data = session.query(Vehicle).filter(Vehicle.id == id).first()
            session.delete(data)
        except:
            session.rollback()
            session.close()
            return False
        else:
            session.commit()
            session.close()
            return True

    def show_cars(self) -> list:
        """This function queries the database and return it."""
        try:
            data = session.query(Vehicle).all()
            if len(data) == 0:
                raise ValueError
            new_list = []
            [new_list.append({"id": car.id,
                             "name": car.name,
                             "brand": car.brand,
                             "year": car.year}) for car in data]
            return new_list
        except:
            session.rollback()
            return False


# RUNNING THE APP
if __name__ == '__main__':
    app.run(debug=True)