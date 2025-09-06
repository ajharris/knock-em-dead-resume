
import React, { useState } from "react";
import Stepper from "./Stepper";
import LandingPage from "./LandingPage";

function App() {
  const [started, setStarted] = useState(false);
  return started ? <Stepper /> : <LandingPage onStart={() => setStarted(true)} />;
}

export default App;
