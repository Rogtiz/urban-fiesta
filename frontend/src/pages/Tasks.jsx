import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import api from "../api/axios";
import { useAuth } from "../context/AuthContext";

export default function Tasks() {
  const [tasks, setTasks] = useState([]);
  const [form, setForm] = useState({
    title: "",
    description: "",
    project_id: "",
    assigned_to: "",
    deadline: "",
  });
  const [projects, setProjects] = useState([]);
  const [availableUsers, setAvailableUsers] = useState([]);
  const { user } = useAuth();

  useEffect(() => {
    api.get("/tasks/").then((res) => setTasks(res.data));
    api.get("/projects/").then((res) => setProjects(res.data));
  }, []);

  useEffect(() => {
    const loadProjects = async () => {
      const res = await api.get("/projects/");
      setProjects(res.data);
    };
    loadProjects();
  }, []);

  useEffect(() => {
    const loadAvailableUsers = async () => {
      if (!form.project_id) return;
  
      try {
        const project = await api.get(`/projects/${form.project_id}`);
        const groupId = project.data.group_id;
        if (!groupId) {
          setAvailableUsers([]);
          return;
        }
  
        const users = await api.get(`/groups/${groupId}/members`);
        setAvailableUsers(users.data);
      } catch (err) {
        console.error("Ошибка при получении участников группы", err);
        setAvailableUsers([]);
      }
    };
  
    loadAvailableUsers();
  }, [form.project_id]);

  const createTask = async () => {
    if (!form.title || !form.project_id) return;
  
      try {
        await api.post("/tasks/", {
          title: form.title,
          description: form.description,
          project_id: parseInt(form.project_id),
          created_by: user.id,
          assigned_to: form.assigned_to ? parseInt(form.assigned_to) : null,
          deadline: form.deadline || null,
          is_completed: false,
        });
  
        // Очистка формы
        setForm({
          title: "",
          description: "",
          project_id: "",
          assigned_to: "",
          deadline: "",
        });
  
        // Обновление задач
        const res = await api.get("/tasks/");
        setTasks(res.data);
      } catch (err) {
        console.error("Ошибка при создании задачи", err);
    }
  };


  return (
    <div className="p-6">
      <h1 className="text-xl font-bold mb-4">Мои задачи</h1>

      <div className="bg-gray-50 p-4 rounded mb-6">
        <h2 className="text-md font-semibold mb-2">Создать задачу</h2>
        <input
          type="text"
          placeholder="Название задачи"
          className="input mb-2"
          value={form.title}
          onChange={(e) => setForm({ ...form, title: e.target.value })}
        />
        <textarea
          placeholder="Описание"
          className="input mb-2"
          value={form.description}
          onChange={(e) => setForm({ ...form, description: e.target.value })}
        />
        <select
          className="input mb-2"
          value={form.project_id}
          onChange={(e) => setForm({ ...form, project_id: Number(e.target.value) })}
        >
          <option value="">Выберите проект</option>
          {projects.map((p) => (
            <option key={p.id} value={p.id}>{p.name}</option>
          ))}
        </select>
        <select
          className="input mb-2"
          value={form.assigned_to}
          onChange={(e) => setForm({ ...form, assigned_to: e.target.value })}
        >
          <option value="">Без назначения</option>
          {/*<option value={user.id}>Назначить себе</option>*/}
          {availableUsers.map((u) => (
            <option key={u.id} value={u.id}>
              {u.username} ({u.email})
            </option>
          ))}
        </select>
        <input
          type="datetime-local"
          className="input mb-2"
          value={form.deadline}
          onChange={(e) => setForm({ ...form, deadline: e.target.value })}
        />
        <button onClick={createTask} className="bg-blue-600 text-white px-4 py-1 rounded">
          Создать
        </button>
      </div>

      <div className="space-y-3">
        {tasks.map((task, i) => (
          <Link
            to={`/tasks/${task.id}`}
            key={i}
            className="block p-4 rounded bg-white shadow hover:bg-gray-100"
          >
            <div className="flex justify-between">
              <h3 className="font-semibold">{task.title}</h3>
              {task.is_completed && <span className="text-green-600 text-sm">✓ Выполнено</span>}
            </div>
            <p className="text-sm text-gray-600">{task.description}</p>
          </Link>
        ))}
      </div>
    </div>
  );
}
