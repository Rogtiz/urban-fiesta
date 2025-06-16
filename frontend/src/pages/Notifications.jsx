import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import api from "../api/axios";
import { useAuth } from "../context/AuthContext";

export default function UserProfile() {
  const navigate = useNavigate();
  const { user } = useAuth();
  const [invitations, setInvitations] = useState([]);

  useEffect(() => {
    api.get("/groups/invitations/get").then((res) => setInvitations(res.data));
  }, []);

  const respond = async (id, action) => {
    await api.post(`/groups/invitations/${id}/${action}`);
    setInvitations((prev) => prev.filter((i) => i.id !== id));
  };

  return (
    <div className="p-6">
      <h1 className="text-xl font-bold mb-4">🔔 Уведомления</h1>
      {invitations.length === 0 ? (
        <p className="text-sm text-gray-500">Нет новых приглашений</p>
      ) : (
        <ul className="space-y-3">
          {invitations.map((inv) => (
            <li key={inv.id} className="bg-white p-4 shadow rounded">
              <p>
                Вас пригласили в группу <strong>{inv.group_name}</strong>
              </p>
              <div className="mt-2 space-x-2">
                <button
                  onClick={() => respond(inv.id, "accept")}
                  className="bg-green-500 hover:bg-green-600 text-white text-sm px-3 py-1 rounded"
                >
                  Принять
                </button>
                
                <button
                  onClick={() => respond(inv.id, "decline")}
                  className="bg-red-500 hover:bg-red-600 text-white text-sm px-3 py-1 rounded"
                >
                  Отклонить
                </button>
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}