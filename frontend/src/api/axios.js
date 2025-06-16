import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000', // заменить на актуальное
  withCredentials: true,
  // headers: {
  //   'Content-Type': 'application/json', // 👈 важно для POST/PUT
  //   'Accept': 'application/json',       // 👈 можно добавить
  // },
});

export default api;
