import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api";
import "bootstrap/dist/css/bootstrap.min.css";
import "../styles/Login.css"; // Si Registro usa este archivo, aquí también lo incluimos

const Vender = () => {
  const [formData, setFormData] = useState({
    model: "",
    location: "",
    price: "",
    year: "",
    km: "",
    image: null,
  });

  const [error, setError] = useState(null);
  const navigate = useNavigate();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleImageChange = (e) => {
    setFormData({ ...formData, image: e.target.files[0] });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    try {
      const formDataToSend = new FormData();
      
      // Agregar campos de texto
      formDataToSend.append("model", formData.model);
      formDataToSend.append("location", formData.location);
      formDataToSend.append("price", formData.price);
      formDataToSend.append("year", formData.year);
      formDataToSend.append("km", formData.km);

      // Agregar imagen
      if (formData.image) {
        formDataToSend.append("imagen", formData.image);
      } else {
        alert("Por favor selecciona una imagen.");
        return;
      }

      const token = localStorage.getItem("token");
      await api.post("/carros/add", formDataToSend, {
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "multipart/form-data",
        },
      });

      alert("Carro publicado con éxito");
      navigate("/inicio");
    } catch (error) {
      setError("Error al publicar el carro");
      console.error("Error al subir el carro:", error);
    }
  };

  return (
    <div className="d-flex align-items-center justify-content-center vh-100">
      <div className="login-box d-flex flex-column w-50 p-4 shadow rounded bg-white">
        <h2 className="text-center mb-3">Publicar un Carro</h2>
        <p className="text-center">Llena los detalles para vender tu carro</p>
        
        <form onSubmit={handleSubmit} className="row">
          <div className="col-md-6 mb-2">
            <input type="text" name="model" placeholder="Modelo" className="form-control" value={formData.model} onChange={handleChange} required />
          </div>
          <div className="col-md-6 mb-2">
            <input type="text" name="location" placeholder="Ubicación" className="form-control" value={formData.location} onChange={handleChange} required />
          </div>
          <div className="col-md-6 mb-2">
            <input type="number" name="price" placeholder="Precio" className="form-control" value={formData.price} onChange={handleChange} required />
          </div>
          <div className="col-md-6 mb-2">
            <input type="number" name="year" placeholder="Año" className="form-control" value={formData.year} onChange={handleChange} required />
          </div>
          <div className="col-md-6 mb-2">
            <input type="number" name="km" placeholder="Kilometraje" className="form-control" value={formData.km} onChange={handleChange} required />
          </div>
          <div className="col-md-6 mb-2">
            <input type="file" accept="image" className="form-control" onChange={handleImageChange} required />
          </div>
          <div className="col-12 mt-3">
            {error && <p className="text-danger text-center">{error}</p>}
	    <button 
		  type="submit" 
		  className="btn w-100 mt-3"
		  style={{ backgroundColor: "#2b6d6f", color: "white" }}
		>
		  Publicar
	</button>

          </div>
        </form>
      </div>
    </div>
  );
};

export default Vender;
