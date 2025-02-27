import React, { useEffect, useState } from "react";
import api from "../api";

const ListaCarros = () => {
  const [carros, setCarros] = useState([]);
  const [reseñas, setReseñas] = useState([]);
  const [showForm, setShowForm] = useState(null);
  const [reviewData, setReviewData] = useState({ rating: "", comment: "" });

  useEffect(() => {
    const obtenerCarros = async () => {
      try {
        const response = await api.get("/carros/");
        setCarros(response.data);
      } catch (error) {
        console.error("Error al obtener los carros", error);
      }
    };

    const obtenerReseñas = async () => {
      try {
        const response = await api.get("/reviews/");
        setReseñas(response.data);
      } catch (error) {
        console.error("Error al obtener las reseñas", error);
      }
    };

    obtenerCarros();
    obtenerReseñas();
  }, []);

  const handleReviewSubmit = async (carroId) => {
    try {
      const token = localStorage.getItem("token");
      await api.post("/reviews/add", { carro_id: carroId, ...reviewData }, {
        headers: { Authorization: `Bearer ${token}` },
      });
      alert("Reseña publicada con éxito");
      setShowForm(null);
      setReviewData({ rating: "", comment: "" });
    } catch (error) {
      console.error("Error al publicar la reseña", error);
    }
  };

  return (
    <div>
      <h2>Lista de Carros</h2>
      {carros.map((carro) => (
        <div key={carro.id} style={{ border: "1px solid #ddd", padding: "10px", marginBottom: "10px" }}>
          <h3>{carro.model}</h3>
          <p><strong>Ubicación:</strong> {carro.location}</p>
          <p><strong>Precio:</strong> ${carro.price}</p>
          <p><strong>Año:</strong> {carro.year}</p>
          <p><strong>Kilometraje:</strong> {carro.km} km</p>
          <img src={carro.image_url} alt={carro.model} width="200" height="200" />
          <h4>Reseñas:</h4>
          <ul>
            {reseñas.filter((res) => res.carro_id === carro.id).map((res) => (
              <li key={res.id}><strong>Calificación:</strong> {res.rating} ⭐ - {res.comment}</li>
            ))}
          </ul>
          {reseñas.filter((res) => res.carro_id === carro.id).length === 0 && <p>No hay reseñas para este carro.</p>}
          <button className="btn btn-primary mt-2" onClick={() => setShowForm(carro.id)}>Publicar Reseña</button>
          {showForm === carro.id && (
            <div className="mt-2">
              <input type="number" placeholder="Calificación (1-5)" className="form-control mb-2" value={reviewData.rating} onChange={(e) => setReviewData({ ...reviewData, rating: e.target.value })} required />
              <textarea placeholder="Comentario" className="form-control mb-2" value={reviewData.comment} onChange={(e) => setReviewData({ ...reviewData, comment: e.target.value })} required />
              <button className="btn btn-success" onClick={() => handleReviewSubmit(carro.id)}>Enviar Reseña</button>
            </div>
          )}
        </div>
      ))}
    </div>
  );
};

export default ListaCarros;
