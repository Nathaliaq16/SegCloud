import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api";
import "bootstrap/dist/css/bootstrap.min.css";
import "../styles/Login.css";
import carImage from "../assets/car.png";

const PaginaInicioSesion = () => {
  const [error, setError] = useState(null);
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
      localStorage.setItem("user_id", response.data.user_id);
      navigate("/inicio");
    } catch (error) {
      setError("Credenciales incorrectas");
    }
  };

  return (
    <div className="d-flex align-items-center justify-content-center vh-100">
      <div className="login-box d-flex">
        <div className="image-section">
          <img src={carImage} alt="Carro" className="car-image" />
        </div>
        <div className="form-section">
          <h2 className="text-center">Bienvenido de nuevo</h2>
          <p className="text-center">Inicia sesión en tu cuenta</p>
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
          <button 
		  className="btn w-100"
		  style={{ backgroundColor: "#2b6d6f", color: "white" }}
		  onClick={handleLogin}
		>
		  Iniciar Sesión
		</button>
  
          <p className="text-center mt-2">
            ¿No tienes cuenta? <span className="text-primary" style={{ cursor: "pointer" }} onClick={() => navigate("/registro")}>Regístrate</span>
          </p>
        </div>
      </div>
    </div>
  );
};

export default PaginaInicioSesion;
