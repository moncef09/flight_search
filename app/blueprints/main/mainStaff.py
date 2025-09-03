from flask import Blueprint, render_template, request, session, redirect, url_for, current_app
from .main import protected_staff

main = Blueprint('mainStaff', __name__)

@main.route('/home_staff', methods = ['GET','POST'])
@protected_staff
def home_staff():
    username = session['username']

    cursor = current_app.config['db'].cursor();
    query = 'SELECT f_name, Airline_name FROM Airline_Staff WHERE username = %s'
    cursor.execute(query, (username))
    data1 = cursor.fetchall() 
    
    for each in data1:
        name = each['f_name']
    
    cursor.close()
    return render_template('staff/home_airlineStaff.html', username=name, posts=data1)

@main.route('/home_airlineStaff_view', methods = ['GET','POST'])
@protected_staff
def home_staff_view():
    if 'username' in session:
        username = session['username']
        airline = session['airline']

        cursor = current_app.config['db'].cursor()

        query_future_flights = """
            SELECT flight_no, departure_date_and_time, arrival_date_and_time, 
                   departure_airport_id, arrival_airport_id, status, base_price, Airplane_airline_name, Airplane_id
            FROM Flight
            WHERE Airline_Name = %s AND departure_date_and_time BETWEEN NOW() AND DATE_ADD(NOW(), INTERVAL 30 DAY)
            ORDER BY departure_date_and_time ASC
        """

        cursor.execute(query_future_flights, (airline,))
        future_flights = cursor.fetchall()
        cursor.close()

        if 'data' in session:
            data = session['data']
            if len(data) > 0:
                filters = session['search_filters']
                return render_template('staff/home_airlineStaff_view.html',username=username, flights=data, filters=filters)
            else:
                return render_template('staff/home_airlineStaff_view.html',username=username, error='No Flights Found!')
        else:
            return render_template('staff/home_airlineStaff_view.html',username=username,future_flights=future_flights)
    else:
        return render_template('staff/home_airlineStaff_view.html',error='No Session')

@main.route('/home_airlineStaff_create', methods = ['GET','POST'])
@protected_staff
def home_staff_create():
    if 'username' not in session:
        return redirect(url_for('login'))

    cursor = current_app.config['db'].cursor()
    airline = session['airline']

    try:
        query_future_flights = """
            SELECT flight_no, departure_date_and_time, arrival_date_and_time, 
                   departure_airport_id, arrival_airport_id, status
            FROM Flight
            WHERE Airline_Name = %s AND departure_date_and_time BETWEEN NOW() AND DATE_ADD(NOW(), INTERVAL 30 DAY)
            ORDER BY departure_date_and_time ASC
        """
        cursor.execute(query_future_flights, (airline,))
        future_flights = cursor.fetchall()

        return render_template(
            'staff/home_airlineStaff_create.html',
            username=session['username'],
            usertype=session['usertype'],
            airline=airline,
            future_flights=future_flights
        )
    except Exception as e:
        error = f"An error occurred while retrieving future flights: {e}"
        return render_template(
            'staff/home_airlineStaff_create.html',
            username=session['username'],
            usertype=session['usertype'],
            airline=session['airline'],
            error=error
        )
    finally:
        cursor.close()

@main.route('/home_airlineStaff_airport', methods = ['GET','POST'])
@protected_staff
def home_staff_airport():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        airport_id = request.form.get('Airport_id')
        name = request.form.get('name')
        city = request.form.get('city')
        country = request.form.get('country')
        if not airport_id or not name or not city or not country:
            error = "All fields are required."
            return render_template('staff/home_airlineStaff_airport.html', username=session['username'], error=error)
        cursor = current_app.config['db'].cursor()
        query_check = 'SELECT * FROM Airport WHERE airport_id = %s'
        cursor.execute(query_check, (airport_id,))
        existing_airport = cursor.fetchone()
        if existing_airport:
            error = "Airport ID already exists."
            return render_template('staff/home_airlineStaff_airport.html', username=session['username'], error=error)
        query_insert = """
            INSERT INTO Airport (airport_id, name, city, country)
            VALUES (%s, %s, %s, %s)
        """
        try:
            cursor.execute(query_insert, (airport_id, name, city, country))
            current_app.config['db'].commit()
            success = "Airport added successfully!"
            return render_template('staff/home_airlineStaff_airport.html', username=session['username'], success=success)
        except Exception as e:
            current_app.config['db'].rollback()
            error = f"Database error: {e}"
            return render_template('staff/home_airlineStaff_airport.html', username=session['username'], error=error)
        finally:
            cursor.close()
    else:
        return render_template('staff/home_airlineStaff_airport.html', username=session['username'])

@main.route('/home_airlineStaff_airplane', methods = ['GET','POST'])
@protected_staff
def home_staff_airplane():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        airline_name = request.form.get('Airline_name')
        airplane_id = request.form.get('id')
        num_seats = request.form.get('num_seats')
        manufacturing_co = request.form.get('manufacturing_co')
        
        if not airline_name or not airplane_id or not num_seats or not manufacturing_co:
            error = "All fields are required."
            return render_template('staff/home_airlineStaff_airplane.html', username=session['username'], error=error)
        
        cursor = current_app.config['db'].cursor()
        
        try:
            query_check = 'SELECT * FROM Airplane WHERE id = %s'
            cursor.execute(query_check, (airplane_id,))
            existing_airplane = cursor.fetchone()
            if existing_airplane:
                error = "Airplane ID already exists."
                return render_template('staff/home_airlineStaff_airplane.html', username=session['username'], error=error)
            query_insert = """
                INSERT INTO Airplane (id, Airline_name, num_seats, manufacturing_co)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query_insert, (airplane_id, airline_name, num_seats, manufacturing_co))
            current_app.config['db'].commit()

            query_all_planes = 'SELECT * FROM Airplane WHERE Airline_name = %s'
            cursor.execute(query_all_planes, (airline_name,))
            airplanes = cursor.fetchall()

            success = "Airplane added successfully!"
            return render_template('staff/home_airlineStaff_airplane.html', username=session['username'], success=success, airplanes=airplanes)
        except Exception as e:
            current_app.config['db'].rollback()
            error = f"Database error: {e}"
            return render_template('staff/home_airlineStaff_airplane.html', username=session['username'], error=error)
        finally:
            cursor.close()
    else:
        return render_template('staff/home_airlineStaff_airplane.html', username=session['username'])

@main.route('/home_airlineStaff_change', methods = ['GET','POST'])
@protected_staff
def home_staff_change():
    username = session['username']
    airline = session['airline']

    success = False #default value
    if 'success' in session:
        success = session['success']
        session.pop('success')

    cursor = current_app.config['db'].cursor();
    query = 'SELECT flight_no,departure_date_and_time,departure_airport_id,arrival_airport_id,arrival_date_and_time,status \
          FROM Flight WHERE Airline_Name = %s AND departure_date_and_time >= NOW()'
    cursor.execute(query, (airline))
    data1 = cursor.fetchall()
    # print("dad",data1)
    cursor.close()
    return render_template('staff/home_airlineStaff_change.html',username=username,flights = data1, success=success)

@main.route('/home_airlineStaff_rating', methods = ['GET','POST'])
@protected_staff
def home_staff_rating():

    if 'username' not in session:
        return redirect(url_for('login'))

    cursor = current_app.config['db'].cursor()
    airline = session['airline']

    try:
        query_avg_ratings = """
            SELECT flight_no, departure_date_and_time, AVG(rate) AS avg_rating
            FROM Review
            WHERE Airline_Name = %s
            GROUP BY flight_no, departure_date_and_time
            ORDER BY avg_rating DESC
        """
        cursor.execute(query_avg_ratings, (airline,))
        avg_ratings = cursor.fetchall()

        query_reviews = """
            SELECT flight_no, departure_date_and_time, email, rate, comment
            FROM Review
            WHERE Airline_Name = %s
            ORDER BY flight_no, departure_date_and_time, rate DESC
        """
        cursor.execute(query_reviews, (airline,))
        reviews = cursor.fetchall()

        return render_template(
            'staff/home_airlineStaff_rating.html',
            username=session['username'],
            avg_ratings=avg_ratings,
            reviews=reviews
        )

    except Exception as e:
        error = f"An error occurred while retrieving ratings: {e}"
        return render_template('staff/home_airlineStaff_rating.html', username=session['username'], error=error)

    finally:
        cursor.close()

@main.route('/home_airlineStaff_report', methods = ['GET','POST'])
@protected_staff
def home_staff_report():
    if 'username' not in session:
        return redirect(url_for('login'))

    cursor = current_app.config['db'].cursor()
    airline = session['airline']

    try:
        start_date = '1900-01-01'
        end_date = '2100-01-01'

        if request.method == 'POST':
            start_date = request.form.get('start_date') or start_date
            end_date = request.form.get('end_date') or end_date

        query_total_sales = """
            SELECT COUNT(*) AS total_tickets
            FROM Purchases
            JOIN Ticket ON Purchases.ticket_id = Ticket.ticket_id
            WHERE Ticket.Airline_Name = %s
            AND date_and_time BETWEEN %s AND %s
        """
        cursor.execute(query_total_sales, (airline, start_date, end_date))
        total_sales = cursor.fetchone()

        query_monthly_sales = """
            SELECT DATE_FORMAT(date_and_time, '%%Y-%%m') AS month, COUNT(*) AS tickets_sold
            FROM Purchases
            JOIN Ticket ON Purchases.ticket_id = Ticket.ticket_id
            WHERE Ticket.Airline_Name = %s
            GROUP BY month
            ORDER BY month
        """
        cursor.execute(query_monthly_sales, (airline,))
        monthly_sales = cursor.fetchall()

        return render_template(
            'staff/home_airlineStaff_report.html',
            username=session['username'],
            total_sales=total_sales,
            monthly_sales=monthly_sales,
            start_date=start_date,
            end_date=end_date
        )

    except Exception as e:
        error = f"An error occurred while retrieving reports: {e}"
        return render_template('staff/home_airlineStaff_report.html', username=session['username'], error=error)

    finally:
        cursor.close()


@main.route('/searchFlightCustomers', methods = ['GET','POST'])
@protected_staff
def search_flight_customers():
    username = session['username']
    if 'data' in session:
        data = session.pop('data')
        if len(data) > 0:
            filters = session.pop('filters')
            return render_template('staff/home_airlineStaff_flightCust.html',username=username, flights=data, filters=filters)
        else:
            return render_template('staff/home_airlineStaff_flightCust.html',username=username, error='Error: There are either no customers or you have entered an invalid flight!')
    else:
        return render_template('staff/home_airlineStaff_flightCust.html',username=username)