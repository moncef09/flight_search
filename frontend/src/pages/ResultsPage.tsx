import { useQuery } from "@tanstack/react-query";
import { Alert, CircularProgress, Container, Stack, Typography } from "@mui/material";
import { useNavigate, useSearchParams } from "react-router-dom";
import { searchFlights } from "../api/flights";
import type { Flight } from "../api/types";
import { ResultsList } from "../components/ResultsList";
import { useAuth } from "../auth/AuthContext";

export function ResultsPage() {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const { isAuthenticated } = useAuth();

  const source = searchParams.get("source") ?? "";
  const destination = searchParams.get("destination") ?? "";
  const departureDate = searchParams.get("departure_date") ?? "";
  const returnDate = searchParams.get("return_date") ?? undefined;

  const { data, isLoading, isError } = useQuery({
    queryKey: ["flight-search", source, destination, departureDate, returnDate],
    queryFn: () =>
      searchFlights({
        source,
        destination,
        departure_date: departureDate,
        return_date: returnDate,
      }),
    enabled: !!source && !!destination && !!departureDate,
  });

  const handleSelect = (flight: Flight) => {
    if (!isAuthenticated) {
      navigate("/login", { state: { from: "/results", pendingFlight: flight } });
      return;
    }
    navigate("/booking", { state: { flight } });
  };

  return (
    <Container maxWidth="md" sx={{ mt: 4, mb: 6 }}>
      <Typography variant="h5" gutterBottom>
        {source} → {destination} on {departureDate}
      </Typography>

      {isLoading && <CircularProgress />}
      {isError && <Alert severity="error">Something went wrong searching for flights.</Alert>}

      {data && (
        <Stack spacing={4} sx={{ mt: 2 }}>
          <ResultsList title="Departure flights" flights={data.departure_flights} onSelect={handleSelect} />
          {returnDate && (
            <ResultsList title="Return flights" flights={data.return_flights} onSelect={handleSelect} />
          )}
        </Stack>
      )}
    </Container>
  );
}
