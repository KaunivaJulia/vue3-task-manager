<template>
  <LayoutCard>
    <template #header>
      <h2>Создать задачу</h2>
    </template>

    <!-- Если ошибка (например backend не доступен) -->
    <p v-if="errorMessage" class="error">{{ errorMessage }}</p>

    <!-- TaskForm — универсальная форма
         здесь используем её для POST (создание) -->
    <TaskForm
      :initialValue="initial"
      submitText="Создать"
      :submitting="submitting"
      @submit="createTask"
      @cancel="goBack"
    />
  </LayoutCard>
</template>

<script setup>
/*
  TaskNewPage.vue — страница создания задачи.
  - задаёт initialValue (пустые значения)
  - принимает submit от TaskForm (payload)
  - делает POST через apiCreateTask(payload)
  - после успеха навигирует на /tasks
*/

import { ref } from "vue";
import { useRouter } from "vue-router";

import LayoutCard from "../layouts/LayoutCard.vue";
import TaskForm from "../components/TaskForm.vue";
import { apiCreateTask } from "../api/tasks";

const router = useRouter();

// блокировка кнопки и защита от двойных запросов
const submitting = ref(false);

// сообщение об ошибке
const errorMessage = ref("");

// начальные значения формы для создания
const initial = ref({
  title: "",
  description: "",
  priority: "medium",
  category: "other",
  important: false,
  completed: false,
});

function goBack() {
  // программная навигация
  router.push({ name: "tasks" });
}

/*
  createTask(payload) вызывается, когда TaskForm сделал emit('submit', payload).
  payload — объект с полями задачи (title, description, priority, category, important, completed).
*/
async function createTask(payload) {
  errorMessage.value = "";
  submitting.value = true;

  try {
    // POST /api/tasks
    await apiCreateTask(payload);

    // после успешного создания — возвращаемся к списку
    router.push({ name: "tasks" });
  } catch (e) {
    // если backend не доступен/ошибка сети/422 и т.п.
    errorMessage.value = "Не удалось создать задачу. Проверь backend и данные формы.";
  } finally {
    submitting.value = false;
  }
}
</script>

<style scoped>
.error {
  border: 1px solid #f0b4b4;
  background: #fff5f5;
  padding: 10px;
  border-radius: 10px;
  margin-bottom: 10px;
}
</style>