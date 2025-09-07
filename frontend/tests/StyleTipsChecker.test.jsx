import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import StyleTipsChecker from "../src/StyleTipsChecker";

// Mock fetch
beforeEach(() => {
  global.fetch = jest.fn();
});
afterEach(() => {
  jest.resetAllMocks();
});

test("shows style tips after clicking Check Style", async () => {
  fetch.mockResolvedValueOnce({
    ok: true,
    json: async () => ({
      tips: [
        { tip: "Avoid passive voice.", severity: "warning" },
        { tip: "Quantify achievements.", severity: "info" }
      ]
    })
  });
  render(<StyleTipsChecker resumeText="My resume content." />);
  fireEvent.click(screen.getByText(/check style/i));
  expect(screen.getByText(/checking/i)).toBeInTheDocument();
  await waitFor(() => expect(screen.getByText(/avoid passive voice/i)).toBeInTheDocument());
  expect(screen.getByText(/quantify achievements/i)).toBeInTheDocument();
});

test("handles API error", async () => {
  fetch.mockResolvedValueOnce({ ok: false });
  render(<StyleTipsChecker resumeText="My resume content." />);
  fireEvent.click(screen.getByText(/check style/i));
  await waitFor(() => expect(screen.getByText(/failed to get style tips/i)).toBeInTheDocument());
});

test("disables button with empty input", () => {
  render(<StyleTipsChecker resumeText="   " />);
  expect(screen.getByText(/check style/i)).toBeDisabled();
});

test("can mark tip as resolved and ignored", async () => {
  fetch.mockResolvedValueOnce({
    ok: true,
    json: async () => ({
      tips: [
        { tip: "Use active voice.", severity: "info" }
      ]
    })
  });
  render(<StyleTipsChecker resumeText="Some text" />);
  fireEvent.click(screen.getByText(/check style/i));
  await waitFor(() => expect(screen.getByTestId("tip-text-0")).toBeInTheDocument());
  fireEvent.click(screen.getByText(/resolved/i));
  expect(screen.getByTestId("tip-item-0")).toHaveStyle("text-decoration: line-through");
  fireEvent.click(screen.getByText(/ignore/i));
  expect(screen.getByTestId("tip-item-0")).toHaveStyle("opacity: 0.4");
});
