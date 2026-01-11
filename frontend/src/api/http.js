import axios from "axios";

/*
  baseURL:
  - локально: VITE_API_URL=http://localhost:8000
  - в docker: VITE_API_URL= (пусто), тогда запросы идут на тот же домен: /api/...
  Важно: используем ?? вместо ||, чтобы пустая строка "" сохранялась.
*/
const baseURL = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

export const http = axios.create({
  baseURL,
  timeout: 10000,
});
