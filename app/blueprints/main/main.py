from flask import Blueprint, render_template, request, session, redirect, url_for, current_app
from functools import wraps

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/home')
def home():
    # redirect the home page to home_customer or home_staff
    usertype = session['usertype']
    if usertype == 'customer':
        return redirect(url_for('mainCust.home_cust'))
    elif usertype == 'staff':
        return redirect(url_for('mainStaff.home_staff'))

@main.route('/logout')
def logout():
    if 'data' in session:
        session.pop('data')
    if 'airline' in session:
        session.pop('airline')
    
    session.pop('username')
    session.pop('usertype')
    return render_template('logout.html')

def protected_cust(route):
    @wraps(route)
    def wrapper(*args, **kwargs):
        if session.get('usertype') == "customer" and session.get('username'):
            return route(*args, **kwargs)
        else:
            return render_template('unauthorized.html')
    return wrapper

def protected_staff(route):
    @wraps(route)
    def wrapper(*args, **kwargs):
        if session.get('usertype') == "staff" and session.get('username'):
            return route(*args, **kwargs)
        else:
            return render_template('unauthorized.html')
    return wrapper

@main.route('/search_flights', methods=['GET', 'POST'])
def search_flights():
    if request.method == 'POST':
        # Get search parameters
        source = request.form['source']
        destination = request.form['destination']
        departure_date = request.form['departure_date']
        is_round_trip = 'return_date' in request.form
        return_date = request.form.get('return_date', None)
        
        # Connect to the database
        cursor = current_app.config['db'].cursor()
        
        # Search query for departure flights
        query = '''
        SELECT f.Airline_Name, f.flight_no, f.departure_date_and_time, f.arrival_date_and_time, 
               a1.name as departure_airport, a2.name as arrival_airport, 
               a1.city as departure_city, a2.city as arrival_city, f.base_price, f.status
        FROM Flight f 
        JOIN Airport a1 ON f.departure_airport_id = a1.Airport_id
        JOIN Airport a2 ON f.arrival_airport_id = a2.Airport_id
        WHERE (a1.city = %s OR a1.name = %s OR a1.Airport_id = %s) 
        AND (a2.city = %s OR a2.name = %s OR a2.Airport_id = %s)
        AND DATE(f.departure_date_and_time) = %s
        '''
        
        cursor.execute(query, (source, source, source, destination, destination, destination, departure_date))
        departure_flights = cursor.fetchall()
        
        # Handle round trip search
        return_flights = []
        if is_round_trip and return_date:
            query = '''
            SELECT f.Airline_Name, f.flight_no, f.departure_date_and_time, f.arrival_date_and_time, 
                   a1.name as departure_airport, a2.name as arrival_airport, 
                   a1.city as departure_city, a2.city as arrival_city, f.base_price, f.status
            FROM Flight f 
            JOIN Airport a1 ON f.departure_airport_id = a1.Airport_id
            JOIN Airport a2 ON f.arrival_airport_id = a2.Airport_id
            WHERE (a1.city = %s OR a1.name = %s OR a1.Airport_id = %s) 
            AND (a2.city = %s OR a2.name = %s OR a2.Airport_id = %s)
            AND DATE(f.departure_date_and_time) = %s
            '''
            
            cursor.execute(query, (destination, destination, destination, source, source, source, return_date))
            return_flights = cursor.fetchall()
            
        cursor.close()
        
        return render_template('search_results.html', 
                              departure_flights=departure_flights, 
                              return_flights=return_flights, 
                              is_round_trip=is_round_trip)
    
    return render_template('search_flights.html')
