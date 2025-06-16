import { useAuth } from "../context/AuthContext";

export default function EmailWarning() {
  const { user } = useAuth();

  if (!user || user.is_verified) return null;

  return (
    <div className="bg-yellow-100 text-yellow-800 p-2 text-center text-sm">
      Внимание: вы не подтвердили свой email. Пожалуйста, проверьте почту.
    </div>
  );
}
