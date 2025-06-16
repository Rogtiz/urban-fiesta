import { useEffect, useState } from "react";
import { useAuth } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";
import api from "../api/axios";
import EmailWarning from "../components/EmailWarning";

export default function Dashboard() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const [groups, setGroups] = useState([]);
  const [projects, setProjects] = useState([]);

  useEffect(() => {
    api.get("/groups").then((res) => setGroups(res.data));
    api.get("/projects").then((res) => setProjects(res.data));
  }, []);

  return (
    <div className="p-6 max-w-4xl mx-auto space-y-6">
      <EmailWarning />

      <div className="bg-white p-6 shadow rounded-lg">
        <h1 className="text-3xl font-bold mb-2">👋 Привет, {user?.username}!</h1>
        <p className="text-gray-600 mb-1">📧 {user?.email}</p>
        <p className="text-sm">
          {user?.is_verified ? (
            <span className="text-green-600">✅ Email подтверждён</span>
          ) : (
            <span className="text-red-500">⚠️ Email не подтверждён</span>
          )}
        </p>
        <p className="text-sm mt-2">
          {user?.open_to_collab ? (
            <span className="bg-green-100 text-green-700 px-2 py-1 rounded text-xs font-medium">Открыт к коллаборации</span>
          ) : (
            <span className="bg-gray-100 text-gray-700 px-2 py-1 rounded text-xs font-medium">Не открыт к коллаборации</span>
          )}
        </p>
        <div className="mt-4 space-x-2">
          <button
            onClick={() => navigate("/profile")}
            className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-1 rounded"
          >
            Мой профиль
          </button>
          <button
            onClick={() => navigate("/projects")}
            className="bg-purple-600 hover:bg-purple-700 text-white px-4 py-1 rounded"
          >
            Проекты
          </button>
          <button
            onClick={() => navigate("/groups")}
            className="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-1 rounded"
          >
            Группы
          </button>
          <button
            onClick={logout}
            className="bg-red-500 hover:bg-red-600 text-white px-4 py-1 rounded"
          >
            Выйти
          </button>
        </div>
      </div>

      <div className="grid md:grid-cols-2 gap-6">
        <div className="bg-white p-4 shadow rounded-lg">
          <h2 className="text-xl font-semibold mb-2">🧑‍🤝‍🧑 Мои группы</h2>
          {groups.length === 0 ? (
            <p className="text-sm text-gray-500">Вы пока не состоите в группах.</p>
          ) : (
            <ul className="text-sm space-y-1">
              {groups.slice(0, 5).map((group) => (
                <li key={group.id} className="text-blue-600 hover:underline cursor-pointer" onClick={() => navigate(`/groups/${group.id}`)}>
                  {group.name}
                </li>
              ))}
            </ul>
          )}
        </div>

        <div className="bg-white p-4 shadow rounded-lg">
          <h2 className="text-xl font-semibold mb-2">📁 Последние проекты</h2>
          {projects.length === 0 ? (
            <p className="text-sm text-gray-500">Нет проектов</p>
          ) : (
            <ul className="text-sm space-y-1">
              {projects.slice(0, 5).map((proj) => (
                <li key={proj.id} className="text-blue-600 hover:underline cursor-pointer" onClick={() => navigate(`/projects/${proj.id}`)}>
                  {proj.name}
                </li>
              ))}
            </ul>
          )}
        </div>
      </div>
    </div>
  );
}
