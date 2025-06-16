import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import api from "../api/axios";
import { useAuth } from "../context/AuthContext";

export default function TaskDetail() {
  const { id } = useParams();
  const { user } = useAuth();
  const [task, setTask] = useState(null);
  const [comments, setComments] = useState([]);
  const [text, setText] = useState("");

  const fetchTask = async () => {
    const res = await api.get(`/tasks/${id}`);
    setTask(res.data);
  };

  const fetchComments = async () => {
    const res = await api.get(`/tasks/${id}/comments`);
    setComments(res.data);
  };

  const addComment = async () => {
    if (!text.trim()) return;
    await api.post(`/tasks/${id}/comments`, {
      text,
      task_id: id,
      user_id: user.id,
    });
    setText("");
    fetchComments();
  };

  const toggleComplete = async () => {
    await api.put(`/tasks/${id}`, {
      ...task,
      is_completed: !task.is_completed,
    });
    fetchTask();
  };

  useEffect(() => {
    fetchTask();
    fetchComments();
  }, [id]);

  if (!task) return <p className="p-4">Загрузка...</p>;

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-2">{task.title}</h1>
      <p className="text-gray-600 mb-2">{task.description}</p>
      <p className="text-sm text-gray-400 mb-4">
        Создана: {new Date(task.created_at).toLocaleString()} | Дедлайн: {task.deadline ? new Date(task.deadline).toLocaleString() : "—"}
      </p>

      {task.created_by === user.id || task.assigned_to === user.id ? (
        <button
          className="mb-4 bg-green-600 text-white px-4 py-1 rounded"
          onClick={toggleComplete}
        >
          {task.is_completed ? "Отметить как невыполнено" : "Отметить как выполнено"}
        </button>
      ) : null}

      <hr className="my-6" />

      <h2 className="text-lg font-semibold mb-2">Комментарии</h2>

      <div className="space-y-2 mb-4">
        {comments.map((c) => (
          <div key={c.created_at} className="bg-gray-100 p-2 rounded">
            <p className="text-sm">{c.text}</p>
            <p className="text-xs text-gray-500">Автор ID: {c.user_id}</p>
          </div>
        ))}
      </div>

      <textarea
        placeholder="Оставить комментарий"
        className="input h-20 mb-2"
        value={text}
        onChange={(e) => setText(e.target.value)}
      />
      <br />
      <button onClick={addComment} className="bg-blue-600 text-white px-4 py-1 rounded">
        Отправить
      </button>
    </div>
  );
}
