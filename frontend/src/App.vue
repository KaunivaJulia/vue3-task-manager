<template>
  <div class="app">
    <AppHeader />

    <main class="main">
      <RouterView />
    </main>

    <AppFooter />
  </div>
</template>

<script setup>
import { RouterView } from "vue-router";
import AppHeader from "./components/AppHeader.vue";
import AppFooter from "./components/AppFooter.vue";
</script>

<style scoped>
.app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;

  background:
    radial-gradient(1200px 600px at 15% 0%, rgba(22, 119, 255, 0.10), transparent),
    radial-gradient(900px 500px at 85% 10%, rgba(250, 173, 20, 0.10), transparent),
    radial-gradient(800px 500px at 50% 100%, rgba(82, 196, 26, 0.08), transparent),
    #ffffff;
}

.main {
  flex: 1;
  padding: 18px;
  max-width: 960px;
  width: 100%;
  margin: 0 auto;
}
</style>
