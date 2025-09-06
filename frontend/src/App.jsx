
import React, { useState } from "react";
import Stepper from "./Stepper";
import LandingPage from "./LandingPage";
import BulletRewriter from "./BulletRewriter";

function App() {
  const [started, setStarted] = useState(false);
  // For demo, show BulletRewriter always. Integrate as needed.
  return (
    <div>
      <BulletRewriter />
      {started ? <Stepper /> : <LandingPage onStart={() => setStarted(true)} />}
    </div>
  );
}

export default App;
