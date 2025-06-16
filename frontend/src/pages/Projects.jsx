import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import api from "../api/axios";
import { useAuth } from "../context/AuthContext";

export default function Projects() {
  const [projects, setProjects] = useState([]);
  const [form, setForm] = useState({ name: "", description: "", group_id: null });
  const [groups, setGroups] = useState([]);
  const { user } = useAuth();

  useEffect(() => {
    fetchProjects();
    fetchGroups();
  }, []);

  const fetchProjects = () => {
    api.get("/projects/")
      .then(res => setProjects(res.data))
      .catch(console.error);
  };

  const fetchGroups = () => {
    api.get("/groups/owned")
      .then(res => setGroups(res.data))
      .catch(console.error);
  };

  const createProject = async () => {
    if (!form.name.trim()) return;
    try {
      await api.post("/projects/", {
        ...form,
        owner_id: user.id,
        group_id: form.group_id || null,
      });
      setForm({ name: "", description: "", group_id: null });
      fetchProjects();
    } catch (err) {
      console.error("Ошибка создания проекта", err);
    }
  };

  return (
    <div className="p-6">
      <h1 className="text-xl font-semibold mb-4">Мои проекты</h1>

      <div className="mb-6 space-y-2 bg-gray-50 p-4 rounded">
        <input
          type="text"
          placeholder="Название проекта"
          className="input"
          value={form.name}
          onChange={(e) => setForm({ ...form, name: e.target.value })}
        />
        <textarea
          placeholder="Описание (необязательно)"
          className="input h-20"
          value={form.description}
          onChange={(e) => setForm({ ...form, description: e.target.value })}
        />
        <select
          className="input"
          value={form.group_id || ""}
          onChange={(e) =>
            setForm({ ...form, group_id: e.target.value || null })
          }
        >
          <option value="">Без группы</option>
          {groups.map((group) => (
            <option key={group.id} value={group.id}>
              {group.name}
            </option>
          ))}
        </select>
        <button onClick={createProject} className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">
          Создать проект
        </button>
      </div>

      <div className="grid gap-4">
        {projects.map(project => (
          <div key={project.name} className="border p-4 rounded shadow-sm bg-white">
            <h2 className="text-lg font-bold">{project.name}</h2>
            <p className="text-sm text-gray-600">{project.description || "Нет описания"}</p>
            <p className="text-xs text-gray-400 mt-1">
              Создан: {new Date(project.created_at).toLocaleString()} |
              Группа: {project.group_id ?? "—"}
            </p>
            <Link
              to={`/projects/${project.id}`}
              className="mt-2 inline-block text-blue-600 hover:underline"
            >
              Перейти в проект →
            </Link>
          </div>
        ))}
      </div>
    </div>
  );
}
