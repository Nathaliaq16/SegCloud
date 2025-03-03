import React, { useEffect, useState } from "react";
import api from "../api";
import "bootstrap/dist/css/bootstrap.min.css";
import { useNavigate } from "react-router-dom";

const ListaCarros = () => {
  const [carros, setCarros] = useState([]);
  const [reseñas, setReseñas] = useState([]);
  const [nuevaReseña, setNuevaReseña] = useState({ rating: 5, comment: "" });
  const [carroSeleccionado, setCarroSeleccionado] = useState(null);
  const [filtroAño, setFiltroAño] = useState("");
  const [filtroKm, setFiltroKm] = useState("");
  const [carrosFiltrados, setCarrosFiltrados] = useState([]);

  const navigate = useNavigate();

  useEffect(() => {
    const obtenerCarros = async () => {
      try {
        const response = await api.get("/carros/");
        setCarros(response.data);
        setCarrosFiltrados(response.data);
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

  const handleReseñaChange = (e) => {
    const { name, value } = e.target;
    setNuevaReseña({
      ...nuevaReseña,
      [name]: name === "rating" ? Number(value) : value,
    });
  };

  const publicarReseña = async (carroId) => {
    try {
      if (nuevaReseña.rating < 1 || nuevaReseña.rating > 5) {
        alert("El rating debe estar entre 1 y 5");
        return;
      }

      await api.post("/reviews/add", {
        carro_id: carroId,
        rating: nuevaReseña.rating,
        comment: nuevaReseña.comment,
        review_date: new Date().toISOString().split("T")[0],
      });

      alert("Reseña publicada exitosamente");

      setReseñas((prevReseñas) => [
        ...prevReseñas,
        {
          id: Date.now(),
          carro_id: carroId,
          rating: nuevaReseña.rating,
          comment: nuevaReseña.comment,
          review_date: new Date().toISOString().split("T")[0],
        },
      ]);

      setNuevaReseña({ rating: 5, comment: "" });
      setCarroSeleccionado(null);
    } catch (error) {
      console.error("Error al publicar la reseña:", error.response?.data || error.message);
      alert("Error al publicar la reseña. Revisa la consola para más detalles.");
    }
  };

  const editarCarro = (id) => {
    navigate(`/editar-carro/${id}`);
  };

  const eliminarCarro = async (id) => {
    if (window.confirm("¿Estás seguro de que quieres eliminar esta publicación?")) {
      try {
        await api.delete(`/carros/delete/${id}`);
        setCarros(carros.filter((carro) => carro.id !== id));
        setCarrosFiltrados(carrosFiltrados.filter((carro) => carro.id !== id));
        alert("Carro eliminado correctamente");
      } catch (error) {
        console.error("Error al eliminar el carro", error);
        alert("Hubo un error al eliminar el carro");
      }
    }
  };

  const aplicarFiltros = () => {
    let filtrados = carros;

    if (filtroAño) {
      filtrados = filtrados.filter((carro) => carro.year === Number(filtroAño));
    }

    if (filtroKm) {
      filtrados = filtrados.filter((carro) => carro.km <= Number(filtroKm));
    }

    setCarrosFiltrados(filtrados);
  };

  const resetFilters = () => {
    setFiltroAño("");
    setFiltroKm("");
    setCarrosFiltrados(carros);
  };

  return (
    <div className="container">
      <div className="row mb-3">
        <div className="col-md-4">
          <input
            type="number"
            className="form-control"
            placeholder="Año mínimo"
            value={filtroAño}
            onChange={(e) => setFiltroAño(e.target.value)}
          />
        </div>
        <div className="col-md-4">
          <input
            type="number"
            className="form-control"
            placeholder="Kilometraje máximo"
            value={filtroKm}
            onChange={(e) => setFiltroKm(e.target.value)}
          />
        </div>
        <div className="col-md-4 d-flex">
          <button
            className="btn w-50 me-2"
            style={{ backgroundColor: "#2b6d6f", color: "white" }}
            onClick={aplicarFiltros}
          >
            Filtrar
          </button>
          <button
            className="btn w-50"
            style={{ backgroundColor: "#4b6e6f", color: "white" }}
            onClick={resetFilters}
          >
            Quitar Filtros
          </button>
        </div>
      </div>

      {carrosFiltrados.map((carro) => (
        <div key={carro.id} className="card mb-4 shadow-sm">
          <div className="row g-0 align-items-center">
            <div className="col-md-4 d-flex justify-content-center align-items-center">
              <img
                src={carro.image_url}
                alt={carro.model}
                className="img-fluid rounded-start"
                style={{ width: "400px", height: "250px", objectFit: "cover", borderRadius: "8px" }}
              />
            </div>

            <div className="col-md-8">
              <div className="card-body">
                <h4 className="card-title">{carro.model}</h4>
                <p className="card-text"><strong>Ubicación:</strong> {carro.location}</p>
                <p className="card-text"><strong>Precio:</strong> ${carro.price.toLocaleString()}</p>
                <p className="card-text"><strong>Año:</strong> {carro.year}</p>
                <p className="card-text"><strong>Kilometraje:</strong> {carro.km.toLocaleString()} km</p>

                {carro.owner === 1 && (
                  <>
                    <button className="btn btn-primary me-2" onClick={() => editarCarro(carro.id)}>Editar</button>
                    <button className="btn btn-danger" onClick={() => eliminarCarro(carro.id)}>Eliminar</button>
                  </>
                )}

                <ul className="list-unstyled">
                  {reseñas.filter((res) => res.carro_id === carro.id).map((res) => (
                    <li key={res.id} className="text-muted">
                      <strong>Calificación:</strong> {res.rating} ⭐ - {res.comment}
                    </li>
                  ))}
                </ul>

                <button
                  className="btn mt-2"
                  style={{ backgroundColor: "#2b6d6f", color: "white" }}
                  onClick={() => setCarroSeleccionado(carro.id)}
                >
                  Publicar Reseña
                </button>

                {carroSeleccionado === carro.id && (
                  <div className="mt-3">
                    <textarea
                      name="comment"
                      className="form-control mb-2"
                      placeholder="Escribe tu reseña"
                      value={nuevaReseña.comment}
                      onChange={handleReseñaChange}
                    />
                    <button className="btn btn-success" onClick={() => publicarReseña(carro.id)}>Enviar Reseña</button>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
};

export default ListaCarros;
