from flask import Blueprint, render_template, request, session, redirect, url_for, current_app

auth = Blueprint('authStaff', __name__)

#Authenticates the login of Staff
@auth.route('/loginAuthAirlineStaff', methods=['GET', 'POST'])
def loginAuthStaff():
	#grabs information from the forms
    username = request.form['username']
    password = request.form['password']

	#cursor used to send queries
    cursor = current_app.config['db'].cursor()
	#executes query
    query = 'SELECT * FROM Airline_Staff WHERE username = %s and password = md5(%s)' #md5 to hash password
    cursor.execute(query, (username, password))
	#stores the results in a variable
    data = cursor.fetchone()
    cursor.close()
    
    error = None
    if(data):
		#creates a session for the the user
        session['username'] = username
        session['usertype'] = "staff"

        cursor = current_app.config['db'].cursor()
        query = 'SELECT Airline_name FROM Airline_Staff WHERE username = %s'
        cursor.execute(query, (username))
        airline = cursor.fetchone()
        cursor.close()

        session['airline'] = airline['Airline_name']

        return redirect(url_for('main.home'))
    else:
		#returns an error message to the html page
        error = 'Invalid login or username'
        return render_template('login.html', error=error)

#Authenticates the register of Staff
@auth.route('/registerAuthAirlineStaff', methods=['GET', 'POST'])
def registerAuthStaff():
    print(request.form)
    #grabs information from the forms
    username = request.form['username']
    password = request.form['password']
    f_name = request.form['f_name']
    l_name = request.form['l_name']
    date_of_birth = request.form['date_of_birth']
    phone_nums = request.form.getlist('phone[]')
    email_add = request.form.getlist('email[]')
    airline_name = request.form['airline_name']


    phone_set = set(phone_nums)
    email_set = set(email_add)

    phones = list(phone_set)
    emails = list(email_set)

    # Format the date to YYYY-MM-DD if it's in MM-DD-YYYY format
    try:
        if '-' in date_of_birth:
            parts = date_of_birth.split('-')
            if len(parts[0]) == 2:  # If first part is MM
                date_of_birth = f"{parts[2]}-{parts[0]}-{parts[1]}"
    except:
        pass

    #cursor used to send queries
    cursor = current_app.config['db'].cursor()
    #executes query
    query = "SELECT * FROM Airline_Staff WHERE username = %s"
    cursor.execute(query, (username,))  # Add comma to make it a tuple
    #stores the results in a variable
    data = cursor.fetchone()
    #use fetchall() if you are expecting more than 1 data row
    error = None
    if(data):
        #If the previous query returns data, then user exists
        error = "This user already exists"
        return render_template('register.html', error = error)
    else:
        ins = 'INSERT INTO Airline_Staff VALUES(%s, md5(%s),%s,%s,%s,%s)'  #added md5 to hash password
        cursor.execute(ins, (username, password, f_name, l_name, date_of_birth, airline_name))

        for phone in phones:
            query1 = 'INSERT INTO Phone_num VALUES(%s, %s)'
            cursor.execute(query1, (username, phone))
        
        for email in emails:
            query2 = 'INSERT INTO Email VALUES(%s, %s)' 
            cursor.execute(query2, (username, email))
        
        current_app.config['db'].commit()
        cursor.close()
        return render_template('index.html')
