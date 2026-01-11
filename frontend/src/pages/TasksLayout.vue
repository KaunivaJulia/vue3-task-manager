<template>
  <div class="wrap">
    <h2>Раздел задач</h2>

    <!-- Здесь будут отображаться дочерние страницы (/tasks, /tasks/new, /tasks/:id/edit) -->
    <RouterView />
  </div>
</template>

<script setup>
import { RouterView } from "vue-router";
</script>

<style scoped>
.wrap {
  display: flex;
  flex-direction: column;
  gap: 14px;
}
</style>
