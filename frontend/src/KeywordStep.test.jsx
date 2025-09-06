import React from "react";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import KeywordStep from "./KeywordStep";

// Mock job description
const jobDescription = "We are seeking a Data Analyst with experience in Python, SQL, and data visualization. Must have strong communication skills and experience with Tableau or Power BI. Familiarity with cloud platforms like AWS is a plus.";

describe("KeywordStep", () => {
  it("renders and fetches keywords from API", async () => {
    render(<KeywordStep jobAdId={1} jobDescription={jobDescription} onKeywordsChange={() => {}} />);
    expect(screen.getByText(/Extracted Keywords/i)).toBeInTheDocument();
    await waitFor(() => {
      expect(screen.getByText(/python/i)).toBeInTheDocument();
      expect(screen.getByText(/sql/i)).toBeInTheDocument();
      expect(screen.getByText(/tableau/i)).toBeInTheDocument();
      expect(screen.getByText(/aws/i)).toBeInTheDocument();
    });
  });

  it("allows adding and removing keywords", async () => {
    render(<KeywordStep jobAdId={1} jobDescription={jobDescription} onKeywordsChange={() => {}} />);
    await waitFor(() => screen.getByText(/python/i));
    const input = screen.getByPlaceholderText(/add keyword/i);
    await userEvent.type(input, "newskill{enter}");
    expect(screen.getByText(/newskill/i)).toBeInTheDocument();
    const removeBtn = screen.getAllByRole("button", { name: /×/ })[0];
    await userEvent.click(removeBtn);
    expect(screen.queryByText(/python/i)).not.toBeInTheDocument();
  });
});
