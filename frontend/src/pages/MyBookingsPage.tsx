import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import {
  Alert,
  Button,
  Card,
  CardContent,
  CircularProgress,
  Container,
  Stack,
  Tab,
  Tabs,
  Typography,
} from "@mui/material";
import { useState } from "react";
import { cancelBooking, getMyBookings } from "../api/bookings";
import type { Ticket } from "../api/types";

function TicketCard({ ticket, onCancel }: { ticket: Ticket; onCancel?: (id: string) => void }) {
  return (
    <Card variant="outlined" sx={{ mb: 2 }}>
      <CardContent>
        <Stack direction="row" justifyContent="space-between" alignItems="center" flexWrap="wrap" gap={2}>
          <Stack>
            <Typography variant="subtitle1">
              {ticket.airline_name} {ticket.flight_no}
            </Typography>
            <Typography color="text.secondary">
              {ticket.departure_airport} → {ticket.arrival_airport}
            </Typography>
            <Typography variant="body2">
              {new Date(ticket.departure_date_and_time).toLocaleString()}
            </Typography>
            <Typography variant="body2">Ticket: {ticket.ticket_id} · ${ticket.sold_price.toFixed(2)}</Typography>
          </Stack>
          {onCancel && (
            <Button color="error" variant="outlined" onClick={() => onCancel(ticket.ticket_id)}>
              Cancel
            </Button>
          )}
        </Stack>
      </CardContent>
    </Card>
  );
}

export function MyBookingsPage() {
  const [tab, setTab] = useState<"upcoming" | "past">("upcoming");
  const [cancelError, setCancelError] = useState<string | null>(null);
  const queryClient = useQueryClient();

  const { data, isLoading } = useQuery({ queryKey: ["my-bookings"], queryFn: getMyBookings });

  const cancelMutation = useMutation({
    mutationFn: cancelBooking,
    onSuccess: () => {
      setCancelError(null);
      queryClient.invalidateQueries({ queryKey: ["my-bookings"] });
    },
    onError: (err: unknown) => {
      const message =
        (err as { response?: { data?: { detail?: string } } })?.response?.data?.detail ??
        "Could not cancel this ticket";
      setCancelError(message);
    },
  });

  return (
    <Container maxWidth="md" sx={{ mt: 4, mb: 6 }}>
      <Typography variant="h5" gutterBottom>
        My Bookings
      </Typography>
      <Tabs value={tab} onChange={(_, v) => setTab(v)} sx={{ mb: 2 }}>
        <Tab label="Upcoming" value="upcoming" />
        <Tab label="Past" value="past" />
      </Tabs>

      {cancelError && (
        <Alert severity="error" sx={{ mb: 2 }} onClose={() => setCancelError(null)}>
          {cancelError}
        </Alert>
      )}

      {isLoading && <CircularProgress />}

      {data && (
        <Stack>
          {(tab === "upcoming" ? data.upcoming : data.past).length === 0 && (
            <Alert severity="info">No {tab} flights.</Alert>
          )}
          {(tab === "upcoming" ? data.upcoming : data.past).map((ticket) => (
            <TicketCard
              key={ticket.ticket_id}
              ticket={ticket}
              onCancel={tab === "upcoming" ? (id) => cancelMutation.mutate(id) : undefined}
            />
          ))}
        </Stack>
      )}
    </Container>
  );
}
