import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { FlightCard } from "./FlightCard";
import type { Flight } from "../api/types";

const flight: Flight = {
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

describe("FlightCard", () => {
  it("renders flight details", () => {
    render(<FlightCard flight={flight} />);

    expect(screen.getByText("Delta · DL100")).toBeInTheDocument();
    expect(screen.getByText(/New York \(JFK Airport\)/)).toBeInTheDocument();
    expect(screen.getByText(/Los Angeles \(LAX Airport\)/)).toBeInTheDocument();
    expect(screen.getByText("$249.99")).toBeInTheDocument();
    expect(screen.getByText("on-time")).toBeInTheDocument();
  });

  it("does not render a Select button when onSelect is not provided", () => {
    render(<FlightCard flight={flight} />);
    expect(screen.queryByRole("button", { name: /select/i })).not.toBeInTheDocument();
  });

  it("calls onSelect with the flight when Select is clicked", async () => {
    const onSelect = jest.fn();
    const user = userEvent.setup();
    render(<FlightCard flight={flight} onSelect={onSelect} />);

    await user.click(screen.getByRole("button", { name: /select/i }));

    expect(onSelect).toHaveBeenCalledWith(flight);
  });
});
