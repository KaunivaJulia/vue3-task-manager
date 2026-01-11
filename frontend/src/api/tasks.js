
// Здесь  все HTTP-запросы к backend в одном месте
// чтобы компоненты Vue не содержали кучу axios-кода

// Импортируем заранее настроенный axios-клиент (baseURL и т.п.)
import { http } from "./http";

/**
 * GET /api/tasks
 * Получить список всех задач.
 * Возвращает массив объектов задач:
 * [
 *   { id, title, description, priority, category, important, completed, created_at },
 *   ...
 * ]
 */
export async function apiGetTasks() {
  // axios возвращает объект ответа: { data, status, headers, ... }
  // Нам нужен только data
  const { data } = await http.get("/api/tasks");
  return data;
}

/**
 * GET /api/tasks/{id}
 * Получить одну задачу по id.
 * Полезно для страницы редактирования (/tasks/:id/edit),
 * чтобы заполнить форму существующими данными.
 */
export async function apiGetTask(id) {
  // id вставляем в URL через шаблонную строку
  const { data } = await http.get(`/api/tasks/${id}`);
  return data;
}

/**
 * POST /api/tasks
 * Создать новую задачу.
 * payload — объект формы (без id и created_at, их добавит сервер):
 * {
 *   title, description, priority, category, important, completed
 * }
 */
export async function apiCreateTask(payload) {
  // Второй аргумент — тело запроса (JSON)
  const { data } = await http.post("/api/tasks", payload);
  return data; // сервер вернёт созданную задачу уже с id и created_at
}

/**
 * PUT /api/tasks/{id}
 * Обновить задачу целиком.
 */
export async function apiUpdateTask(id, payload) {
  const { data } = await http.put(`/api/tasks/${id}`, payload);
  return data; // сервер вернёт обновлённую задачу
}

/**
 * DELETE /api/tasks/{id}
 * Удалить задачу по id.
 */
export async function apiDeleteTask(id) {
  await http.delete(`/api/tasks/${id}`);
}