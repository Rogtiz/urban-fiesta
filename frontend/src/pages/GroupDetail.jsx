import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import api from "../api/axios";
import { useAuth } from "../context/AuthContext";

export default function GroupDetail() {
  const { id } = useParams(); // group id
  const { user } = useAuth();
  const navigate = useNavigate();

  const [group, setGroup] = useState(null);
  const [members, setMembers] = useState([]);
  const [openUsers, setOpenUsers] = useState([]);
  const [sentInvites, setSentInvites] = useState([]);

  const [editingName, setEditingName] = useState(false);
  const [newName, setNewName] = useState("");

  const isOwner = group?.owner_id === user?.id;

  useEffect(() => {
    loadGroup();
    if (isOwner) {
      loadOpenUsers();
    }
  }, [id]);

  const loadGroup = async () => {
    try {
      const res = await api.get(`/groups/${id}`);
      setGroup(res.data);
      setMembers(res.data.members || []);
      setNewName(res.data.name);
    } catch (err) {
      console.error("Ошибка загрузки группы:", err);
    }
  };

  const loadOpenUsers = async () => {
    try {
      const [openRes, invitesRes] = await Promise.all([
        api.get("/users/open_to_collab"),
        api.get(`/groups/${id}/invitations/sent`),
      ]);
      setOpenUsers(openRes.data);
      setSentInvites(invitesRes.data.map((inv) => inv.receiver_id));
    } catch (err) {
      console.error("Ошибка при загрузке доступных пользователей", err);
    }
  };

  const inviteUser = async (userId) => {
    try {
      await api.post("/groups/invitations/send", {
        group_id: parseInt(id),
        receiver_id: userId,
        sender_id: user.id,
        message: "Присоединяйся к нашей группе!",
      });
      setSentInvites((prev) => [...prev, userId]);
      alert("Приглашение отправлено!");
    } catch (err) {
      console.error("Ошибка приглашения пользователя", err);
    }
  };

  const leaveGroup = async () => {
    try {
      await api.post(`/groups/${id}/leave`);
      navigate("/groups");
    } catch (err) {
      console.error("Ошибка выхода из группы:", err);
    }
  };

  const removeMember = async (memberId) => {
    try {
      await api.delete(`/groups/${id}/members/${memberId}`);
      await loadGroup();
    } catch (err) {
      console.error("Ошибка удаления участника:", err);
    }
  };

  const updateGroupName = async () => {
    try {
      await api.put(`/groups/${id}`, { name: newName });
      setEditingName(false);
      await loadGroup();
    } catch (err) {
      console.error("Ошибка обновления названия группы:", err);
    }
  };

  if (!group) return <div className="p-4">Загрузка группы...</div>;

  return (
    <div className="p-6 space-y-4 max-w-3xl mx-auto">
      <div className="flex justify-between items-center">
        {editingName ? (
          <div className="flex gap-2 items-center">
            <input
              value={newName}
              onChange={(e) => setNewName(e.target.value)}
              className="border px-2 py-1 rounded"
            />
            <button onClick={updateGroupName} className="btn-blue">
              Сохранить
            </button>
            <button onClick={() => setEditingName(false)} className="text-red-500">
              Отмена
            </button>
          </div>
        ) : (
          <>
            <h1 className="text-2xl font-bold">{group.name}</h1>
            {isOwner && (
              <button onClick={() => setEditingName(true)} className="btn-blue">
                ✏️ Редактировать
              </button>
            )}
          </>
        )}
      </div>

      <h2 className="text-lg font-semibold">Участники группы:</h2>
      <ul className="list-disc ml-6 space-y-1 text-sm">
        {members.map((member) => (
          <li key={member.id} className="flex justify-between items-center">
            {member.username} ({member.email})
            {isOwner && member.id !== user.id && (
              <button
                onClick={() => removeMember(member.id)}
                className="text-red-500 text-xs hover:underline"
              >
                Удалить
              </button>
            )}
          </li>
        ))}
      </ul>

      {!isOwner && (
        <button
          onClick={leaveGroup}
          className="bg-red-600 text-white px-4 py-1 rounded mt-4"
        >
          Покинуть группу
        </button>
      )}

      {isOwner && (
        <div className="mt-6">
          <h3 className="text-md font-semibold mb-2">👥 Пригласить участников</h3>
          {openUsers.length === 0 ? (
            <p className="text-sm text-gray-500">Нет пользователей, готовых к коллаборации</p>
          ) : (
            <ul className="space-y-2">
              {openUsers
                .filter(
                  (u) => !members.some((m) => m.id === u.id) && !sentInvites.includes(u.id)
                )
                .map((user) => (
                  <li key={user.id} className="flex justify-between items-center">
                    <span>
                      {user.full_name || user.username} ({user.email})
                    </span>
                    <button
                      onClick={() => inviteUser(user.id)}
                      className="bg-blue-600 text-white text-sm px-3 py-1 rounded"
                    >
                      ➕ Пригласить
                    </button>
                  </li>
                ))}
            </ul>
          )}
        </div>
      )}
    </div>
  );
}
