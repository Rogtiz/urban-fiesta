import { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";
import api from "../../api/axios";

export default function VerifyEmail() {
  const [params] = useSearchParams();
  const [status, setStatus] = useState("Проверка...");

  useEffect(() => {
    const token = params.get("token");
    if (token) {
      api
        .get(`/users/verify-email?token=${token}`)
        .then(() => setStatus("Email успешно подтвержден."))
        .catch(() => setStatus("Ошибка при подтверждении email."));
    } else {
      setStatus("Токен не найден.");
    }
  }, [params]);

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <div className="bg-white p-6 rounded shadow-md w-96 text-center">
        <h2 className="text-xl font-semibold mb-4">Подтверждение Email</h2>
        <p>{status}</p>
        <a href="/login" className="mt-4 block text-blue-600 hover:underline">
          Перейти ко входу
        </a>
      </div>
    </div>
  );
}
