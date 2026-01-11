<template>
  <div class="list">
    <!-- v-if: если список задач пустой — показываем сообщение -->
    <p v-if="tasks.length === 0" class="empty">
      Список пуст. Создайте задачу 
    </p>

    <!-- v-for: перебираем массив tasks и рисуем компонент TaskItem для каждой задачи -->
    <!-- :key обязателен: помогает Vue правильно обновлять DOM при удалении/сортировке -->
    <TaskItem
      v-for="task in tasks"
      :key="task.id"
      :task="task"
      @delete="forwardDelete"
      @toggle="forwardToggle"
    />
  </div>
</template>

<script setup>
/*
  TaskList — “прослойка” между страницей (TasksPage) и отдельной карточкой (TaskItem)
  - получает tasks через props
  - показывает список (v-for)
  - отображает пустое состояние (v-if)
  - принимает события от TaskItem и пробрасывает их наверх (emit)
*/

import TaskItem from "./TaskItem.vue";

/*
  props: список задач приходит от родителя.
*/
defineProps({
  tasks: {
    type: Array,
    required: true,
  },
});

/*
  emit: события наружу, чтобы TasksPage мог обработать:
  - delete (удаление)
  - toggle (переключение статуса)
*/
const emit = defineEmits(["delete", "toggle"]);

/*
  Проброс событий:
  Эти функции просто “пересылают” событие вверх
*/
function forwardDelete(id) {
  emit("delete", id);
}

function forwardToggle(task) {
  emit("toggle", task);
}
</script>

<style scoped>
.list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.empty {
  opacity: 0.75;
  padding: 10px 0;
}
</style>