import { Alert, Stack, Typography } from "@mui/material";
import type { Flight } from "../api/types";
import { FlightCard } from "./FlightCard";

interface ResultsListProps {
  title: string;
  flights: Flight[];
  onSelect?: (flight: Flight) => void;
}

export function ResultsList({ title, flights, onSelect }: ResultsListProps) {
  return (
    <Stack spacing={1}>
      <Typography variant="h6">{title}</Typography>
      {flights.length === 0 ? (
        <Alert severity="info">No flights found for these dates.</Alert>
      ) : (
        flights.map((flight) => (
          <FlightCard
            key={`${flight.airline_name}-${flight.flight_no}-${flight.departure_date_and_time}`}
            flight={flight}
            onSelect={onSelect}
          />
        ))
      )}
    </Stack>
  );
}
