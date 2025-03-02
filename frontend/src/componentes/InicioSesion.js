import React, { useState } from "react";

const InicioSesion = ({ onLogin, isRegister }) => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [username, setUsername] = useState("");
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [phoneNumber, setPhoneNumber] = useState("");
  const [address, setAddress] = useState("");
  const [city, setCity] = useState("");
  const [country, setCountry] = useState("");
  const [birthdate, setBirthdate] = useState("");

  const validateEmail = (email) => {
    const regex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    return regex.test(email);
  };

  const validatePhoneNumber = (phone) => {
    const regex = /^[0-9]{10}$/;
    return regex.test(phone);
  };

  const validateBirthdate = (date) => {
    const birth = new Date(date);
    const today = new Date();
    const age = today.getFullYear() - birth.getFullYear();
    return age >= 18;
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    if (!validateEmail(email)) {
      alert("Por favor ingresa un correo electrónico válido.");
      return;
    }

    if (!validatePhoneNumber(phoneNumber)) {
      alert("El número de celular debe tener 10 dígitos.");
      return;
    }

    if (!validateBirthdate(birthdate)) {
      alert("Debes ser mayor de 18 años para registrarte.");
      return;
    }

    if (isRegister) {
      onLogin({
        username,
        email,
        password_hash: password,
        first_name: firstName,
        last_name: lastName,
        phone_number: phoneNumber,
        address,
        city,
        country,
        birthdate,
        is_seller: true,
        is_admin: false,
      });
    } else {
      onLogin(email, password);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="row">
      {isRegister && (
        <>
          <div className="col-md-6 mb-2">
            <input type="text" className="form-control" placeholder="Nombre de usuario" value={username} onChange={(e) => setUsername(e.target.value)} required />
          </div>
          <div className="col-md-6 mb-2">
            <input type="text" className="form-control" placeholder="Nombre" value={firstName} onChange={(e) => setFirstName(e.target.value)} required />
          </div>
          <div className="col-md-6 mb-2">
            <input type="text" className="form-control" placeholder="Apellido" value={lastName} onChange={(e) => setLastName(e.target.value)} required />
          </div>
          <div className="col-md-6 mb-2">
            <input type="text" className="form-control" placeholder="Celular" value={phoneNumber} onChange={(e) => setPhoneNumber(e.target.value)} required />
          </div>
          <div className="col-md-6 mb-2">
            <input type="text" className="form-control" placeholder="Dirección" value={address} onChange={(e) => setAddress(e.target.value)} required />
          </div>
          <div className="col-md-6 mb-2">
            <input type="text" className="form-control" placeholder="Ciudad" value={city} onChange={(e) => setCity(e.target.value)} required />
          </div>
          <div className="col-md-6 mb-2">
            <input type="text" className="form-control" placeholder="País" value={country} onChange={(e) => setCountry(e.target.value)} required />
          </div>
          <div className="col-md-6 mb-2">
            <label className="form-label">Fecha de Nacimiento</label>
            <input type="date" className="form-control" value={birthdate} onChange={(e) => setBirthdate(e.target.value)} required />
          </div>
        </>
      )}
      <div className="col-md-6 mb-2">
        <input type="email" className="form-control" placeholder="Correo electrónico" value={email} onChange={(e) => setEmail(e.target.value)} required />
      </div>
      <div className="col-md-6 mb-2">
        <input type="password" className="form-control" placeholder="Contraseña" value={password} onChange={(e) => setPassword(e.target.value)} required />
      </div>
      <div className="col-12 mt-3">
        <button 
          type="submit" 
          className="btn w-100" 
          style={{ backgroundColor: "#2b6d6f", color: "white" }}
        >
          {isRegister ? "Registrarse" : "Ingresar"}
        </button>
      </div>
    </form>
  );
};

export default InicioSesion;
