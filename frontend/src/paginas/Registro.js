import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api";
import "bootstrap/dist/css/bootstrap.min.css";
import "../styles/Login.css";
import InicioSesion from "../componentes/InicioSesion";

const Registro = () => {
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  const handleRegistro = async (formData) => {
    setError(null);
    try {
      const usuario = {
        ...formData,
        is_admin: false,
        is_active: true,
        registration_date: new Date().toISOString(),
        last_login: new Date().toISOString(),
      };
      await api.post("/usuarios/add", usuario);
      alert("Usuario registrado con éxito, ahora inicia sesión");
      navigate("/");
    } catch (error) {
      console.error("Error al registrar usuario:", error.response?.data || error.message);
      setError(error.response?.data?.error || "Error al registrar usuario");
    }
  };

  return (
    <div className="d-flex align-items-center justify-content-center vh-100">
      <div className="login-box d-flex flex-column w-50 p-4 shadow rounded bg-white">
        <h2 className="text-center mb-3">Registro</h2>
        <p className="text-center">Crea una cuenta</p>
        <div className="row">
          <div className="col-md-12">
            <InicioSesion onLogin={handleRegistro} isRegister={true} />
          </div>
        </div>
        {error && <p className="text-danger text-center mt-2">{error}</p>}
        <p className="text-center mt-2">
          ¿Ya tienes cuenta? <span className="text-primary" style={{ cursor: "pointer" }} onClick={() => navigate("/")}>Inicia sesión</span>
        </p>
      </div>
    </div>
  );
};

export default Registro;

