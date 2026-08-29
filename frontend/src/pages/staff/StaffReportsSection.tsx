import { useQuery } from "@tanstack/react-query";
import {
  Alert,
  Button,
  Card,
  CardContent,
  CircularProgress,
  Grid,
  Stack,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
  TextField,
  Typography,
} from "@mui/material";
import { useState } from "react";
import { getSalesReport } from "../../api/staff";

export function StaffReportsSection() {
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");
  const [appliedRange, setAppliedRange] = useState<{ start?: string; end?: string }>({});

  const { data, isLoading, refetch } = useQuery({
    queryKey: ["staff-sales-report", appliedRange],
    queryFn: () => getSalesReport(appliedRange.start, appliedRange.end),
  });

  const applyFilter = () => {
    setAppliedRange({ start: startDate || undefined, end: endDate || undefined });
    refetch();
  };

  return (
    <Stack spacing={3}>
      <Typography variant="h6">Sales report</Typography>
      <Grid container spacing={2} alignItems="center">
        <Grid item xs={5} sm={3}>
          <TextField
            label="From"
            type="date"
            fullWidth
            slotProps={{ inputLabel: { shrink: true } }}
            value={startDate}
            onChange={(e) => setStartDate(e.target.value)}
          />
        </Grid>
        <Grid item xs={5} sm={3}>
          <TextField
            label="To"
            type="date"
            fullWidth
            slotProps={{ inputLabel: { shrink: true } }}
            value={endDate}
            onChange={(e) => setEndDate(e.target.value)}
          />
        </Grid>
        <Grid item xs={2}>
          <Button variant="outlined" onClick={applyFilter}>
            Filter
          </Button>
        </Grid>
      </Grid>

      {isLoading && <CircularProgress />}

      {data && (
        <>
          <Card variant="outlined" sx={{ maxWidth: 300 }}>
            <CardContent>
              <Typography color="text.secondary">Total tickets sold</Typography>
              <Typography variant="h4">{data.total_tickets}</Typography>
            </CardContent>
          </Card>

          <Typography variant="subtitle1">Monthly breakdown</Typography>
          {data.monthly_sales.length === 0 ? (
            <Alert severity="info">No sales data yet.</Alert>
          ) : (
            <Table size="small" sx={{ maxWidth: 400 }}>
              <TableHead>
                <TableRow>
                  <TableCell>Month</TableCell>
                  <TableCell align="right">Tickets sold</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {data.monthly_sales.map((m) => (
                  <TableRow key={m.month}>
                    <TableCell>{m.month}</TableCell>
                    <TableCell align="right">{m.tickets_sold}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          )}
        </>
      )}
    </Stack>
  );
}
