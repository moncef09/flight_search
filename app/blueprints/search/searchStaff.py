from flask import Blueprint, render_template, request, session, redirect, url_for, current_app

search = Blueprint('searchStaff', __name__)

@search.route('/searchFlightsStaff', methods = ['GET','POST'])
def search_staff():
    #grabs information from the forms
    username = session['username']
    airline = session['airline']
	
    start_date = request.form['start_date']
    end_date = request.form['end_date']
    source = request.form['source']
    destination = request.form['destination']
    status = request.form['status']
	
    cursor = current_app.config['db'].cursor()
    query = "Select Airline_Name AS Airline,\
         flight_no AS Flight, \
            departure_date_and_time AS Departure_Date, \
         departure_airport_id AS Departure, \
             arrival_airport_id AS Arrival, \
                arrival_date_and_time AS Arrival_Date, \
                     status, base_price, \
                         Airplane_airline_name AS AA_name, \
                             Airplane_id FROM Flight WHERE Airline_Name = %s"
	
    params = [airline]
    filters = ["No Filters"]
        
    if start_date:
        query += " AND departure_date_and_time >= %s"
        params.append(start_date)
        filters.append('From ' + start_date)

    if end_date:
        query += " AND departure_date_and_time <= %s"
        params.append(end_date)
        filters.append('To ' + end_date)

    if source:
        query += " AND departure_airport_id = %s"
        params.append(source)
        filters.append('Departure: ' + source)

    if destination:
        query += " AND arrival_airport_id = %s"
        params.append(destination)
        filters.append('Arrival: ' + destination)

    if status:
        query += " AND `status` = %s"
        params.append(status)
        filters.append('Status: ' + status)
    # query = 'SELECT * FROM Flight WHERE departure_airport_id =%s AND Airline_Name \
	# 	= (SELECT Airline_name FROM Airline_Staff WHERE username=%s)'
    
    if not len(filters) == 1:
        filters = filters[1:]

    cursor.execute(query, params)
    data = cursor.fetchall()
    cursor.close()
    error = None
	
    if('username' in session):
		#creates a session for the the user
		#session is a built in
        session['data'] = data
        session['search_filters'] = filters
        return redirect(url_for('mainStaff.home_staff_view'))
    else:
		#returns an error message to the html page
        error = 'Invalid login or username'
        return render_template('login.html', error=error)
    
@search.route('/editFiltersStaff', methods = ['GET','POST'])
def edit_filter_staff():
    session.pop('data')
    return redirect(url_for('mainStaff.home_staff_view'))

@search.route('/createFlightsStaff', methods = ['GET','POST'])
def create_flights_staff():
    username = session['username']
    airline = session['airline']

    flight_no = request.form['flight_no']
    dep_date = request.form['dep_date']
    dep_time = request.form['dep_time']
    dep_airport = request.form['dep_airport']
    arr_date = request.form['arr_date']
    arr_time = request.form['arr_time']
    arr_airport = request.form['arr_airport']
    status = request.form['status']
    base_price = request.form['base_price']
    # AA_name = request.form['AA_name']
    AA_id = request.form['AA_id']

    dep_date_time = f"{dep_date} {dep_time}:00"
    arr_date_time = f"{arr_date} {arr_time}:00"


    cursor = current_app.config['db'].cursor()
    # query = "INSERT INTO FLIGHT VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    query = """
    INSERT INTO FLIGHT
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
        departure_airport_id = %s,
        arrival_airport_id = %s,
        arrival_date_and_time = %s,
        status = %s,
        base_price = %s,
        Airplane_airline_name = %s,
        Airplane_id = %s
    """
    cursor.execute(query, (airline, flight_no,dep_date_time,dep_airport,arr_airport, arr_date_time ,status,base_price,airline,AA_id, \
                           dep_airport,arr_airport,arr_date_time,status,base_price,airline,AA_id
                           ))
    current_app.config['db'].commit()
    cursor.close()
    return redirect(url_for('mainStaff.home_staff_create'))

@search.route('/changeFlightStatus', methods = ['GET','POST'])
def change_flight_staff():
    for key in request.form:
        if key.startswith('status_'):
            new_status = request.form[key] 
            keys = key.split('_')
            print(key, new_status)
            cursor = current_app.config['db'].cursor()
            query = "UPDATE Flight SET status = %s WHERE flight_no = %s AND departure_date_and_time = %s"
            cursor.execute(query,(new_status,keys[1],keys[2]))
            current_app.config['db'].commit()
            cursor.close()
    session['success'] = True
    return redirect(url_for('mainStaff.home_staff_change'))

@search.route('/searchCustomerFlights', methods = ['GET','POST'])
def search_cust_flights():
    airline = session['airline']
    flight_no = request.form['flight_no']
    dep_date = request.form['dep_date']
    dep_time = request.form['dep_time']

    dep_date_time = f"{dep_date} {dep_time}:00"

    cursor = current_app.config['db'].cursor()
    query = """SELECT c.name, c.passport_number
        FROM Ticket t
        JOIN Purchases p ON t.ticket_id = p.ticket_id
        JOIN Customer c ON p.email = c.email
        WHERE t.Airline_name = %s AND t.flight_no = %s AND t.departure_date_and_time = %s;
        """
    cursor.execute(query, (airline, flight_no, dep_date_time))
    data = cursor.fetchall()
    cursor.close()

    filters = ["Flight " + flight_no + " at " + dep_date_time]
    
    session['data'] = data
    session['filters'] = filters

    return redirect(url_for('mainStaff.search_flight_customers'))
