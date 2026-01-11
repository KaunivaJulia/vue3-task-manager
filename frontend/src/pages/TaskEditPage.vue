<template>
  <LayoutCard>
    <template #header>
      <h2>Редактировать задачу #{{ id }}</h2>
    </template>

    <p v-if="loading">Загрузка...</p>
    <p v-if="errorMessage" class="error">{{ errorMessage }}</p>

    <TaskForm
      v-if="!loading"
      :initialValue="initial"
      submitText="Сохранить"
      :submitting="submitting"
      @submit="saveTask"
      @cancel="goBack"
    />
  </LayoutCard>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";

import LayoutCard from "../layouts/LayoutCard.vue";
import TaskForm from "../components/TaskForm.vue";

import { apiGetTask, apiUpdateTask } from "../api/tasks";

const props = defineProps({
  id: {
    type: [String, Number],
    required: true,
  },
});

const router = useRouter();

const loading = ref(true);
const submitting = ref(false);
const errorMessage = ref("");

const initial = ref({
  title: "",
  description: "",
  priority: "medium",
  category: "other",
  important: false,
  completed: false,
});

function goBack() {
  router.push({ name: "tasks" });
}

onMounted(async () => {
  errorMessage.value = "";
  loading.value = true;

  try {
    const task = await apiGetTask(props.id);
    initial.value = task;
  } catch (e) {
    errorMessage.value = "Не удалось загрузить задачу. Возможно, такого id нет.";
  } finally {
    loading.value = false;
  }
});

async function saveTask(payload) {
  errorMessage.value = "";
  submitting.value = true;

  try {
    await apiUpdateTask(props.id, payload);
    router.push({ name: "tasks" });
  } catch (e) {
    errorMessage.value = "Не удалось сохранить задачу.";
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
