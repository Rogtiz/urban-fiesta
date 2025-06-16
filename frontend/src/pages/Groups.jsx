import { useEffect, useState } from "react";
import api from "../api/axios";
import { Link } from "react-router-dom";

export default function Groups() {
  const [groups, setGroups] = useState([]);
  const [groupName, setGroupName] = useState("");

  useEffect(() => {
    fetchGroups();
  }, []);

  const fetchGroups = () => {
    api.get("/groups/")
      .then(res => setGroups(res.data))
      .catch(err => console.error(err));
  };

  const createGroup = async () => {
    if (!groupName.trim()) return;
    try {
      await api.post("/groups/", { name: groupName });
      setGroupName("");
      fetchGroups();
    } catch (err) {
      console.error("Ошибка создания группы", err);
    }
  };

  return (
    <div className="p-6">
      <h1 className="text-xl font-semibold mb-4">Мои группы</h1>

      <div className="mb-6 flex gap-4 items-center">
        <input
          type="text"
          placeholder="Название новой группы"
          className="input"
          value={groupName}
          onChange={(e) => setGroupName(e.target.value)}
        />
        <button onClick={createGroup} className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">
          Создать
        </button>
      </div>

      <div className="grid gap-4">
        {/*{groups.map(group => (
          <div key={group.id} className="border p-4 rounded shadow-sm bg-white">
            <h2 className="text-lg font-bold">{group.name}</h2>
            <p className="text-sm text-gray-600">ID: {group.id} | Владелец: {group.owner_id}</p>
          </div>
        ))}*/}
        {groups.length === 0 ? (
          <p className="text-sm text-gray-500">Нет групп</p>
        ) : (
          <ul className="space-y-3">
            {groups.map((group) => (
              <li
                key={group.id}
                className="bg-white p-4 shadow rounded hover:bg-gray-100"
              >
                <Link to={`/groups/${group.id}`} className="text-blue-600 font-semibold hover:underline">
                  {group.name}
                </Link>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}
