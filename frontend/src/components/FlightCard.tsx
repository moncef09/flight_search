import { Button, Card, CardContent, Chip, Stack, Typography } from "@mui/material";
import type { Flight } from "../api/types";

interface FlightCardProps {
  flight: Flight;
  onSelect?: (flight: Flight) => void;
}

function formatTime(iso: string): string {
  return new Date(iso).toLocaleString(undefined, {
    month: "short",
    day: "numeric",
    hour: "numeric",
    minute: "2-digit",
  });
}

const statusColor: Record<string, "success" | "warning" | "error" | "default"> = {
  "on-time": "success",
  delayed: "warning",
  cancelled: "error",
};

export function FlightCard({ flight, onSelect }: FlightCardProps) {
  return (
    <Card variant="outlined" sx={{ mb: 2 }}>
      <CardContent>
        <Stack direction="row" justifyContent="space-between" alignItems="flex-start" flexWrap="wrap" gap={2}>
          <Stack spacing={0.5}>
            <Typography variant="h6">
              {flight.airline_name} · {flight.flight_no}
            </Typography>
            <Typography color="text.secondary">
              {flight.departure_city} ({flight.departure_airport}) → {flight.arrival_city} (
              {flight.arrival_airport})
            </Typography>
            <Typography variant="body2">
              Departs {formatTime(flight.departure_date_and_time)} · Arrives{" "}
              {formatTime(flight.arrival_date_and_time)}
            </Typography>
            <Chip
              label={flight.status}
              size="small"
              color={statusColor[flight.status] ?? "default"}
              sx={{ width: "fit-content" }}
            />
          </Stack>
          <Stack alignItems="flex-end" spacing={1}>
            <Typography variant="h5">${flight.base_price.toFixed(2)}</Typography>
            {onSelect && (
              <Button variant="contained" onClick={() => onSelect(flight)}>
                Select
              </Button>
            )}
          </Stack>
        </Stack>
      </CardContent>
    </Card>
  );
}
