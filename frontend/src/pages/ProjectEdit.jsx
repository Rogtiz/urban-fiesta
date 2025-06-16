import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import api from "../api/axios";
import { Link } from "react-router-dom";

export default function ProjectEdit() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [form, setForm] = useState({ name: "", description: "" });
  const [userGroups, setUserGroups] = useState([]);

  useEffect(() => {
    loadProject();
    loadGroups();
  }, []);

  const loadProject = async () => {
    const res = await api.get(`/projects/${id}`);
    setForm({
      name: res.data.name,
      description: res.data.description,
      group_id: res.data.group_id,
    });
  };

  const loadGroups = async () => {
    const res = await api.get("/groups/owned");
    setUserGroups(res.data);
  };

  const handleSave = async () => {
    try {
      await api.put(`/projects/${id}`, form);
      navigate(`/projects/${id}`);
    } catch (err) {
      console.error("Ошибка при сохранении", err);
    }
  };

  return (
    <div className="p-6 max-w-lg mx-auto space-y-4">
      <Link to={`/projects/${id}`} className="text-blue-600 underline text-sm">
        ← Назад к проекту
      </Link>
      <h1 className="text-2xl font-bold">Редактировать проект</h1>
      <input
        className="input w-full"
        value={form.name}
        onChange={(e) => setForm({ ...form, name: e.target.value })}
        placeholder="Название проекта"
      />
      <textarea
        className="input w-full"
        value={form.description}
        onChange={(e) => setForm({ ...form, description: e.target.value })}
        placeholder="Описание проекта"
      />
      <label className="block text-sm font-medium">Привязать к группе</label>
      <select
        className="input w-full"
        value={String(form.group_id || "")} // <-- гарантируем строку
        onChange={(e) =>
          setForm({
            ...form,
            group_id: e.target.value === "" ? null : parseInt(e.target.value),
          })
        }
      >
        <option value="">Без группы</option>
        {userGroups.map((group) => (
          <option key={group.id} value={group.id}>
            {group.name}
          </option>
        ))}
      </select>
      <button
        onClick={handleSave}
        className="bg-blue-600 text-white px-4 py-2 rounded"
      >
        💾 Сохранить
      </button>
    </div>
  );
}
