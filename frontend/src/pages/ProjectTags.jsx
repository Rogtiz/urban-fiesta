import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import api from "../api/axios";
import { Link } from "react-router-dom";

export default function ProjectTags() {
  const { id } = useParams();
  const [tags, setTags] = useState([]);
  const [allTags, setAllTags] = useState([]);
  const [selectedTagId, setSelectedTagId] = useState("");

  useEffect(() => {
    loadTags();
  }, []);

  const loadTags = async () => {
    const projectTags = await api.get(`/tags/project/${id}`);
    const all = await api.get("/tags");
    setTags(projectTags.data);
    setAllTags(all.data);
  };

  const handleAdd = async () => {
    if (!selectedTagId) return;
    try {
      await api.post(`/tags/project/${id}/${parseInt(selectedTagId)}`);
      await loadTags();
      setSelectedTagId("");
    } catch (err) {
      console.error("Ошибка при добавлении тега", err);
    }
  };

  const handleDelete = async (tagId) => {
    try {
      await api.delete(`/tags/project/${id}/${tagId}`);
      await loadTags();
    } catch (err) {
      console.error("Ошибка при удалении тега", err);
    }
  };

  return (
    <div className="p-6 max-w-xl mx-auto space-y-4">
      <Link to={`/projects/${id}`} className="text-blue-600 underline text-sm">
        ← Назад к проекту
      </Link>
      <h1 className="text-2xl font-bold">🏷 Управление тегами проекта</h1>

      <div className="flex flex-wrap gap-2">
        {tags.map((tag) => (
          <span
            key={tag.id}
            className="bg-purple-200 text-purple-800 text-xs px-2 py-1 rounded flex items-center gap-1"
          >
            {tag.name}
            <button
              onClick={() => handleDelete(tag.id)}
              className="text-red-600"
            >
              ✕
            </button>
          </span>
        ))}
      </div>

      <div className="flex items-center gap-2 mt-4">
        <select
          value={selectedTagId}
          onChange={(e) => setSelectedTagId(e.target.value)}
          className="input"
        >
          <option value="">Выберите тег</option>
          {allTags
            .filter((tag) => !tags.some((t) => t.id === tag.id))
            .map((tag) => (
              <option key={tag.id} value={tag.id}>
                {tag.name}
              </option>
            ))}
        </select>
        <button
          onClick={handleAdd}
          className="bg-blue-600 text-white px-3 py-1 rounded"
        >
          ➕ Добавить
        </button>
      </div>
    </div>
  );
}
