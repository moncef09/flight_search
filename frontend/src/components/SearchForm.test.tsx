import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { SearchForm } from "./SearchForm";

describe("SearchForm", () => {
  it("calls onSearch with the entered values when valid", async () => {
    const onSearch = jest.fn();
    const user = userEvent.setup();
    render(<SearchForm onSearch={onSearch} />);

    await user.type(screen.getByLabelText(/from/i), "JFK");
    await user.type(screen.getByLabelText(/to/i), "LAX");
    await user.type(screen.getByLabelText(/departure date/i), "2026-09-03");
    await user.click(screen.getByRole("button", { name: /search flights/i }));

    expect(onSearch).toHaveBeenCalledWith(
      expect.objectContaining({ source: "JFK", destination: "LAX", departure_date: "2026-09-03" }),
      expect.anything(),
    );
  });

  it("shows a validation error and does not submit when required fields are empty", async () => {
    const onSearch = jest.fn();
    const user = userEvent.setup();
    render(<SearchForm onSearch={onSearch} />);

    await user.click(screen.getByRole("button", { name: /search flights/i }));

    expect(await screen.findByText(/departure city\/airport is required/i)).toBeInTheDocument();
    expect(onSearch).not.toHaveBeenCalled();
  });

  it("rejects a return date earlier than the departure date", async () => {
    const onSearch = jest.fn();
    const user = userEvent.setup();
    render(<SearchForm onSearch={onSearch} />);

    await user.type(screen.getByLabelText(/from/i), "JFK");
    await user.type(screen.getByLabelText(/to/i), "LAX");
    await user.type(screen.getByLabelText(/departure date/i), "2026-09-10");
    await user.type(screen.getByLabelText(/return date/i), "2026-09-01");
    await user.click(screen.getByRole("button", { name: /search flights/i }));

    expect(
      await screen.findByText(/return date must be on or after the departure date/i),
    ).toBeInTheDocument();
    expect(onSearch).not.toHaveBeenCalled();
  });

  it("rejects when source and destination are the same", async () => {
    const onSearch = jest.fn();
    const user = userEvent.setup();
    render(<SearchForm onSearch={onSearch} />);

    await user.type(screen.getByLabelText(/from/i), "JFK");
    await user.type(screen.getByLabelText(/to/i), "JFK");
    await user.type(screen.getByLabelText(/departure date/i), "2026-09-10");
    await user.click(screen.getByRole("button", { name: /search flights/i }));

    expect(await screen.findByText(/can't be the same/i)).toBeInTheDocument();
    expect(onSearch).not.toHaveBeenCalled();
  });
});
