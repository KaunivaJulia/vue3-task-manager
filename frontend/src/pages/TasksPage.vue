<template>
  <LayoutCard>
    <template #header>
      <h2>Список задач</h2>
    </template>

    <!-- Панель управления: фильтр + сортировка + кнопка создать -->
    <div class="controls">
      <label class="control">
        Фильтр:
        <select v-model="statusFilter">
          <option value="all">Все</option>
          <option value="completed">Выполненные</option>
          <option value="active">Невыполненные</option>
        </select>
      </label>

      <label class="control">
        Сортировка:
        <select v-model="sortMode">
          <option value="date_desc">По дате (сначала новые)</option>
          <option value="date_asc">По дате (сначала старые)</option>
          <option value="title_asc">По алфавиту (А→Я)</option>
          <option value="title_desc">По алфавиту (Я→А)</option>
        </select>
      </label>

      <RouterLink class="create" :to="{ name: 'task-new' }">
        + Создать
      </RouterLink>
    </div>

    <!-- Ошибка загрузки/операций -->
    <p v-if="errorMessage" class="error">{{ errorMessage }}</p>

    <!-- TaskList принимает массив задач и отдаёт события delete/toggle -->
    <TaskList
      :tasks="sortedAndFilteredTasks"
      @delete="removeTask"
      @toggle="toggleTaskStatus"
    />

    <!-- scoped slot footer у LayoutCard: получаем now -->
    <template #footer="{ now }">
      <small>Отображение обновлено: {{ now }}</small>
    </template>
  </LayoutCard>
</template>

<script setup>
/*
  TasksPage.vue — контейнерная страница.
  - состояние (tasks, фильтры, сортировка, ошибки)
  - загрузка данных с сервера (GET)
  - действия над задачами (DELETE, PUT)
  - computed для фильтрации/сортировки
  - watch для отслеживания изменений фильтра/сортировки
*/

import { ref, computed, onMounted, watch } from "vue";
import { RouterLink } from "vue-router";

import LayoutCard from "../layouts/LayoutCard.vue";
import TaskList from "../components/TaskList.vue";

// API функции (axios внутри)
import { apiGetTasks, apiDeleteTask, apiUpdateTask } from "../api/tasks";

/* --------------------------
   STATE (состояние страницы)
--------------------------- */

// Список задач
const tasks = ref([]);

// UI-состояния управления
const statusFilter = ref("all");     // all | completed | active
const sortMode = ref("date_desc");   // варианты сортировки

// Сообщение об ошибках (например если backend не доступен)
const errorMessage = ref("");

/* --------------------------
   LOAD (загрузка данных)
--------------------------- */

async function loadTasks() {
  errorMessage.value = "";

  try {
    // GET /api/tasks
    tasks.value = await apiGetTasks();
  } catch (e) {
    // Частая причина: backend не запущен, неправильный baseURL, CORS
    errorMessage.value =
      "Не удалось загрузить задачи. Проверь, что backend запущен";
  }
}

onMounted(() => {
  loadTasks();
});

/* --------------------------
   COMPUTED: фильтр/сортировка
--------------------------- */

/*
  computed filteredTasks:
  - если выбрали completed -> оставляем только completed=true
  - если active -> completed=false
  - иначе все
*/
const filteredTasks = computed(() => {
  if (statusFilter.value === "completed") {
    return tasks.value.filter((t) => t.completed);
  }
  if (statusFilter.value === "active") {
    return tasks.value.filter((t) => !t.completed);
  }
  return tasks.value;
});

const sortedAndFilteredTasks = computed(() => {
  const arr = [...filteredTasks.value];

  if (sortMode.value === "date_desc") {
    // created_at — ISO строка -> сравнение строк подходит
    arr.sort((a, b) => String(b.created_at).localeCompare(String(a.created_at)));
  } else if (sortMode.value === "date_asc") {
    arr.sort((a, b) => String(a.created_at).localeCompare(String(b.created_at)));
  } else if (sortMode.value === "title_asc") {
    arr.sort((a, b) => String(a.title).localeCompare(String(b.title)));
  } else if (sortMode.value === "title_desc") {
    arr.sort((a, b) => String(b.title).localeCompare(String(a.title)));
  }

  return arr;
});

/* --------------------------
   WATCH: отслеживание фильтров
--------------------------- */

/*
  watch 
  - сохранять фильтр/сортировку в localStorage
  - сбрасывать ошибки
  - логировать изменения
*/
watch([statusFilter, sortMode], ([newStatus, newSort], [oldStatus, oldSort]) => {
  // eslint-disable-next-line no-console
  console.log("Filter/sort changed:", { oldStatus, oldSort, newStatus, newSort });

  errorMessage.value = "";
});

/* --------------------------
   ACTIONS: DELETE и PUT
--------------------------- */

/*
  DELETE /api/tasks/{id}
  Удаляем задачу на сервере и обновляем локальный список.
*/
async function removeTask(id) {
  errorMessage.value = "";

  try {
    await apiDeleteTask(id);
    tasks.value = tasks.value.filter((t) => t.id !== id);
  } catch (e) {
    errorMessage.value = "Не удалось удалить задачу.";
  }
}

/*
  PUT /api/tasks/{id}
  Переключаем completed.
  - UI меняется сразу
  - потом подтверждаем с сервера
  - если ошибка — откатываем
*/
async function toggleTaskStatus(task) {
  errorMessage.value = "";

  const previous = task.completed;

  // 1) UI обновляем сразу
  tasks.value = tasks.value.map((t) =>
    t.id === task.id ? { ...t, completed: !t.completed } : t
  );

  try {
    // 2) Собираем payload целиком 
    const payload = {
      title: task.title,
      description: task.description,
      priority: task.priority,
      category: task.category,
      important: task.important,
      completed: !previous,
    };

    const updated = await apiUpdateTask(task.id, payload);

    // 3) Подменяем задачу данными с сервера
    tasks.value = tasks.value.map((t) => (t.id === task.id ? updated : t));
  } catch (e) {
    // 4) Откат если ошибка
    tasks.value = tasks.value.map((t) =>
      t.id === task.id ? { ...t, completed: previous } : t
    );
    errorMessage.value = "Не удалось обновить статус задачи (PUT).";
  }
}
</script>

<style scoped>
.controls {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
  align-items: end;
  margin-bottom: 12px;
}

.control {
  display: flex;
  flex-direction: column;
  gap: 6px;
  font-size: 14px;
}

select {
  padding: 8px 10px;
  border: 1px solid #ddd;
  border-radius: 10px;
  background: #fff;
}

.create {
  padding: 8px 10px;
  border: 1px solid rgba(0,0,0,0.08);
  border-radius: 12px;
  text-decoration: none;
  color: #222;
  background: rgba(255,255,255,0.8);
  box-shadow: 0 8px 18px rgba(0,0,0,0.06);
}

.create:hover {
  background: #f2f2f2;
}

.error {
  border: 1px solid #f0b4b4;
  background: #fff5f5;
  padding: 10px;
  border-radius: 10px;
  margin-bottom: 10px;
}
</style>