import { Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function Navbar() {
  const { user, logout } = useAuth();

  const handleLogout = async () => {
    await logout();
    navigate("/login");
  };

  return (
    <nav className="bg-gray-800 text-white px-6 py-3 flex justify-between items-center">
      <div className="flex gap-4">
        <Link to="/" className="font-semibold hover:underline">DevHub</Link>
        {user && (
          <>
            <Link to="/projects" className="hover:underline">Проекты</Link>
            <Link to="/groups" className="hover:underline">Группы</Link>
            <Link to="/tasks" className="hover:underline">Задачи</Link>
            <Link to="/profile" className="hover:underline">Профиль</Link>
            <Link to="/collaborators">Коллаборации</Link>
            <Link to="/notifications">🔔</Link>
          </>
        )}
      </div>
      <div>
        {user ? (
          <div className="flex items-center gap-4">
            <span className="text-sm">Привет, {user.username}</span>
            <button onClick={handleLogout} className="bg-red-500 px-3 py-1 rounded hover:bg-red-600">
              Выйти
            </button>
          </div>
        ) : (
          <>
            <Link to="/login" className="hover:underline">Войти</Link>
            <Link to="/register" className="ml-4 hover:underline">Регистрация</Link>
          </>
        )}
      </div>
    </nav>
  );
}
