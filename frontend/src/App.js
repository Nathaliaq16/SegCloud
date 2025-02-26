import React from "react";
import { BrowserRouter as Router, Route, Routes, Navigate } from "react-router-dom";
import Navbar from "./componentes/Navbar";
import PaginaInicioSesion from "./paginas/PaginaInicioSesion";
import Inicio from "./paginas/Inicio";

const PrivateRoute = ({ element }) => {
  const token = localStorage.getItem("token");
  return token ? element : <Navigate to="/" />;
};

function App() {
  return (
    <Router>
      <Navbar /> {/* Navbar siempre presente */}
      <div className="container mt-4">
        <Routes>
          <Route path="/" element={<PaginaInicioSesion />} />
          <Route path="/inicio" element={<PrivateRoute element={<Inicio />} />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
