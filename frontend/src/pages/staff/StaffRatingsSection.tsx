import { useQuery } from "@tanstack/react-query";
import {
  Alert,
  Chip,
  CircularProgress,
  Stack,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
  Typography,
} from "@mui/material";
import { getRatingsSummary } from "../../api/staff";

export function StaffRatingsSection() {
  const { data, isLoading } = useQuery({ queryKey: ["staff-ratings"], queryFn: getRatingsSummary });

  if (isLoading) return <CircularProgress />;
  if (!data) return null;

  return (
    <Stack spacing={3}>
      <div>
        <Typography variant="h6" gutterBottom>
          Average rating by flight
        </Typography>
        {data.average_ratings.length === 0 ? (
          <Alert severity="info">No ratings yet.</Alert>
        ) : (
          <Table size="small">
            <TableHead>
              <TableRow>
                <TableCell>Flight</TableCell>
                <TableCell>Departure</TableCell>
                <TableCell align="right">Avg rating</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {data.average_ratings.map((r) => (
                <TableRow key={`${r.flight_no}-${r.departure_date_and_time}`}>
                  <TableCell>{r.flight_no}</TableCell>
                  <TableCell>{new Date(r.departure_date_and_time).toLocaleString()}</TableCell>
                  <TableCell align="right">
                    <Chip label={`${r.avg_rating.toFixed(1)} ★`} size="small" color="primary" />
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        )}
      </div>

      <div>
        <Typography variant="h6" gutterBottom>
          All reviews
        </Typography>
        {data.reviews.length === 0 ? (
          <Alert severity="info">No reviews yet.</Alert>
        ) : (
          <Table size="small">
            <TableHead>
              <TableRow>
                <TableCell>Flight</TableCell>
                <TableCell>Customer</TableCell>
                <TableCell>Rating</TableCell>
                <TableCell>Comment</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {data.reviews.map((review, i) => (
                <TableRow key={i}>
                  <TableCell>{review.flight_no}</TableCell>
                  <TableCell>{review.email}</TableCell>
                  <TableCell>{review.rate} ★</TableCell>
                  <TableCell>{review.comment ?? "—"}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        )}
      </div>
    </Stack>
  );
}
