import { useState, useEffect } from "react";
import { useAuth } from "../context/AuthContext";
import api from "../api/axios";

export default function Profile() {
  const { user, setUser } = useAuth();
  const [form, setForm] = useState({
    username: user?.username || "",
    email: user?.email || "",
    full_name: user?.full_name || "",
    description: user?.description || "",
    open_to_collab: user?.open_to_collab || false,
  });

  const [message, setMessage] = useState("");
  const [tags, setTags] = useState([]);
  const [allTags, setAllTags] = useState([]);
  const [selectedTagId, setSelectedTagId] = useState("");

  useEffect(() => {
    if (user?.id) {
      api.get(`/tags/user`).then((res) => setTags(res.data));
      api.get("/tags").then((res) => setAllTags(res.data)); // получить все существующие теги
    }
  }, [user]);

  const handleUpdate = async () => {
    try {
      await api.put("/users/update", form);
      setUser({ ...user, ...form });
      setMessage("✅ Данные обновлены");
    } catch (err) {
      console.error(err);
      setMessage("❌ Ошибка при обновлении");
    }
  };

  const handleAddTag = async () => {
    if (!selectedTagId) return;
    try {
      await api.post(`/tags/user/${parseInt(selectedTagId)}`);
      const res = await api.get(`/tags/user`);
      setTags(res.data);
      setSelectedTagId("");
    } catch (err) {
      console.error("Ошибка при добавлении тега", err);
    }
  };

  const handleDeleteTag = async (tagId) => {
    try {
      await api.delete(`/tags/user/${tagId}`);
      setTags(tags.filter((t) => t.id !== tagId));
    } catch (err) {
      console.error("Ошибка при удалении тега", err);
    }
  };

  return (
    <div className="p-6 max-w-md mx-auto space-y-6">
      <h1 className="text-xl font-semibold">Мой профиль</h1>

      {message && <p className="text-sm text-green-600">{message}</p>}

      <input
        type="text"
        className="input"
        value={form.username}
        onChange={(e) => setForm({ ...form, username: e.target.value })}
        placeholder="Имя пользователя"
      />
      <input
        type="email"
        className="input"
        value={form.email}
        onChange={(e) => setForm({ ...form, email: e.target.value })}
        placeholder="Email"
      />
      <input
        type="text"
        className="input"
        value={form.full_name}
        onChange={(e) => setForm({ ...form, full_name: e.target.value })}
        placeholder="Полное имя"
      />
      <textarea
        className="input"
        value={form.description}
        onChange={(e) => setForm({ ...form, description: e.target.value })}
        placeholder="Описание / Чем занимаетесь"
      ></textarea>

      <label className="flex items-center gap-2 text-sm">
        <input
          type="checkbox"
          checked={form.open_to_collab}
          onChange={(e) => setForm({ ...form, open_to_collab: e.target.checked })}
        />
        Готов к коллаборации
      </label>

      <button
        onClick={handleUpdate}
        className="bg-blue-600 text-white px-4 py-2 rounded"
      >
        💾 Обновить профиль
      </button>

      <div className="mt-6">
        <h2 className="text-lg font-semibold">🏷 Мои теги</h2>
        <div className="flex flex-wrap gap-2 mt-2">
          {tags.map((tag) => (
            <span
              key={tag.id}
              className="bg-purple-200 text-purple-800 text-xs px-2 py-1 rounded flex items-center gap-1"
            >
              {tag.name}
              <button
                className="text-red-600"
                onClick={() => handleDeleteTag(tag.id)}
              >
                ✕
              </button>
            </span>
          ))}
        </div>

        <div className="mt-4 flex items-center gap-2">
          <select
            className="input text-sm"
            value={selectedTagId}
            onChange={(e) => setSelectedTagId(e.target.value)}
          >
            <option value="">Выбрать тег</option>
            {allTags
              .filter((tag) => !tags.some((t) => t.id === tag.id))
              .map((tag) => (
                <option key={tag.id} value={tag.id}>
                  {tag.name}
                </option>
              ))}
          </select>
          <button
            onClick={handleAddTag}
            className="bg-blue-600 text-white px-3 py-1 rounded text-sm"
          >
            ➕
          </button>
        </div>
      </div>
    </div>
  );
}
