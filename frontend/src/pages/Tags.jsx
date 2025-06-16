import { useEffect, useState } from "react";
import api from "../api/axios";
import { useAuth } from "../context/AuthContext";

export default function Tags() {
  const { user } = useAuth();
  const [allTags, setAllTags] = useState([]);
  const [userTags, setUserTags] = useState([]);
  const [selectedTag, setSelectedTag] = useState("");

  const fetchTags = async () => {
    const [all, user] = await Promise.all([
      api.get("/tags/"),
      api.get("/tags/user"),
    ]);
    setAllTags(all.data);
    setUserTags(user.data);
  };

  const addUserTag = async () => {
    if (!selectedTag) return;
    await api.post(`/tags/user/${selectedTag}`);
    fetchTags();
  };

  const removeUserTag = async (id) => {
    await api.delete(`/tags/user/${id}`);
    fetchTags();
  };

  useEffect(() => {
    fetchTags();
  }, []);

  return (
    <div className="p-6">
      <h1 className="text-xl font-semibold mb-4">Мои теги</h1>

      <div className="mb-4">
        <select
          className="input"
          value={selectedTag}
          onChange={(e) => setSelectedTag(e.target.value)}
        >
          <option value="">Выбрать тег</option>
          {allTags.map((tag) => (
            <option key={tag.id} value={tag.id}>{tag.name}</option>
          ))}
        </select>
        <button onClick={addUserTag} className="ml-2 bg-blue-600 text-white px-3 py-1 rounded">
          Добавить
        </button>
      </div>

      <ul className="space-y-2">
        {userTags.map((tag) => (
          <li key={tag.id} className="bg-gray-100 p-2 rounded flex justify-between">
            <span>{tag.name}</span>
            <button
              onClick={() => removeUserTag(tag.id)}
              className="text-red-600 hover:underline"
            >
              Удалить
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}
