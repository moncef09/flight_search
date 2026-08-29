import { apiClient } from "./client";
import type {
  Airplane,
  Airport,
  FlightCreatePayload,
  Passenger,
  SalesReport,
  StaffFlight,
  StaffReviewSummary,
} from "./types";

export async function getUpcomingFlights(): Promise<StaffFlight[]> {
  const { data } = await apiClient.get<StaffFlight[]>("/flights/staff/upcoming");
  return data;
}

export interface StaffFlightSearchParams {
  start_date?: string;
  end_date?: string;
  source?: string;
  destination?: string;
  status?: string;
}

export async function searchStaffFlights(params: StaffFlightSearchParams): Promise<StaffFlight[]> {
  const { data } = await apiClient.get<StaffFlight[]>("/flights/staff", { params });
  return data;
}

export async function createOrUpdateFlight(payload: FlightCreatePayload): Promise<StaffFlight> {
  const { data } = await apiClient.post<StaffFlight>("/flights/staff", payload);
  return data;
}

export async function updateFlightStatus(
  flight_no: string,
  departure_date_and_time: string,
  status: string,
): Promise<void> {
  await apiClient.patch("/flights/staff/status", { flight_no, departure_date_and_time, status });
}

export async function addAirport(payload: Airport): Promise<Airport> {
  const { data } = await apiClient.post<Airport>("/staff/airports", payload);
  return data;
}

export async function addAirplane(payload: {
  id: string;
  num_seats: number;
  manufacturing_co: string;
}): Promise<Airplane> {
  const { data } = await apiClient.post<Airplane>("/staff/airplanes", payload);
  return data;
}

export async function listAirplanes(): Promise<Airplane[]> {
  const { data } = await apiClient.get<Airplane[]>("/staff/airplanes");
  return data;
}

export async function getSalesReport(start_date?: string, end_date?: string): Promise<SalesReport> {
  const { data } = await apiClient.get<SalesReport>("/staff/reports", {
    params: { start_date, end_date },
  });
  return data;
}

export async function getRatingsSummary(): Promise<StaffReviewSummary> {
  const { data } = await apiClient.get<StaffReviewSummary>("/reviews/staff/summary");
  return data;
}

export async function getFlightPassengers(
  flightNo: string,
  departure: string,
): Promise<Passenger[]> {
  const { data } = await apiClient.get<Passenger[]>(`/staff/flights/${flightNo}/passengers`, {
    params: { departure },
  });
  return data;
}
