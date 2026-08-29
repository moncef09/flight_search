import { apiClient } from "./client";
import type { FlightSearchResponse } from "./types";

export interface FlightSearchParams {
  source: string;
  destination: string;
  departure_date: string;
  return_date?: string;
}

export async function searchFlights(params: FlightSearchParams): Promise<FlightSearchResponse> {
  const { data } = await apiClient.get<FlightSearchResponse>("/flights/search", { params });
  return data;
}
