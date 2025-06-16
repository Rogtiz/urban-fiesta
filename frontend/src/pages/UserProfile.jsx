import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import api from "../api/axios";
import { useAuth } from "../context/AuthContext";

export default function UserProfile() {
  const navigate = useNavigate();
  const { id } = useParams();
  const [profile, setProfile] = useState(null);
  const { user } = useAuth();
  const [groups, setGroups] = useState([]);

  useEffect(() => {
    api.get(`/users/collaborators/${id}`).then((res) => setProfile(res.data));
    api.get("/groups/owned").then((res) => setGroups(res.data)); // только группы, где user — владелец
  }, [id]);

  const sendInvite = async (groupId) => {
    await api.post("/groups/invitations/send", {
      group_id: groupId,
      receiver_id: profile.id,
      sender_id: user.id,
      message: "Присоединяйся к нашей группе!"
    });
    alert("Приглашение отправлено!");
  };

  if (!profile) return <p>Загрузка...</p>;

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-2">{profile.full_name || profile.username}</h1>
      <p className="text-gray-600">{profile.description}</p>
      <p className="text-sm text-gray-400 mt-1">{profile.email}</p>

      <div className="mt-4">
        <h3 className="text-md font-semibold mb-2">Теги:</h3>
        <div className="flex flex-wrap gap-2">
          {profile.tags?.map((tag, i) => (
            <span key={i} className="bg-blue-100 text-blue-700 text-sm px-2 py-1 rounded">{tag}</span>
          ))}
        </div>
      </div>

      {groups.length > 0 && (
        <div className="mt-6">
          <h3 className="font-semibold">Пригласить в свою группу:</h3>
          <div className="flex flex-wrap gap-2 mt-2">
            {groups.map((g) => (
              <button
                key={g.id}
                onClick={() => sendInvite(g.id)}
                className="flex items-center gap-2 bg-blue-600 hover:bg-blue-700 text-white text-sm font-medium px-4 py-1 rounded transition"
              >
                <span>Пригласить в {g.name}</span>
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}