<template>
  <header class="header">
    <div class="side left">
      <div class="brand" @click="goHome" title="На главную">
        Task Manager
      </div>
    </div>

    <!--навигация по страницам -->
    <nav class="nav">
      <!-- RouterLink — (SPA переход без перезагрузки) -->
      <RouterLink :to="{ name: 'home' }" class="pill">Главная</RouterLink>
      <RouterLink :to="{ name: 'tasks' }" class="pill">Задачи</RouterLink>
      <RouterLink :to="{ name: 'task-new' }" class="pill accent">Создать</RouterLink>
    </nav>
  </header>
</template>

<script setup>
/*
  useRouter — доступ к объекту роутера, чтобы делать router.push(...) из JS
*/
import { RouterLink, useRouter } from "vue-router";

const router = useRouter();

/*
  Программная навигация:
  router.push(...) меняет URL и страницу без перезагрузки
*/
function goHome() {
  router.push({ name: "home" });
}
</script>

<style scoped>
.header {
  position: sticky;
  top: 0;
  z-index: 10;
  display: grid;
  grid-template-columns: 1fr auto 1fr; /* левый / центр / правый */
  align-items: center;
  gap: 10px;
  padding: 12px 16px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.06);
  background: rgba(255, 255, 255, 0.75);
  backdrop-filter: blur(10px);
}

.side {
  display: flex;
  align-items: center;
}
.left {
  justify-content: flex-start;
}
.right {
  justify-content: flex-end;
}

.brand {
  font-weight: 800;
  letter-spacing: 0.2px;
  cursor: pointer;
  user-select: none;
}

/* Центр: меню */
.nav {
  justify-self: center;
  display: flex;
  gap: 10px;
  padding: 6px;
  border-radius: 999px;
  border: 1px solid rgba(0, 0, 0, 0.07);
  background: rgba(255, 255, 255, 0.65);
}

/* Пункты меню */
.pill {
  text-decoration: none;
  color: #222;
  padding: 8px 12px;
  border-radius: 999px;
  font-weight: 600;
  transition: transform 0.12s ease, background 0.12s ease;
}

.pill:hover {
  background: rgba(0, 0, 0, 0.05);
  transform: translateY(-1px);
}

/* Vue Router автоматически добавляет класс router-link-active */
.pill.router-link-active {
  background: rgba(22, 119, 255, 0.12);
  border: 1px solid rgba(22, 119, 255, 0.25);
}

.accent {
  background: rgba(250, 173, 20, 0.18);
  border: 1px solid rgba(250, 173, 20, 0.35);
}

.hint {
  font-size: 12px;
  opacity: 0.7;
  border: 1px solid rgba(0, 0, 0, 0.06);
  padding: 6px 10px;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.6);
}
</style>