import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api";
import "bootstrap/dist/css/bootstrap.min.css";
import "../styles/Login.css"; // Archivo de estilos personalizados
import carImage from "../assets/car.png"; // Asegúrate de que la imagen esté en esta carpeta

const PaginaInicioSesion = () => {
  const [error, setError] = useState(null);
  const [registro, setRegistro] = useState(false);
  const [formData, setFormData] = useState({ email: "", password: "" });
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleLogin = async () => {
    setError(null);
    try {
      const response = await api.post("/usuarios/login", formData);
      localStorage.setItem("token", response.data.token);
      navigate("/inicio");
    } catch (error) {
      setError("Credenciales incorrectas");
    }
  };

  const handleRegistro = async () => {
    setError(null);
    try {
      await api.post("/usuarios/add", formData);
      alert("Usuario registrado con éxito, ahora inicia sesión");
      setRegistro(false);
    } catch (error) {
      setError("Error al registrar usuario");
    }
  };

  return (
    <div className="d-flex align-items-center justify-content-center vh-100">
      <div className="login-box d-flex">
        {/* Sección Izquierda - Imagen */}
        <div className="image-section">
          <img src={carImage} alt="Carro" className="car-image" />
        </div>
        
        {/* Sección Derecha - Formulario */}
        <div className="form-section">
          <h2 className="text-center">{registro ? "Registro" : "Bienvenido de nuevo"}</h2>
          <p className="text-center">{registro ? "Crea una cuenta" : "Inicia sesión en tu cuenta"}</p>
          <input
            type="email"
            name="email"
            placeholder="Correo electrónico"
            className="form-control mb-2"
            value={formData.email}
            onChange={handleChange}
          />
          <input
            type="password"
            name="password"
            placeholder="Contraseña"
            className="form-control mb-3"
            value={formData.password}
            onChange={handleChange}
          />
          {error && <p className="text-danger text-center">{error}</p>}
          <button className="btn btn-primary w-100" onClick={registro ? handleRegistro : handleLogin}>
            {registro ? "Registrarse" : "Iniciar Sesión"}
          </button>
          <p className="text-center mt-2">
            {registro ? "¿Ya tienes cuenta? " : "¿No tienes cuenta? "}
            <span className="text-primary" style={{ cursor: "pointer" }} onClick={() => setRegistro(!registro)}>
              {registro ? "Inicia sesión" : "Regístrate"}
            </span>
          </p>
        </div>
      </div>
    </div>
  );
};

export default PaginaInicioSesion;
