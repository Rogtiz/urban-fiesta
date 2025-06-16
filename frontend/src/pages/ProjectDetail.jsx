import { useEffect, useState } from "react";
import { useParams, Link, useNavigate } from "react-router-dom";
import api from "../api/axios";
import { useAuth } from "../context/AuthContext";

export default function ProjectDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { user } = useAuth();

  const [project, setProject] = useState(null);
  const [tasks, setTasks] = useState([]);
  const [group, setGroup] = useState(null);
  const [groupMembers, setGroupMembers] = useState([]);
  const [files, setFiles] = useState([]);

  const isOwner = project?.owner_id === user?.id;

  useEffect(() => {
    loadProjectData();
  }, [id]);

  const loadProjectData = async () => {
    try {
      const res = await api.get(`/projects/${id}`);
      setProject(res.data);

      api.get(`/projects/${id}/files`).then((res) => setFiles(res.data));

      // Загрузка задач проекта с учётом пользователя
      const taskRes = await api.get(`/projects/${id}/tasks`);
      setTasks(taskRes.data);

      // Загрузка группы и участников, если есть
      if (res.data.group_id) {
        const groupRes = await api.get(`/groups/${res.data.group_id}`);
        setGroup(groupRes.data);
        setGroupMembers(groupRes.data.members || []);
      }
    } catch (err) {
      console.error("Ошибка при загрузке проекта:", err);
    }
  };

  if (!project) return <p className="p-4">Загрузка проекта...</p>;

  return (
    <div className="p-6 space-y-4">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold">{project.name}</h1>
        {isOwner && (
          <div className="space-x-2">
            <button
              onClick={() => navigate(`/projects/${id}/edit`)}
              className="bg-yellow-500 text-white px-3 py-1 rounded"
            >
              ✏️ Редактировать
            </button>
            <button
              onClick={() => navigate(`/projects/${id}/tags`)}
              className="bg-purple-600 text-white px-3 py-1 rounded"
            >
              🏷 Управлять тэгами
            </button>
          </div>
        )}
      </div>
      <p className="text-gray-600">{project.description}</p>
      <p className="text-sm text-gray-400">ID проекта: {project.id}</p>

      <hr />

      <h2 className="text-xl font-semibold">Задачи проекта</h2>
      {tasks.length === 0 ? (
        <p className="text-sm text-gray-500">Нет задач</p>
      ) : (
        <ul className="space-y-2">
          {tasks.map((task) => (
            <li
              key={task.id}
              className="bg-white shadow rounded p-3 hover:bg-gray-100"
            >
              <Link to={`/tasks/${task.id}`} className="text-blue-600 font-medium">
                {task.title}
              </Link>
              <p className="text-sm text-gray-500">{task.description}</p>
            </li>
          ))}
        </ul>
      )}

      {group && (
        <>
          <hr />
          <h2 className="text-xl font-semibold">Группа: {group.name}</h2>
          <Link
            to={`/groups/${group.id}`}
            className="text-sm text-blue-600 hover:underline"
          >
            Перейти к группе →
          </Link>

          <h3 className="mt-2 font-semibold">Участники:</h3>
          <ul className="list-disc ml-6 text-sm text-gray-700">
            {groupMembers.map((member) => (
              <li key={member.id}>{member.username} ({member.email})</li>
            ))}
          </ul>
        </>
      )}

      <hr />

      <h2 className="text-xl font-semibold mb-2">Файлы проекта</h2>
      {files.length === 0 ? (
        <p className="text-sm text-gray-500">Файлов пока нет.</p>
      ) : (
        <ul className="space-y-2">
          {files.map((file) => (
            <li
              key={file.id}
              className="bg-gray-100 rounded px-4 py-2 hover:bg-gray-200"
            >
              <Link to={`/editor/${id}/${file.id}`} className="text-blue-600 underline">
                {file.filename}
              </Link>
              <br/>
              <br/>
              <a
                href={`${api.defaults.baseURL}/files/${file.id}/download`}
                className="text-sm text-blue-600 hover:underline"
              >
                ⬇️ Скачать
              </a>
              <Link
                to={`/files/${file.id}/versions`}
                className="text-green-600 hover:underline"
              >
                📜 Версии файла
              </Link>
            </li>
          ))}
        </ul>
      )}

      <UploadForm projectId={project.id} onUploaded={() => api.get(`/projects/${id}/files`).then((res) => setFiles(res.data.files))} />
    </div>
  );
}

function UploadForm({ projectId, onUploaded }) {
  const [file, setFile] = useState(null);

  const handleUpload = async () => {
    if (!file) return;
    const formData = new FormData();
    formData.append("uploaded_file", file);
    try {
      await api.post(`/files/upload/${projectId}`, formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setFile(null);
      onUploaded();
    } catch (err) {
      console.error("Ошибка загрузки файла", err);
    }
  };

  return (
    <div className="mt-6">
      <h3 className="text-md font-semibold mb-2">Загрузить файл</h3>
      <input
        type="file"
        onChange={(e) => setFile(e.target.files[0])}
        className="mb-2"
      />
      <br />
      <button
        onClick={handleUpload}
        className="bg-blue-600 text-white px-4 py-1 rounded hover:bg-blue-700"
      >
        Загрузить
      </button>
    </div>
  );
}

