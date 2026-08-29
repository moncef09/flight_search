# Flight Search Frontend (React + TypeScript + Vite)

Talks to the FastAPI backend in `../backend`. Built with MUI, TanStack Query,
React Router, and react-hook-form + zod.

## Directory guide

```
src/
  api/          # typed HTTP client - one file per backend domain (auth, flights, bookings, reviews)
                # types.ts mirrors the backend's Pydantic schemas by hand
  auth/         # AuthContext (JWT storage) + ProtectedRoute (client-side route guard)
  components/   # reusable pieces: SearchForm, FlightCard, ResultsList, NavBar
  pages/        # one component per route, wired up in App.tsx
  pages/staff/  # sections rendered inside StaffDashboardPage's tabs (overview, flights, resources, ratings, reports)
```

## Why these libraries

- **TanStack Query** owns all server data - `useQuery`/`useMutation` handle loading/error
  states and caching, so components don't hand-roll `useEffect` + `useState` fetch logic.
- **react-hook-form + zod** - forms register fields imperatively (no re-render per keystroke)
  and validate against a zod schema before submission, giving typed, validated form values
  for free (`z.infer<typeof schema>`).
- **React Router** protects routes the same way the backend does in spirit: `ProtectedRoute`
  redirects unauthenticated users to `/login`, mirroring `deps.py`'s `CurrentCustomer`/`CurrentStaff`
  on the backend - but this is a UX convenience only. The real enforcement is server-side.

## Running locally

```bash
npm install
npm run dev       # http://localhost:5173, expects the backend at http://127.0.0.1:8000
```

Set `VITE_API_URL` in `.env` if the backend runs somewhere else.

## Tests

```bash
npm test
```

Uses Jest + React Testing Library. `ResultsPage.test.tsx` is the "fetch flow" test - it mocks
the API layer with an explicit factory (`jest.mock("../api/flights", () => ({...}))`) rather
than a bare automock, because the real `api/client.ts` uses Vite's `import.meta.env` syntax
that ts-jest can't parse under CommonJS - the factory means Jest never has to load that file.

## Known next steps

- `api/types.ts` is hand-maintained to mirror the backend's Pydantic schemas. A follow-up would
  be generating it from the backend's `/openapi.json` instead, so the two can't drift apart.
- The staff dashboard (`pages/StaffDashboardPage.tsx` + `pages/staff/*`) covers flight
  management, airports/airplanes, ratings, and sales reports - all wired to real backend data.
  It's plain MUI tables rather than a data grid, so pagination/sorting on large datasets would
  be a reasonable follow-up if an airline's flight list grew large.
