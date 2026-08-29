import { apiClient } from "./client";
import type { BookingQuote, MyBookings, PaymentPayload, Ticket } from "./types";

export interface QuoteParams {
  airline_name: string;
  flight_no: string;
  departure_date_and_time: string;
}

export async function getQuote(params: QuoteParams): Promise<BookingQuote> {
  const { data } = await apiClient.get<BookingQuote>("/bookings/quote", { params });
  return data;
}

export async function payForBooking(payload: PaymentPayload): Promise<Ticket> {
  const { data } = await apiClient.post<Ticket>("/bookings/pay", payload);
  return data;
}

export async function getMyBookings(): Promise<MyBookings> {
  const { data } = await apiClient.get<MyBookings>("/bookings/me");
  return data;
}

export async function cancelBooking(ticketId: string): Promise<void> {
  await apiClient.post(`/bookings/${ticketId}/cancel`);
}
