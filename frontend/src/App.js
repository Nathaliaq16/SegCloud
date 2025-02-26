import React from "react";
import { BrowserRouter as Router, Route, Routes, Navigate } from "react-router-dom";
import PaginaInicioSesion from "./paginas/PaginaInicioSesion";
import Inicio from "./paginas/Inicio";

const PrivateRoute = ({ element }) => {
  const token = localStorage.getItem("token");
  return token ? element : <Navigate to="/" />;
};

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<PaginaInicioSesion />} />
        <Route path="/inicio" element={<PrivateRoute element={<Inicio />} />} />
      </Routes>
    </Router>
  );
}

export default App;
