from flask import Blueprint, render_template, request, session, redirect, url_for, current_app, flash
from datetime import datetime, timedelta
from .main import protected_cust

main = Blueprint('mainCust', __name__)

@main.route('/home_customer', methods = ['GET','POST'])
@protected_cust
def home_cust():
    username = session['username']

    cursor = current_app.config['db'].cursor();
    query = 'SELECT name FROM Customer WHERE email = %s'
    cursor.execute(query, username)  
    data = cursor.fetchone() 
    
    cursor.close()
    return render_template('customer/home_customer.html', username=data['name'], posts=data)




@main.route('/home_customer_search', methods = ['GET','POST'])
@protected_cust
def home_cust_search():
    return render_template('customer/home_customer_search.html', username=session['username'])

@main.route('/customer_search_flights', methods = ['POST'])
@protected_cust
def customer_search_flights():
    # Get search parameters from form
    source = request.form.get('source', '')
    destination = request.form.get('destination', '')
    departure_date = request.form.get('departure_date', '')
    return_date = request.form.get('return_date', '')
    
    # Debug log to verify form data
    print(f"Search params - Source: {source}, Destination: {destination}, Departure: {departure_date}, Return: {return_date}")
    
    # Validate form inputs
    if not source or not destination or not departure_date:
        return render_template('customer/home_customer_search.html', 
                             username=session['username'],
                             error="All search fields are required except return date")
    
    # Cursor for database queries
    cursor = current_app.config['db'].cursor()
    
    # Check if airports/cities exist
    check_query = '''
    SELECT COUNT(*) as count FROM Airport 
    WHERE Airport_id = %s OR city = %s OR name = %s
    '''
    cursor.execute(check_query, (source, source,source))
    source_exists = cursor.fetchone()['count'] > 0
    
    cursor.execute(check_query, (destination, destination,destination))
    destination_exists = cursor.fetchone()['count'] > 0
    
    if not source_exists:
        return render_template('customer/home_customer_search.html', 
                             username=session['username'],
                             error="Departure airport or city not found")
    
    if not destination_exists:
        return render_template('customer/home_customer_search.html', 
                             username=session['username'],
                             error="Arrival airport or city not found")
    
    # Base query for outbound flights
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
    
    # Execute query for outbound flights
    cursor.execute(query, (source, source, source, destination, destination, destination, departure_date))
    flights = cursor.fetchall()
    
    # If return date is provided, search for return flights
    return_flights = None
    if return_date:
        cursor.execute(query, (destination, destination, destination, source, source, source, return_date))
        return_flights = cursor.fetchall()
    
    cursor.close()
    
    # Debug log to verify results
    print(f"Found {len(flights)} outbound flights and {len(return_flights) if return_flights else 0} return flights")
    
    return render_template('customer/home_customer_search.html', 
                          username=session['username'], 
                          flights=flights,
                          return_flights=return_flights)

@main.route('/home_customer_rate', methods = ['GET','POST'])
@protected_cust
def home_cust_rate():
    if 'username' not in session:
        return redirect(url_for('auth.login'))
    
    customer_email = session['username']
    
    # Check for messages in session
    error = None
    success = None
    
    if 'rating_error' in session:
        error = session.pop('rating_error')  # Get and remove from session
    
    if 'rating_success' in session:
        success = session.pop('rating_success')  # Get and remove from session
    
    # Get past flights that the customer has taken
    cursor = current_app.config['db'].cursor()
    
    # Query for past flights that can be rated
    past_flights_query = '''
    SELECT DISTINCT f.Airline_Name, f.flight_no, f.departure_date_and_time, f.arrival_date_and_time, 
           a1.name as departure_airport, a2.name as arrival_airport,
           a1.city as departure_city, a2.city as arrival_city, f.status
    FROM Purchases p
    JOIN Ticket t ON p.ticket_id = t.ticket_id
    JOIN Flight f ON t.Airline_name = f.Airline_Name 
                 AND t.flight_no = f.flight_no 
                 AND t.departure_date_and_time = f.departure_date_and_time
    JOIN Airport a1 ON f.departure_airport_id = a1.Airport_id
    JOIN Airport a2 ON f.arrival_airport_id = a2.Airport_id
    LEFT JOIN Review r ON p.email = r.email 
                      AND f.Airline_Name = r.Airline_Name 
                      AND f.flight_no = r.flight_no 
                      AND f.departure_date_and_time = r.departure_date_and_time
    WHERE p.email = %s
    AND f.arrival_date_and_time < NOW()  -- Ensure flight has already arrived
    AND r.email IS NULL  -- Ensure flight hasn't been rated already
    ORDER BY f.departure_date_and_time DESC
    '''
    
    cursor.execute(past_flights_query, (customer_email,))
    past_flights = cursor.fetchall()
    cursor.close()
    
    # Get customer name for display
    customer_name = session['username']
    cursor = current_app.config['db'].cursor()
    name_query = 'SELECT name FROM Customer WHERE email = %s'
    cursor.execute(name_query, (customer_email,))
    customer_data = cursor.fetchone()
    if customer_data:
        customer_name = customer_data['name']
    cursor.close()
    
    return render_template('customer/home_customer_rate.html', 
                          username=customer_name,
                          past_flights=past_flights,
                          error=error,
                          success=success)

@main.route('/submit_rating', methods=['POST'])
@protected_cust
def submit_rating():
    if 'username' not in session:
        return redirect(url_for('auth.login'))
    
    customer_email = session['username']
    
    # Get form data
    airline_name = request.form.get('airline_name')
    flight_no = request.form.get('flight_no')
    departure_time = request.form.get('departure_time')
    rating = request.form.get('rate')
    comment = request.form.get('comment', '')
    
    # Debug print to verify we're getting the data
    current_app.logger.debug(f"Rating submission - Airline: {airline_name}, Flight: {flight_no}, Rating: {rating}")
    
    # Validate input
    if not airline_name or not flight_no or not departure_time or not rating:
        # Store error message in session to display after redirect
        session['rating_error'] = "All rating fields are required"
        return redirect(url_for('mainCust.home_cust_rate'))
    
    try:
        # Insert rating into the database
        cursor = current_app.config['db'].cursor()
        
        # Check if this flight exists and customer has purchased a ticket for it
        check_query = '''
        SELECT COUNT(*) as count 
        FROM Purchases p
        JOIN Ticket t ON p.ticket_id = t.ticket_id
        JOIN Flight f ON t.Airline_name = f.Airline_Name 
                     AND t.flight_no = f.flight_no 
                     AND t.departure_date_and_time = f.departure_date_and_time
        WHERE p.email = %s
        AND f.Airline_Name = %s
        AND f.flight_no = %s
        AND f.departure_date_and_time = %s
        '''
        
        cursor.execute(check_query, (customer_email, airline_name, flight_no, departure_time))
        result = cursor.fetchone()
        
        if not result or result['count'] == 0:
            cursor.close()
            session['rating_error'] = "You can only rate flights you have taken"
            return redirect(url_for('mainCust.home_cust_rate'))
        
        # Check if user has already rated this flight
        check_review_query = '''
        SELECT COUNT(*) as count 
        FROM Review
        WHERE email = %s
        AND Airline_Name = %s
        AND flight_no = %s
        AND departure_date_and_time = %s
        '''
        
        cursor.execute(check_review_query, (customer_email, airline_name, flight_no, departure_time))
        result = cursor.fetchone()
        
        if result and result['count'] > 0:
            cursor.close()
            session['rating_error'] = "You have already rated this flight"
            return redirect(url_for('mainCust.home_cust_rate'))
        
        # Insert new review
        insert_query = '''
        INSERT INTO Review (email, Airline_Name, flight_no, departure_date_and_time, rate, comment)
        VALUES (%s, %s, %s, %s, %s, %s)
        '''
        
        cursor.execute(insert_query, (customer_email, airline_name, flight_no, departure_time, rating, comment))
        current_app.config['db'].commit()
        
        cursor.close()
        
        # Store success message in session to display after redirect
        session['rating_success'] = "Thank you for your rating!"
        return redirect(url_for('mainCust.home_cust_rate'))
    
    except Exception as e:
        current_app.logger.error(f"Error submitting rating: {e}")
        session['rating_error'] = f"Error submitting your rating: {str(e)}"
        return redirect(url_for('mainCust.home_cust_rate'))
@main.route('/book_flight', methods=['POST'])
@protected_cust
def book_flight():
    if 'username' not in session:
        return redirect(url_for('auth.login'))
    
    # Get flight details from form
    airline = request.form.get('airline')
    flight_no = request.form.get('flight_no')
    departure_time = request.form.get('departure_time')
    
    # Get the flight information and airplane capacity
    cursor = current_app.config['db'].cursor()
    
    # Query to get flight details and airplane capacity
    query = '''
    SELECT f.base_price, f.Airline_Name, f.flight_no, f.departure_date_and_time, 
           f.arrival_date_and_time, a1.name as departure_airport, a2.name as arrival_airport,
           ap.num_seats
    FROM Flight f
    JOIN Airport a1 ON f.departure_airport_id = a1.Airport_id
    JOIN Airport a2 ON f.arrival_airport_id = a2.Airport_id
    JOIN Airplane ap ON f.Airplane_airline_name = ap.Airline_name AND f.Airplane_id = ap.id
    WHERE f.Airline_Name = %s AND f.flight_no = %s AND f.departure_date_and_time = %s 
    AND f.arrival_date_and_time > NOW()
    '''
    
    cursor.execute(query, (airline, flight_no, departure_time))
    flight_data = cursor.fetchone()
    
    if not flight_data:
        # Flight not found
        flash("Flight not available for booking", "danger")
        return redirect(url_for('mainCust.home_cust_search'))
    
    # Get the number of tickets already sold for this flight
    tickets_query = '''
    SELECT COUNT(*) as tickets_sold
    FROM Ticket
    WHERE Airline_name = %s AND flight_no = %s AND departure_date_and_time = %s
    '''
    cursor.execute(tickets_query, (airline, flight_no, departure_time))
    ticket_data = cursor.fetchone()
    
    cursor.close()
    
    # Calculate current capacity usage
    base_price = float(flight_data['base_price'])
    capacity = int(flight_data['num_seats'])
    tickets_sold = int(ticket_data['tickets_sold'])
    
    # Check if flight is full
    if tickets_sold >= capacity:
        flash("Sorry, this flight is fully booked", "danger")
        return redirect(url_for('mainCust.home_cust_search'))
    
    # Calculate dynamic price based on capacity
    # If 60% or more of seats are booked, add 20% to the base price
    capacity_percentage = (tickets_sold / capacity) * 100
    
    if capacity_percentage >= 60:
        sold_price = base_price * 1.2  # Add 20% to base price
    else:
        sold_price = base_price
    
    # Round to 2 decimal places
    sold_price = round(sold_price, 2)
    
    # Store flight booking details in session for payment page
    session['booking'] = {
        'airline': airline,
        'flight_no': flight_no,
        'departure_time': departure_time,
        'sold_price': sold_price,
        'departure_airport': flight_data['departure_airport'],
        'arrival_airport': flight_data['arrival_airport'],
        'arrival_time': flight_data['arrival_date_and_time'],
        'capacity_percentage': capacity_percentage,
        'base_price': base_price
    }
    
    # Redirect to payment page
    return redirect(url_for('mainCust.payment_page'))

@main.route('/payment_page', methods=['GET'])
@protected_cust
def payment_page():
    if 'username' not in session or 'booking' not in session:
        return redirect(url_for('auth.login'))
    
    booking = session['booking']
    return render_template('customer/payment_page.html', 
                          username=session['username'],
                          booking=booking)

@main.route('/process_payment', methods=['POST'])
@protected_cust
def process_payment():
    if 'username' not in session or 'booking' not in session:
        return redirect(url_for('auth.login'))
    
    # Get booking details from session
    booking = session['booking']
    airline = booking['airline']
    flight_no = booking['flight_no']
    departure_time = booking['departure_time']
    sold_price = booking['sold_price']
    customer_email = session['username']
    
    # Get payment details from form
    card_type = request.form.get('card_type')
    card_num = request.form.get('card_num')
    name_on_card = request.form.get('name_on_card')
    card_expiry_date = request.form.get('card_expiry_date')
    # ---- DEBUG LOGS ----
    print("DEBUG process_payment - booking in session:", session.get('booking'))
    print(f"DEBUG process_payment - form values -> card_type: {card_type}, card_num: {card_num}, "
          f"name_on_card: {name_on_card}, expiry: {card_expiry_date}")
    
    # Validate that all fields are present
    # Validate payment details
    if not card_type or not card_num or not name_on_card or not card_expiry_date:
        print("DEBUG process_payment - missing payment fields")
        flash("All payment fields are required", "danger")
        return render_template('customer/payment_page.html', 
                             username=session['username'],
                             booking=booking,
                             error="All payment fields are required")
    
    # Basic card validation
    if not validate_card(card_type, card_num, card_expiry_date):
        print("DEBUG process_payment - validate_card returned False")
        flash("Invalid card information provided", "danger")
        return render_template('customer/payment_page.html',
                               username=session['username'],
                               booking=booking,
                               error="Invalid card information provided")
    
    # Initialize cursor first
    cursor = current_app.config['db'].cursor()
    
    try:
        # Generate a ticket ID based on the number of tickets booked
        # First, get the count of tickets already in the system
        ticket_count_query = '''
        SELECT COUNT(*) as total_tickets
        FROM Ticket
        '''
        cursor.execute(ticket_count_query)
        ticket_count_data = cursor.fetchone()
        
        # The new ticket ID will be the next number (current count + 1)
        next_ticket_number = ticket_count_data['total_tickets'] + 1
        
        # Format the ticket ID with leading zeros (e.g., TKT00001)
        ticket_id = f"TKT{next_ticket_number:05d}"
        print(f"DEBUG process_payment - generated ticket_id: {ticket_id}")
        
        # Start a transaction
        current_app.config['db'].begin()
        
        # Insert into Ticket table with payment details
        ticket_query = '''
        INSERT INTO Ticket (ticket_id, sold_price, card_type, card_num, name_on_card, card_expiry_date, 
                          Airline_name, flight_no, departure_date_and_time)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        '''
        cursor.execute(ticket_query, (
            ticket_id, sold_price, card_type, card_num, name_on_card, card_expiry_date,
            airline, flight_no, departure_time
        ))
        
        # Insert into Purchases table
        purchase_query = '''
        INSERT INTO Purchases (ticket_id, email, date_and_time)
        VALUES (%s, %s, %s)
        '''
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute(purchase_query, (ticket_id, customer_email, current_time))
        
        # Commit the transaction
        current_app.config['db'].commit()
        
        # Clear booking data from session
        session.pop('booking', None)
        
        # Add debug print to help diagnose issues
        print(f"Redirecting to booking confirmation with ticket ID: {ticket_id}")
        
        # Redirect to booking confirmation page
        return redirect(url_for('mainCust.booking_confirmation', ticket_id=ticket_id))
        
    except Exception as e:
        # If there's an error, rollback the transaction
        current_app.config['db'].rollback()
        current_app.logger.error(f"Error processing payment: {e}")
        print(f"Payment processing error: {e}")  # Add debug print
        return render_template('customer/payment_page.html', 
                             username=session['username'],
                             booking=booking,
                             error=f"Payment processing error: {e}")
    
    finally:
        cursor.close()
def validate_card(card_type, card_num, expiry_date):
    """
    Basic validation for card information
    """
    # Convert expiry date to datetime
    try:
        expiry = datetime.strptime(expiry_date, '%Y-%m-%d')
        if expiry < datetime.now():
            return False
    except:
        return False
    
    # Basic card number validation
    if not card_num.isdigit():
        return False
    
    return True

@main.route('/booking_confirmation/<ticket_id>', methods=['GET'])
@protected_cust
def booking_confirmation(ticket_id):
    if 'username' not in session:
        return redirect(url_for('auth.login'))
    
    # Get ticket details from database
    cursor = current_app.config['db'].cursor()
    query = '''
    SELECT t.ticket_id, t.sold_price, t.Airline_name, t.flight_no, t.departure_date_and_time,
           f.arrival_date_and_time, a1.name as departure_airport, a2.name as arrival_airport
    FROM Ticket t
    JOIN Flight f ON t.Airline_name = f.Airline_Name AND t.flight_no = f.flight_no 
                  AND t.departure_date_and_time = f.departure_date_and_time
    JOIN Airport a1 ON f.departure_airport_id = a1.Airport_id
    JOIN Airport a2 ON f.arrival_airport_id = a2.Airport_id
    WHERE t.ticket_id = %s
    '''
    
    cursor.execute(query, (ticket_id,))
    ticket_data = cursor.fetchone()
    cursor.close()
    
    if not ticket_data:
        return redirect(url_for('mainCust.home_cust_flight'))
    
    return render_template('customer/booking_confirmation.html', 
                          username=session['username'],
                          ticket=ticket_data)
@main.route('/home_customer_flight', methods = ['GET','POST'])
@protected_cust
def home_cust_flight():
    if 'username' not in session:
        return redirect(url_for('auth.login'))
    
    customer_email = session['username']
    
    # Get customer name
    cursor = current_app.config['db'].cursor()
    name_query = 'SELECT name FROM Customer WHERE email = %s'
    cursor.execute(name_query, (customer_email,))
    customer_data = cursor.fetchone()
    
    # Get all flights booked by this customer
    flights_query = '''
    SELECT t.ticket_id, t.sold_price, t.Airline_name, t.flight_no, 
           t.departure_date_and_time, f.arrival_date_and_time, 
           a1.name as departure_airport, a2.name as arrival_airport,
           a1.city as departure_city, a2.city as arrival_city,
           p.date_and_time as booking_date, f.status
    FROM Purchases p
    JOIN Ticket t ON p.ticket_id = t.ticket_id
    JOIN Flight f ON t.Airline_name = f.Airline_Name 
                 AND t.flight_no = f.flight_no 
                 AND t.departure_date_and_time = f.departure_date_and_time
    JOIN Airport a1 ON f.departure_airport_id = a1.Airport_id
    JOIN Airport a2 ON f.arrival_airport_id = a2.Airport_id
    WHERE p.email = %s
    ORDER BY t.departure_date_and_time
    '''
    
    cursor.execute(flights_query, (customer_email,))
    flights = cursor.fetchall()
    
    # Separate upcoming and past flights
    current_time = datetime.now()
    upcoming_flights = []
    past_flights = []
    
    for flight in flights:
        departure_time = flight['departure_date_and_time']
        if isinstance(departure_time, str):
            departure_time = datetime.strptime(departure_time, '%Y-%m-%d %H:%M:%S')
        
        if departure_time > current_time:
            upcoming_flights.append(flight)
        else:
            past_flights.append(flight)
    
    cursor.close()
    
    return render_template('customer/home_customer_flight.html', 
                          username=customer_data['name'] if customer_data else customer_email,
                          upcoming_flights=upcoming_flights,
                          past_flights=past_flights)

@main.route('/cancel_flight', methods=['POST'])
@protected_cust
def cancel_flight():
    if 'username' not in session:
        return redirect(url_for('auth.login'))
    
    ticket_id = request.form.get('ticket_id')
    if not ticket_id:
        flash("Invalid ticket information", "danger")
        return redirect(url_for('mainCust.home_cust_flight'))
    
    customer_email = session['username']
    
    # Get flight details
    cursor = current_app.config['db'].cursor()
    flight_query = '''
    SELECT t.ticket_id, t.departure_date_and_time 
    FROM Ticket t
    JOIN Purchases p ON t.ticket_id = p.ticket_id
    WHERE t.ticket_id = %s AND p.email = %s
    '''
    
    cursor.execute(flight_query, (ticket_id, customer_email))
    flight_data = cursor.fetchone()
    
    if not flight_data:
        cursor.close()
        flash("Ticket not found or not owned by you", "danger")
        return redirect(url_for('mainCust.home_cust_flight'))
    
    # Check if flight is within 24 hours
    departure_time = flight_data['departure_date_and_time']
    if isinstance(departure_time, str):
        departure_time = datetime.strptime(departure_time, '%Y-%m-%d %H:%M:%S')
    
    current_time = datetime.now()
    time_until_departure = departure_time - current_time
    
    # Check if flight is within 24 hours but still process with different message
    within_24_hours = time_until_departure.total_seconds() <= 24 * 3600
    
    try:
       
        
        if within_24_hours:
            flash("Flight cannot be cancelled since it is within 24 hours of departure ", "warning")

        else:
            # Start a transaction
            current_app.config['db'].begin()
            
            # Delete from Purchases table
            delete_purchase_query = 'DELETE FROM Purchases WHERE ticket_id = %s AND email = %s'
            cursor.execute(delete_purchase_query, (ticket_id, customer_email))
            
            # Delete from Ticket table
            delete_ticket_query = 'DELETE FROM Ticket WHERE ticket_id = %s'
            cursor.execute(delete_ticket_query, (ticket_id,))
            
            # Commit the transaction
            current_app.config['db'].commit()
            
            cursor.close()
            flash("Flight cancelled successfully. Your payment will be refunded within 7-10 business days.", "success")
        
        return redirect(url_for('mainCust.home_cust_flight'))
        
    except Exception as e:
        # If there's an error, rollback the transaction
        current_app.config['db'].rollback()
        cursor.close()
        print(f"Error cancelling flight: {e}")
        flash(f"Error cancelling flight: {e}", "danger")
        return redirect(url_for('mainCust.home_cust_flight'))