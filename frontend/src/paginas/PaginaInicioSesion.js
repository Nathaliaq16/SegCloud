import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api";
import InicioSesion from "../componentes/InicioSesion";

const PaginaInicioSesion = () => {
  const [error, setError] = useState(null);
  const [registro, setRegistro] = useState(false);
  const navigate = useNavigate();

  const handleLogin = async (email, password) => {
    setError(null);
    try {
      const response = await api.post("/usuarios/login", { email, password });
      localStorage.setItem("token", response.data.token);
      navigate("/inicio");
    } catch (error) {
      setError("Credenciales incorrectas");
    }
  };

const handleRegistro = async (formData) => {
  setError(null);
  try {
    await api.post("/usuarios/add", formData);
    alert("Usuario registrado con éxito, ahora inicia sesión");
    setRegistro(false);
  } catch (error) {
    console.error("Error al registrar usuario:", error.response?.data || error.message);
    setError(error.response?.data?.error || "Error al registrar usuario");
  }
};

  return (
    <div>
      <h2>{registro ? "Registro" : "Iniciar Sesión"}</h2>
      {registro ? (
        <InicioSesion onLogin={handleRegistro} isRegister={true} />
      ) : (
        <InicioSesion onLogin={handleLogin} isRegister={false} />
      )}
      {error && <p style={{ color: "red" }}>{error}</p>}
      <button onClick={() => setRegistro(!registro)}>
        {registro ? "Volver al login" : "Registrarse"}
      </button>
    </div>
  );
};

export default PaginaInicioSesion;

