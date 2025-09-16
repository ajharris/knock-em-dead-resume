import { render, screen, fireEvent } from "@testing-library/react";
import { act } from "react-dom/test-utils";
import OAuthButtons from "../OAuthButtons";

describe("OAuthButtons", () => {
  it("renders all provider buttons", () => {
    render(<OAuthButtons onLogin={() => {}} />);
    expect(screen.getByText(/Sign in with Google/i)).toBeInTheDocument();
    expect(screen.getByText(/Sign in with Facebook/i)).toBeInTheDocument();
    expect(screen.getByText(/Sign in with LinkedIn/i)).toBeInTheDocument();
  });

  it("shows error if popup is blocked", () => {
    const originalOpen = window.open;
    window.open = () => null;
    render(<OAuthButtons onLogin={() => {}} />);
    fireEvent.click(screen.getByText(/Sign in with Google/i));
    expect(screen.getByText(/Popup blocked/i)).toBeInTheDocument();
    window.open = originalOpen;
  });

  it("calls onLogin on oauth-success message", () => {
    const onLogin = jest.fn();
    render(<OAuthButtons onLogin={onLogin} />);
    // Simulate popup
    window.open = jest.fn(() => ({ close: jest.fn() }));
    fireEvent.click(screen.getByText(/Sign in with Google/i));
    window.dispatchEvent(new MessageEvent("message", {
      origin: window.location.origin,
      data: { type: "oauth-success", user: { name: "Test", email: "test@example.com" } }
    }));
    expect(onLogin).toHaveBeenCalledWith({ name: "Test", email: "test@example.com" });
  });

  it("shows error on oauth-error message", async () => {
    render(<OAuthButtons onLogin={() => {}} />);
    window.open = jest.fn(() => ({ close: jest.fn() }));
    fireEvent.click(screen.getByText(/Sign in with Google/i));
    await act(async () => {
      window.dispatchEvent(new MessageEvent("message", {
        origin: window.location.origin,
        data: { type: "oauth-error", error: "OAuth failed" }
      }));
    });
    expect(await screen.findByText(/OAuth failed/i)).toBeInTheDocument();
  });
});
