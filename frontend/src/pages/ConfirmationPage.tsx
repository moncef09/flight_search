import { useQuery } from "@tanstack/react-query";
import { CheckCircle } from "@mui/icons-material";
import { Button, Card, CardContent, CircularProgress, Container, Stack, Typography } from "@mui/material";
import { useLocation, useNavigate, useParams } from "react-router-dom";
import { apiClient } from "../api/client";
import type { Ticket } from "../api/types";

export function ConfirmationPage() {
  const { ticketId } = useParams<{ ticketId: string }>();
  const location = useLocation();
  const navigate = useNavigate();
  const stateTicket = (location.state as { ticket?: Ticket } | null)?.ticket;

  const { data: ticket, isLoading } = useQuery({
    queryKey: ["ticket", ticketId],
    queryFn: async () => {
      const { data } = await apiClient.get<Ticket>(`/bookings/${ticketId}`);
      return data;
    },
    initialData: stateTicket,
    enabled: !stateTicket && !!ticketId,
  });

  if (isLoading) return <CircularProgress sx={{ mt: 6, ml: 4 }} />;
  if (!ticket) return null;

  return (
    <Container maxWidth="sm" sx={{ mt: 6 }}>
      <Card variant="outlined">
        <CardContent>
          <Stack spacing={2} alignItems="center" textAlign="center">
            <CheckCircle color="success" sx={{ fontSize: 56 }} />
            <Typography variant="h5">Booking confirmed!</Typography>
            <Typography color="text.secondary">Ticket ID: {ticket.ticket_id}</Typography>
            <Typography>
              {ticket.airline_name} {ticket.flight_no} · {ticket.departure_airport} →{" "}
              {ticket.arrival_airport}
            </Typography>
            <Typography>Total paid: ${ticket.sold_price.toFixed(2)}</Typography>
            <Button variant="contained" onClick={() => navigate("/my-bookings")}>
              View my bookings
            </Button>
          </Stack>
        </CardContent>
      </Card>
    </Container>
  );
}
