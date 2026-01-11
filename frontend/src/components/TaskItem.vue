<template>
  <!-- Карточка одной задачи -->
  <div class="item" :class="{ done: task.completed }" :style="accentStyle">
    <div class="row">
      <div>
        <h3 class="title">
          <span class="status" :class="task.completed ? 'ok' : 'todo'">
            {{ task.completed ? "Выполнено" : "В процессе" }}
          </span>

          <!-- Заголовок задачи. Если completed=true — зачёркиваем -->
          <span class="text" :class="{ strike: task.completed }">
            {{ task.title }}
          </span>

          <!-- “Важно” как бейдж -->
          <span v-if="task.important" class="badge important">Важно</span>
        </h3>

        <!-- Доп. информация: категория, приоритет, дата -->
        <div class="meta">
          <span class="badge">{{ task.category }}</span>
          <span class="badge">priority: {{ task.priority }}</span>
          <span class="badge">создано: {{ createdAtText }}</span>
        </div>
      </div>

      <!-- Кнопки действий -->
      <div class="actions">
        <!-- RouterLink: переход на страницу редактирования -->
        <!-- Передаём параметр id в URL /tasks/:id/edit -->
        <RouterLink
          class="btn"
          :to="{ name: 'task-edit', params: { id: task.id } }"
        >
          Редактировать
        </RouterLink>

        <!-- TaskItem не меняет задачу сам.
             Он отправляет событие наверх через emit -->
        <button class="btn" @click="onToggle">
          Изменить статус
        </button>

        <!-- Удаление тоже через emit наверх -->
        <button class="btn danger" @click="$emit('delete', task.id)">
          Удалить
        </button>
      </div>
    </div>

    <p v-if="task.description" class="desc">{{ task.description }}</p>
  </div>
</template>

<script setup>
import { computed } from "vue";
import { RouterLink } from "vue-router";

/*
  props — входные данные. Родитель передаёт сюда объект задачи.
*/
const props = defineProps({
  task: { type: Object, required: true },
});

/*
  emit — события наверх (родитель их ловит).
  delete: передаём id
  toggle: передаём объект task 
*/
const emit = defineEmits(["delete", "toggle"]);

/*
  computed — “вычисляемое” значение.
   берём created_at (строка ISO от сервера) и делаем красивый текст.
*/
const createdAtText = computed(() => {
  if (!props.task.created_at) return "—";
  const d = new Date(props.task.created_at);
  if (Number.isNaN(d.getTime())) return String(props.task.created_at);
  return d.toLocaleString("ru-RU");
});

const accentStyle = computed(() => {
  const p = props.task.priority;
  const map = {
    high: "#ff4d4f",
    medium: "#faad14",
    low: "#52c41a",
  };
  return { "--accent": map[p] || "#1677ff" };
});

function onToggle() {
  // Отправляем событие наверх.
  // В TasksPage.vue  функция toggleTaskStatus(task),
  // которая сделает PUT на сервер и обновит список
  emit("toggle", props.task);
}
</script>

<style scoped>
.item {
  border: 1px solid #e6e6e6;
  border-radius: 16px;
  padding: 14px;
  background: linear-gradient(180deg, #ffffff, #fbfbfb);
  box-shadow: 0 8px 22px rgba(0, 0, 0, 0.06);
  position: relative;
  transition: transform 0.12s ease, opacity 0.12s ease;
}

/* Цветная полоска слева */
.item::before {
  content: "";
  position: absolute;
  left: 0;
  top: 12px;
  bottom: 12px;
  width: 6px;
  border-radius: 999px;
  background: var(--accent);
}

.item:hover {
  transform: translateY(-1px);
}

.item.done {
  opacity: 0.78;
}

.row {
  display: flex;
  gap: 14px;
  justify-content: space-between;
  align-items: flex-start;
  flex-wrap: wrap;
}

.title {
  margin: 0;
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
  align-items: center;
}

.text {
  font-weight: 700;
}

.strike {
  text-decoration: line-through;
}

.meta {
  margin-top: 8px;
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  opacity: 0.9;
  font-size: 12px;
}

.badge {
  border: 1px solid #e6e6e6;
  padding: 3px 10px;
  border-radius: 999px;
  background: #fff;
}

.badge.important {
  border-color: #ffd6d6;
  background: #fff2f0;
}

.status {
  font-size: 12px;
  padding: 3px 10px;
  border-radius: 999px;
  border: 1px solid #e6e6e6;
  background: #fff;
}

.status.ok {
  border-color: #b7eb8f;
  background: #f6ffed;
}

.status.todo {
  border-color: #91caff;
  background: #e6f4ff;
}

.actions {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.btn {
  padding: 8px 10px;
  border: 1px solid #e6e6e6;
  border-radius: 12px;
  background: #ffffff;
  cursor: pointer;
  text-decoration: none;
  color: #222;
}

.btn:hover {
  background: #f5f5f5;
}

.danger {
  border-color: #ffd6d6;
}

.desc {
  margin: 10px 0 0 0;
  opacity: 0.95;
}
</style>