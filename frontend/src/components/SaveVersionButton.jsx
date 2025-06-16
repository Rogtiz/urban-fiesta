// components/SaveVersionButton.jsx
import { useState } from "react";
import api from "../api/axios";

export default function SaveVersionButton({ fileId, getContent }) {
  const [saving, setSaving] = useState(false);
  const [status, setStatus] = useState("");
  const [description, setDescription] = useState("");

  const saveVersion = async () => {
    const content = getContent();
    if (!content || !description) {
      setStatus("Описание обязательно");
      return;
    }

    setSaving(true);
    try {
      await api.post(`/files/${fileId}/version/${description}`, content, {
        headers: {
          "Content-Type": "text/plain",
        },
      });
      setStatus("✅ Сохранено как версия");
      setDescription("");
    } catch (e) {
      console.error(e);
      setStatus("❌ Ошибка сохранения");
    } finally {
      setSaving(false);
      setTimeout(() => setStatus(""), 3000);
    }
  };

  return (
    <div className="flex flex-col items-start gap-2">
      <input
        className="bg-gray-800 border border-gray-600 text-white px-2 py-1 rounded w-64"
        placeholder="Описание версии"
        value={description}
        onChange={(e) => setDescription(e.target.value)}
      />
      <div className="flex gap-2 items-center">
        <button
          className="bg-indigo-600 text-white px-3 py-1 rounded hover:bg-indigo-700"
          onClick={saveVersion}
          disabled={saving}
        >
          💾 Сохранить как версию
        </button>
        <span className="text-sm text-gray-300">{status}</span>
      </div>
    </div>
  );
}
