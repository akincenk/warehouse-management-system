import React, { useEffect, useState } from "react";
import axios from "axios";
import { API_URL } from "../api";

function Dashboard() {
  const [products, setProducts] = useState([]);
  const [users, setUsers] = useState([]);
  const token = localStorage.getItem("token");

  useEffect(() => {
    if (!token) {
      window.location.href = "/";
    } else {
      axios.get(`${API_URL}/products/`, {
        headers: { Authorization: `Bearer ${token}` }
      }).then(res => setProducts(res.data)).catch(() => {
        localStorage.removeItem("token");
        window.location.href = "/";
      });

      axios.get(`${API_URL}/users/`, {
        headers: { Authorization: `Bearer ${token}` }
      }).then(res => setUsers(res.data)).catch(() => {}); // admin-only endpoint
    }
  }, [token]);

  return (
    <div>
      <h2>Dashboard</h2>
      <h3>Products:</h3>
      <ul>
        {products.map(p => (
          <li key={p.id}>{p.name} - {p.quantity}</li>
        ))}
      </ul>
      <h3>Users:</h3>
      <ul>
        {users.map(u => (
          <li key={u.id}>{u.username} - {u.role}</li>
        ))}
      </ul>
    </div>
  );
}

export default Dashboard;
