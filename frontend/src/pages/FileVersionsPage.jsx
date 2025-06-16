import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import api from "../api/axios";
import { useAuth } from "../context/AuthContext";

export default function FileVersionsPage() {
  const { fileId } = useParams();
  const { user } = useAuth();
  const [file, setFile] = useState(null);
  const [versions, setVersions] = useState([]);

  useEffect(() => {
    loadVersions();
  }, [fileId]);

  const loadVersions = async () => {
    try {
      const res = await api.get(`/files/${fileId}`);
      setFile(res.data);

      const vRes = await api.get(`/files/${fileId}/versions`);
      setVersions(vRes.data);
    } catch (err) {
      console.error("Ошибка загрузки версий файла:", err);
    }
  };

  const makeVersionMain = async (versionId) => {
    try {
      await api.post(`/files/version/${versionId}`);
      await loadVersions();
      alert("Версия сделана основной");
    } catch (err) {
      console.error("Ошибка при выборе основной версии:", err);
    }
  };

  return (
    <div className="p-6 space-y-4">
      <h1 className="text-2xl font-bold">Версии файла: {file?.filename}</h1>
      <Link to={`/editor/${file?.project_id}/${file?.id}`} className="text-blue-500 underline text-sm">
        ← Вернуться к редактору
      </Link>

      {versions.length === 0 ? (
        <p className="text-sm text-gray-500">Пока нет сохранённых версий.</p>
      ) : (
        <ul className="space-y-4">
          {versions.map((v) => (
            <li key={v.id} className="border p-4 rounded bg-gray-100">
              <p><strong>Дата:</strong> {new Date(v.created_at).toLocaleString()}</p>
              <p><strong>Описание:</strong> {v.description}</p>
              <p><strong>Пользователь:</strong> {v.user?.username || v.user_id}</p>
              <div className="mt-2 space-x-2">
                <a
                  href={`${api.defaults.baseURL}/files/${v.id}/download_version`}
                  className="text-blue-600 underline"
                >
                  ⬇️ Скачать
                </a>
                <button
                  onClick={() => makeVersionMain(v.id)}
                  className="bg-green-600 text-white px-3 py-1 rounded text-sm"
                >
                  Сделать основной
                </button>
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
