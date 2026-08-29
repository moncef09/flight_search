import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { render, screen, waitFor } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { ResultsPage } from "./ResultsPage";
import * as flightsApi from "../api/flights";
import { AuthProvider } from "../auth/AuthContext";
import type { FlightSearchResponse } from "../api/types";

// Explicit factory (not a bare automock) so Jest never has to load the real
// module - api/flights.ts imports api/client.ts, which uses Vite's
// `import.meta.env` syntax that ts-jest can't parse under CommonJS.
jest.mock("../api/flights", () => ({ searchFlights: jest.fn() }));

const mockedSearchFlights = flightsApi.searchFlights as jest.MockedFunction<
  typeof flightsApi.searchFlights
>;

function renderWithProviders(path: string) {
  const queryClient = new QueryClient({
    defaultOptions: { queries: { retry: false } },
  });
  return render(
    <QueryClientProvider client={queryClient}>
      <AuthProvider>
        <MemoryRouter initialEntries={[path]}>
          <ResultsPage />
        </MemoryRouter>
      </AuthProvider>
    </QueryClientProvider>,
  );
}

const sampleFlight = {
  airline_name: "Delta",
  flight_no: "DL100",
  departure_date_and_time: "2026-09-03T12:00:00",
  arrival_date_and_time: "2026-09-03T18:00:00",
  departure_airport: "JFK Airport",
  arrival_airport: "LAX Airport",
  departure_city: "New York",
  arrival_city: "Los Angeles",
  base_price: 249.99,
  status: "on-time",
};

describe("ResultsPage (fetch flow)", () => {
  beforeEach(() => {
    mockedSearchFlights.mockReset();
  });

  it("calls the search API with the URL params and renders the returned flights", async () => {
    const response: FlightSearchResponse = { departure_flights: [sampleFlight], return_flights: [] };
    mockedSearchFlights.mockResolvedValue(response);

    renderWithProviders("/results?source=JFK&destination=LAX&departure_date=2026-09-03");

    await waitFor(() => {
      expect(mockedSearchFlights).toHaveBeenCalledWith({
        source: "JFK",
        destination: "LAX",
        departure_date: "2026-09-03",
        return_date: undefined,
      });
    });

    expect(await screen.findByText("Delta · DL100")).toBeInTheDocument();
  });

  it("shows an empty state when no flights match", async () => {
    mockedSearchFlights.mockResolvedValue({ departure_flights: [], return_flights: [] });

    renderWithProviders("/results?source=JFK&destination=ORD&departure_date=2026-09-03");

    expect(await screen.findByText(/no flights found/i)).toBeInTheDocument();
  });

  it("shows an error message when the search request fails", async () => {
    mockedSearchFlights.mockRejectedValue(new Error("network error"));

    renderWithProviders("/results?source=JFK&destination=LAX&departure_date=2026-09-03");

    expect(await screen.findByText(/something went wrong searching/i)).toBeInTheDocument();
  });
});
