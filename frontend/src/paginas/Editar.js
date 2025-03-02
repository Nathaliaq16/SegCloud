import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import api from "../api";
import "bootstrap/dist/css/bootstrap.min.css";

const EditarCarro = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [formData, setFormData] = useState(null); // Inicializar en null para evitar errores de renderizado

  useEffect(() => {
    const obtenerCarro = async () => {
      try {
        const response = await api.get(`/carros/${id}`);
        if (response.data.length > 0) { // Asegurar que hay datos en la respuesta
          setFormData({
            model: response.data[0].model,
            location: response.data[0].location,
            price: response.data[0].price,
            year: response.data[0].year,
            km: response.data[0].km,
            usuario_id: response.data[0].usuario_id, // Guardar usuario_id en el estado
            image_url:response.data[0].image_url,
            image: null, // No se puede prellenar un archivo
          });
        } else {
          console.error("No se encontró el carro con el ID proporcionado.");
        }
      } catch (error) {
        console.error("Error al obtener los datos del carro", error);
      }
    };
    obtenerCarro();
  }, [id]);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleImageChange = (e) => {
    setFormData({ ...formData, image: e.target.files[0] });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const formDataToSend = new FormData();
      formDataToSend.append("model", formData.model);
      formDataToSend.append("location", formData.location);
      formDataToSend.append("price", formData.price);
      formDataToSend.append("year", formData.year);
      formDataToSend.append("km", formData.km);
      formDataToSend.append("usuario_id", formData.usuario_id); // Agregar usuario_id

      if (formData.image) {
        formDataToSend.append("imagen", formData.image);
      }
      else{
        formDataToSend.append("image_url", formData.image_url);
      }

      await api.put(`/carros/update/${id}`, formDataToSend, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      navigate("/inicio");
    } catch (error) {
      console.error("Error al actualizar el carro", error);
    }
  };

  return (
    <div className="container mt-4">
      <h2>Editar Carro</h2>
      {/* Solo renderizar el formulario si `formData` ya tiene datos */}
      {formData ? (
        <form onSubmit={handleSubmit} className="row">
          <div className="col-md-6 mb-2">
            <input type="text" name="model" className="form-control" value={formData.model} onChange={handleChange} required />
          </div>
          <div className="col-md-6 mb-2">
            <input type="text" name="location" className="form-control" value={formData.location} onChange={handleChange} required />
          </div>
          <div className="col-md-6 mb-2">
            <input type="number" name="price" className="form-control" value={formData.price} onChange={handleChange} required />
          </div>
          <div className="col-md-6 mb-2">
            <input type="number" name="year" className="form-control" value={formData.year} onChange={handleChange} required />
          </div>
          <div className="col-md-6 mb-2">
            <input type="number" name="km" className="form-control" value={formData.km} onChange={handleChange} required />
          </div>
          <div className="col-md-6 mb-2">
            <input type="file" accept="image/*" className="form-control" onChange={handleImageChange} />
          </div>
          <div className="col-12 mt-3">
            <button type="submit" className="btn btn-success w-100">Guardar Cambios</button>
          </div>
        </form>
      ) : (
        <p>Cargando datos del carro...</p> // Muestra esto mientras se cargan los datos
      )}
    </div>
  );
};

export default EditarCarro;
