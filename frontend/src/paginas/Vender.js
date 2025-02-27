import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api";
import "bootstrap/dist/css/bootstrap.min.css";

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
      Object.keys(formData).forEach((key) => {
        formDataToSend.append(key, formData[key]);
      });
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
    }
  };

  return (
    <div className="container mt-5">
      <h2>Publicar un Carro</h2>
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
          {error && <p className="text-danger">{error}</p>}
          <button type="submit" className="btn btn-success w-100">Publicar</button>
        </div>
      </form>
    </div>
  );
};

export default Vender;
