import React from "react";
import { BrowserRouter as Router, Route, Routes, Navigate } from "react-router-dom";
import Navbar from "./componentes/Navbar";
import PaginaInicioSesion from "./paginas/PaginaInicioSesion";
import Registro from "./paginas/Registro";
import Inicio from "./paginas/Inicio";
import Vender from "./paginas/Vender";

import EditarCarro from "./paginas/Editar"; 

const PrivateRoute = ({ element }) => {
  const token = localStorage.getItem("token");
  return token ? element : <Navigate to="/" />;
};

function App() {
  return (
    <Router>
      <Navbar />
      <div className="container mt-4">
        <Routes>
          <Route path="/" element={<PaginaInicioSesion />} />
          <Route path="/registro" element={<Registro />} />
          <Route path="/inicio" element={<PrivateRoute element={<Inicio />} />} />
          <Route path="/vender" element={<PrivateRoute element={<Vender />} />} />
          <Route path="/editar-carro/:id" element={<PrivateRoute element={<EditarCarro />} />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
