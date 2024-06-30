from db import Db
from flask import Flask, jsonify, request
from models import User


db = Db()
# Create a cursor object to execute SQL queries
cursor = db.cursor

#init app
app = Flask("app")

# Define a route to get data from the database

@app.route('/login',methods=['POST'])
def login():
    temp = User()
    temp.email, temp.password = request.form['email'],request.form['password']
    if db.login(temp):
        user = db.get_user_by_email(temp.email).totuple()
        return jsonify({'message': 'Login successful','user': user})
    else:
        return jsonify({'message': 'Invalid username or password'})

@app.route('/register',methods=['POST'])
def register():
    temp = User()
    temp.insert(request.form['email'],request.form['password'],request.form['firstname'],request.form['Last_name'])
    if db.insert_user(temp):
        return jsonify({'message': 'register successful'})
    else:
        return jsonify({'message': 'register not successful'})

@app.route('/user',methods=['POST'])
def user():
    id = request.form['id']
    user = db.get_user_by_id(int(id))
    if user:
        return jsonify({'message': 'register successful', 'user': user.totuple()})
    else:
        return jsonify({'message': 'register not successful'})

@app.route('/changeType',methods =['POST'])
def change_type():
    email, type = request.form['email'], request.form['type']
    flag = db.change_type_of_user(email, type)
    if flag:
        return jsonify({'message': 'change successful'})
    else:
        return jsonify({'message': 'change not successful'})

@app.route('/changePassword',methods=['POST'])
def change_Password():
    email,temp_password, new_password = request.form['email'],request.form['temp_password'], request.form['new_password']
    flag = db.change_password(email,temp_password,new_password)
    if flag:
        return jsonify({'message': 'change successful'})
    else:
        return jsonify({'message': 'change not successful'})

@app.route('/getAllUsers',methods=['GET'])
def get_all_users():
    users = db.print_user_table()
    return jsonify({'message': 'change successful','users':users})

@app.route('/changeInfo',methods=['POST'])
def change_info():
    if db.update_info(request.form['email'],request.form['name'],request.form['lastname']):
        return jsonify({'message': 'change successful'})
    else:
        return jsonify({'message': 'change not successful'})

@app.route('/getUsersTypes',methods=['GET'])
def get_users_types():
    tupple_lst = db.get_users_types()
    return jsonify({'message': 'change successful', 'users': tupple_lst})

@app.route('/removeUser',methods = ['POST'])
def delete_user_email():
    if db.delete_user_by_email(request.form['email']):
        return jsonify({'message': 'change successful'})
    else:
        return jsonify({'message': 'change not successful'})

@app.route('/getAllSupply',methods = ['GET'])
def get_all_supply():
    supply = db.get_all_supply()
    return jsonify({'message': 'successful', 'supply': supply})

@app.route('/getAllBorrows',methods = ['GET'])
def get_all_borrows():
    borrows = db.get_all_borrows()
    return jsonify({'message': 'successful', 'borrows': borrows})

@app.route('/borrowItem',methods = ['POST'])
def borrow_item():
    print(request.form['return_time'])
    if db.borrow_item(request.form['user_id'], request.form['item_id'],
                      request.form['return_time'], request.form['num_of_items'], request.form['num_of_items_remain']):
        return jsonify({'message': 'change successful'})
    return jsonify({'message': 'change not successful'})

@app.route('/returnAllItems',methods = ['POST'])
def return_all_items():
    if db.return_all_items(request.form['user_id']):
        return jsonify({'message': 'change successful'})
    return jsonify({'message': 'change not successful'})

@app.route('/returnSomeItem',methods = ['POST'])
def return_some_items():
    if db.return_item(request.form['user_id'],request.form['item_id'],int(request.form['num_of_items'])):
        return jsonify({'message': 'change successful'})
    return jsonify({'message': 'change not successful'})

@app.route('/generateTempPassword',methods = ['POST'])
def generate_temp_password():
    if db.generate_temp_password(request.form['email']):
        return jsonify({'message': 'change successful'})
    return jsonify({'message': 'change not successful'})

@app.route('/getBorrowedItems',methods = ['POST'])
def get_my_borrowed_items():
    items = db.get_items_dosent_return(request.form['user_id'])
    return jsonify({'message': 'successful', 'items': items})

@app.route('/addItemToSupply',methods = ['POST'])
def add_item_to_supply():
    item_id = db.add_item_to_supply(request.form['name'],request.form['units'],request.form['type'],request.form['description'])
    if item_id:
        return jsonify({'message': 'change successful','id':item_id})
    return jsonify({'message': 'change not successful'})
@app.route('/plot_borrow',methods = ['GET'])
def plot_borrow():
    borrow_data, num_of_items = db.plot_borrow()
    print(borrow_data)
    print(num_of_items)
    return jsonify({'borrow_data':borrow_data,'num_of_items':num_of_items})

@app.route('/reportItem',methods = ['POST'])
def report_item():
    if db.report_problem_item(request.form['user_id'],request.form['id'],request.form['des'],request.form['units']):
        return jsonify({'message': 'change successful'})
    return jsonify({'message': 'change not successful'})

if __name__ == '__main__':
    app.run(debug=True)