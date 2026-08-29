// These mirror the Pydantic schemas in backend/app/schemas/ - keeping them in
// sync by hand is a known tradeoff of a hand-rolled client; a follow-up step
// would be generating this file from /openapi.json instead.

export interface TokenResponse {
  access_token: string;
  token_type: string;
  user_type: "customer" | "staff";
  username: string;
}

export interface CustomerRegisterPayload {
  email: string;
  password: string;
  name: string;
  building_num: string;
  street: string;
  city: string;
  state: string;
  phone_num: string;
  passport_number: string;
  passport_expiration: string; // YYYY-MM-DD
  passport_country: string;
  date_of_birth: string; // YYYY-MM-DD
}

export interface Flight {
  airline_name: string;
  flight_no: string;
  departure_date_and_time: string;
  arrival_date_and_time: string;
  departure_airport: string;
  arrival_airport: string;
  departure_city: string;
  arrival_city: string;
  base_price: number;
  status: string;
}

export interface FlightSearchResponse {
  departure_flights: Flight[];
  return_flights: Flight[];
}

export interface BookingQuote {
  airline_name: string;
  flight_no: string;
  departure_date_and_time: string;
  arrival_date_and_time: string;
  departure_airport: string;
  arrival_airport: string;
  base_price: number;
  sold_price: number;
  capacity_percentage: number;
}

export interface PaymentPayload {
  airline_name: string;
  flight_no: string;
  departure_date_and_time: string;
  sold_price: number;
  card_type: string;
  card_num: string;
  name_on_card: string;
  card_expiry_date: string;
}

export interface Ticket {
  ticket_id: string;
  sold_price: number;
  airline_name: string;
  flight_no: string;
  departure_date_and_time: string;
  arrival_date_and_time: string;
  departure_airport: string;
  arrival_airport: string;
  status: string | null;
}

export interface MyBookings {
  upcoming: Ticket[];
  past: Ticket[];
}

export interface RatableFlight {
  airline_name: string;
  flight_no: string;
  departure_date_and_time: string;
  arrival_date_and_time: string;
  departure_airport: string;
  arrival_airport: string;
}

// Staff-facing types - these mirror StaffFlightOut / staff_admin schemas,
// which return raw airport IDs (not names) since there's no airport join.
export interface StaffFlight {
  airline_name: string;
  flight_no: string;
  departure_date_and_time: string;
  arrival_date_and_time: string;
  departure_airport_id: string;
  arrival_airport_id: string;
  status: string;
  base_price: number;
  airplane_airline_name: string | null;
  airplane_id: string | null;
}

export interface FlightCreatePayload {
  flight_no: string;
  departure_date_and_time: string;
  departure_airport_id: string;
  arrival_airport_id: string;
  arrival_date_and_time: string;
  status: string;
  base_price: number;
  airplane_id: string;
}

export interface Airplane {
  id: string;
  airline_name: string;
  num_seats: number;
  manufacturing_co: string;
}

export interface Airport {
  airport_id: string;
  name: string;
  city: string;
  country: string;
}

export interface AverageRating {
  flight_no: string;
  departure_date_and_time: string;
  avg_rating: number;
}

export interface Review {
  email: string;
  airline_name: string;
  flight_no: string;
  departure_date_and_time: string;
  rate: number;
  comment: string | null;
}

export interface StaffReviewSummary {
  average_ratings: AverageRating[];
  reviews: Review[];
}

export interface MonthlySales {
  month: string;
  tickets_sold: number;
}

export interface SalesReport {
  total_tickets: number;
  monthly_sales: MonthlySales[];
}

export interface Passenger {
  name: string;
  passport_number: string | null;
}
