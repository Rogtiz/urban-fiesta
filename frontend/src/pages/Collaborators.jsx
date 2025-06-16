import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import api from "../api/axios";
import { useAuth } from "../context/AuthContext";
import { Link } from "react-router-dom";

export default function Collaborators() {
  const [users, setUsers] = useState([]);
  const { user } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    api.get("/users/open_to_collab").then((res) => setUsers(res.data));
  }, []);

  return (
    <div className="p-6">
      <h1 className="text-xl font-bold mb-4">💡 Пользователи, открытые к коллаборации</h1>
      <div className="grid gap-4">
        {users.map((u) => (
          <Link
            to={`/users/${u.id}`}
            key={u.id}
            className="block border p-4 bg-white rounded shadow hover:bg-gray-50"
          >
            <h2 className="text-lg font-semibold">{u.full_name || u.username}</h2>
            <p className="text-sm text-gray-500">{u.description || "Без описания"}</p>
            <div className="text-xs text-blue-500 mt-1">
              {u.tags?.join(", ")}
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
}
