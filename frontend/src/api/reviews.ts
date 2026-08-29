import { apiClient } from "./client";
import type { RatableFlight } from "./types";

export interface ReviewPayload {
  airline_name: string;
  flight_no: string;
  departure_date_and_time: string;
  rate: number;
  comment?: string;
}

export async function getRatableFlights(): Promise<RatableFlight[]> {
  const { data } = await apiClient.get<RatableFlight[]>("/reviews/ratable");
  return data;
}

export async function submitReview(payload: ReviewPayload): Promise<void> {
  await apiClient.post("/reviews", payload);
}
