import { useQuery } from "@tanstack/react-query";
import {
  Alert,
  CircularProgress,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Typography,
} from "@mui/material";
import { getUpcomingFlights } from "../../api/staff";

export function StaffOverviewSection() {
  const { data, isLoading } = useQuery({
    queryKey: ["staff-upcoming-flights"],
    queryFn: getUpcomingFlights,
  });

  if (isLoading) return <CircularProgress />;

  return (
    <>
      <Typography variant="h6" gutterBottom>
        Upcoming flights (next 30 days)
      </Typography>
      {!data || data.length === 0 ? (
        <Alert severity="info">No upcoming flights scheduled.</Alert>
      ) : (
        <TableContainer>
          <Table size="small">
            <TableHead>
              <TableRow>
                <TableCell>Flight</TableCell>
                <TableCell>Route</TableCell>
                <TableCell>Departs</TableCell>
                <TableCell>Status</TableCell>
                <TableCell align="right">Base price</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {data.map((flight) => (
                <TableRow key={`${flight.flight_no}-${flight.departure_date_and_time}`}>
                  <TableCell>{flight.flight_no}</TableCell>
                  <TableCell>
                    {flight.departure_airport_id} → {flight.arrival_airport_id}
                  </TableCell>
                  <TableCell>{new Date(flight.departure_date_and_time).toLocaleString()}</TableCell>
                  <TableCell>{flight.status}</TableCell>
                  <TableCell align="right">${flight.base_price.toFixed(2)}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      )}
    </>
  );
}
