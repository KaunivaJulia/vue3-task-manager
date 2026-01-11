<template>
  <LayoutCard>
    <!-- Именованный слот header -->
    <template #header>
      <h2>Добро пожаловать!</h2>
    </template>

    <p>
      Это «Менеджер задач» на Vue 3 + FastAPI
      Здесь ты сможешь создавать, редактировать и удалять задачи.
    </p>

    <button class="btn" @click="goToTasks">
      Перейти к задачам
    </button>
  </LayoutCard>
</template>

<script setup>
import { useRouter } from "vue-router";
import LayoutCard from "../layouts/LayoutCard.vue";

const router = useRouter();

function goToTasks() {
  // программная навигация по имени маршрута
  router.push({ name: "tasks" });
}
</script>

<style scoped>
.btn {
  margin-top: 12px;
  padding: 10px 12px;
  border: 1px solid #ddd;
  border-radius: 10px;
  background: #fafafa;
  cursor: pointer;
}
.btn:hover {
  background: #f2f2f2;
}
</style>
