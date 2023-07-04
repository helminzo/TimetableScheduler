import "./App.css";
import Header from "./Header";
import Home from "./Home";
import Signin from "./Signin";
import Institution from "./Institution";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
//import { Router } from "react-router-dom";
//import { Switch } from "@mui/base";

function App() {
  return (
    <Router>
      <div className="app">
        <Routes>
        
          <Route path="/" element={<><Header/><Home/></>}> </Route>
          <Route path="/institution" element={<><Header/><Institution /></> }></Route> 
          <Route path="/signin" element={<Signin />}></Route>
        </Routes>
      </div>
    </Router>
  );
}

export default App;
