from flask import Blueprint, render_template, request, session, redirect, url_for, current_app

auth = Blueprint('auth', __name__)

#Define route for login
@auth.route('/login')
def login():
    return render_template('login.html')

#Define route for register
@auth.route('/register')
def register():
    return render_template('register.html')

@auth.route('/register_customer')
def register_customer():
    return render_template('register_customer.html')

@auth.route('/register_staff')
def register_staff():
    return render_template('register_staff.html')
