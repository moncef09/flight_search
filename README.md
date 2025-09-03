<!--
  Flight Search
  -------------
  This web application makes it easy for customers to search, book, and review flights while giving airline staff the tools they need to manage flight operations.  
  It is built with Python, Flask, MySQL and a responsive front‑end.
-->

# ✈️ Flight Search Web Application

Welcome to **Flight Search**, a full‑stack web application designed for airlines and travelers alike.  
Customers can quickly find and book flights, manage their bookings and leave feedback.  
Airline staff get dashboards to create flights, monitor status, view customer information and analyse bookings.  

<p align="center">
  <img src="app/static/airport.webp" alt="Flight Search hero image" width="600" />
</p>

## 🎯 Features

- **Intuitive flight search** — search by city, airport code or name, filter by dates and choose one‑way or return trips.
- **Customer portal** — view past and upcoming trips, book flights with dynamic pricing based on seat availability, and securely pay for tickets.
- **Ratings & reviews** — passengers can rate and comment on completed flights; average ratings are shown to staff.
- **Staff portal** — airline employees can create flights, adjust schedules and statuses, view passenger lists, manage airplanes/airports and generate reports.
- **Role‑based authentication** — separate registration and login flows for customers and airline staff, with protected routes and sessions to keep data secure.
- **Responsive UI** — built with semantic HTML, modern CSS and Jinja2 templates to provide a consistent experience on desktop and mobile.
- **Extensible database schema** — a comprehensive MySQL schema powers the application, covering customers, staff, airlines, airplanes, flights, tickets, purchases and reviews.

## 🛠️ Technology Stack

| Layer            | Technology                                          |
|------------------|-----------------------------------------------------|
| **Language**     | [Python 3](https://www.python.org/)                 |
| **Web framework**| [Flask](https://flask.palletsprojects.com/)         |
| **Database**     | [MySQL](https://www.mysql.com/) via [PyMySQL](https://pymysql.readthedocs.io/) |
| **Frontend**     | HTML5, CSS3 (responsive styles), [Jinja2](https://palletsprojects.com/p/jinja/) |
| **Auth & Sessions**| Flask’s built‑in sessions and custom decorators    |
| **Deployment**   | Tested locally using MAMP for MySQL; easily portable to Docker or cloud services |

## 🚀 Getting Started

Follow these steps to run the project locally.  
The instructions assume **Python 3** and **MySQL** are installed on your machine.  

### 1. Clone the repository

```bash
git clone https://github.com/<your‑username>/flight_search.git
cd flight_search
```

### 2. Install dependencies

Install the Python dependencies using `pip`:

```bash
pip install flask pymysql
```

### 3. Set up the database

1. Start your MySQL server (the original project uses [MAMP](https://www.mamp.info/) with a default socket; adjust configuration in `app/__init__.py` if you use a different host or port).
2. Create a database named **`flights_new`**.
3. Import the schema contained in `app/create_tables.SQL`:

   ```sql
   SOURCE /path/to/app/create_tables.SQL;
   ```

You can optionally add sample data to test the application.

### 4. Run the application

Execute the `run.py` script to start the Flask development server:

```bash
python run.py
```

The application will run at `http://127.0.0.1:8889`.  Visit this URL in your browser to explore the site.  
For live reloading during development, run Flask in debug mode (already enabled in `run.py`).

## 🧭 Project Structure

```
flight_search/
├─ app/                 # Application package
│  ├─ static/           # Static assets (CSS, images)
│  ├─ templates/        # HTML/Jinja2 templates
│  ├─ blueprints/       # Modular Flask blueprints
│  │  ├─ auth/          # Registration & login for customers and staff
│  │  ├─ main/          # Public pages, customer & staff dashboards
│  │  └─ search/        # Flight search and staff flight management
│  └─ create_tables.SQL # SQL schema for the MySQL database
├─ run.py               # Entry point to run the Flask app
└─ README.md            # You are here 📖
```

The application uses **Flask blueprints** to separate concerns: `auth` handles authentication, `main` contains general routes and dashboards for customers and staff, and `search` contains staff‑only search and management endpoints.  Static assets are served from the `static` directory, and templates live in the `templates` directory.

## 🧪 Example Use Cases

- **Searching for flights:** a customer enters a departure city, arrival city and dates.  The application displays matching flights with details like departure/arrival times, airline and price.
- **Booking a flight:** if seats are available, dynamic pricing kicks in (tickets become 20 % more expensive once 60 % of seats are sold).  The user enters payment details and receives confirmation with a unique ticket ID.
- **Rating a flight:** after travelling, customers can rate and review flights.  Staff can view these ratings to improve services.
- **Managing flights (staff):** staff users create new flights, update existing ones and change statuses (e.g. on‑time, delayed, cancelled).  They can also view passenger lists and generate sales reports.

## 🤝 Contributing

Contributions are welcome!  Feel free to fork the repository, create a feature branch, and open a pull request.

1. Fork this repository.
2. Create your feature branch: `git checkout -b <name_of_feature>`.
3. Commit your changes: `git commit -m 'Add some feature'`.
4. Push to the branch: `git push origin <name_of_feature>`.
5. Open a pull request.

## 📄 License

This project is open source and available under the [MIT License](LICENSE).  See the **LICENSE** file for details.

---

> Built with care by the Flight Search team.  
> Designed to showcase Python & Flask skills, SQL knowledge, and full‑stack development.