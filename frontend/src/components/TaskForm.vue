<template>
  <!-- Форма. @submit.prevent: не перезагружать страницу, а вызвать handleSubmit -->
  <form class="form" @submit.prevent="handleSubmit">
    <!-- TITLE -->
    <div class="field">
      <label class="label">Заголовок *</label>

      <!-- v-model.trim: связываем поле ввода с local.title и обрезаем пробелы -->
      <input
        class="input"
        type="text"
        v-model.trim="local.title"
        placeholder="Например: Сделать отчёт"
      />

      <!-- Ошибка под полем -->
      <p v-if="errors.title" class="error">{{ errors.title }}</p>
    </div>

    <!-- DESCRIPTION -->
    <div class="field">
      <label class="label">Описание</label>

      <textarea
        class="textarea"
        v-model.trim="local.description"
        placeholder="Дополнительные детали..."
        rows="4"
      ></textarea>

      <p v-if="errors.description" class="error">{{ errors.description }}</p>
    </div>

    <!-- PRIORITY -->
    <div class="field">
      <label class="label">Приоритет</label>

      <select class="select" v-model="local.priority">
        <option value="low">low</option>
        <option value="medium">medium</option>
        <option value="high">high</option>
      </select>
    </div>

    <!-- CATEGORY (radio) -->
    <div class="field">
      <label class="label">Категория</label>

      <!-- Радио-кнопки: v-model на local.category -->
      <div class="radios">
        <label class="radio">
          <input type="radio" value="work" v-model="local.category" />
          work
        </label>

        <label class="radio">
          <input type="radio" value="study" v-model="local.category" />
          study
        </label>

        <label class="radio">
          <input type="radio" value="home" v-model="local.category" />
          home
        </label>

        <label class="radio">
          <input type="radio" value="other" v-model="local.category" />
          other
        </label>
      </div>
    </div>

    <!-- IMPORTANT (checkbox) -->
    <div class="field">
      <!-- Checkbox: v-model на boolean -->
      <label class="checkbox">
        <input type="checkbox" v-model="local.important" />
        Важно
      </label>
    </div>

    <!-- COMPLETED (checkbox) -->
    <div class="field">
      <label class="checkbox">
        <input type="checkbox" v-model="local.completed" />
        Выполнено
      </label>
    </div>

    <!-- Кнопки -->
    <div class="actions">
      <!-- submitting блокирует повторные клики -->
      <button class="btn" type="submit" :disabled="submitting">
        {{ submitting ? "Сохранение..." : submitText }}
      </button>

      <!-- Отмена: отправляем событие cancel наружу -->
      <button
        class="btn secondary"
        type="button"
        @click="$emit('cancel')"
        :disabled="submitting"
      >
        Отмена
      </button>
    </div>
  </form>
</template>

<script setup>
/*
  TaskForm 
  1) принимает initialValue (начальные значения) через props
  2) заполняет локальные поля (local)
  3) валидирует
  4) при submit отправляет данные наружу: emit('submit', payload)
*/

import { reactive, watch } from "vue";

const props = defineProps({
  // initialValue — объект с начальными значениями формы
  // (для /new — пустой объект, для /edit — загруженная задача)
  initialValue: {
    type: Object,
    required: true,
  },

  // текст на кнопке submit (Создать / Сохранить)
  submitText: {
    type: String,
    default: "Сохранить",
  },

  // submitting — блокировка кнопок, когда страница делает запрос
  submitting: {
    type: Boolean,
    default: false,
  },
});

const emit = defineEmits(["submit", "cancel"]);

/*
  local — локальная реактивная копия данных формы.
  С ней работает v-model.
*/
const local = reactive({
  title: "",
  description: "",
  priority: "medium",
  category: "other",
  important: false,
  completed: false,
});

/*
  errors — объект с сообщениями ошибок для полей.
*/
const errors = reactive({
  title: "",
  description: "",
});

/*
  watch нужен, потому что initialValue может поменяться:
  - для edit: сначала initialValue пустой, потом мы загрузили задачу с сервера
    и initialValue обновился -> нужно обновить local.
*/
watch(
  () => props.initialValue,
  (val) => {
    local.title = val.title ?? "";
    local.description = val.description ?? "";
    local.priority = val.priority ?? "medium";
    local.category = val.category ?? "other";
    local.important = !!val.important;
    local.completed = !!val.completed;

    // при смене initialValue сбрасываем ошибки
    errors.title = "";
    errors.description = "";
  },
  { immediate: true, deep: true }
);

/*
  validate() — простая клиентская валидация.
  Сервер всё равно тоже валидирует (FastAPI), но пользователю удобнее видеть ошибки сразу.
*/
function validate() {
  let ok = true;

  errors.title = "";
  errors.description = "";

  if (!local.title || local.title.length < 1) {
    errors.title = "Заголовок обязателен";
    ok = false;
  }

  if (local.description && local.description.length > 2000) {
    errors.description = "Описание слишком длинное (максимум 2000 символов)";
    ok = false;
  }

  return ok;
}

/*
  handleSubmit — вызывается при отправке формы.
  Если валидация ок — отправляем данные наружу через emit('submit', payload).
*/
function handleSubmit() {
  if (!validate()) return;

  emit("submit", {
    title: local.title,
    description: local.description,
    priority: local.priority,
    category: local.category,
    important: local.important,
    completed: local.completed,
  });
}
</script>

<style scoped>
.form {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.field {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.label {
  font-weight: 600;
}

.input,
.textarea,
.select {
  padding: 10px 12px;
  border: 1px solid #ddd;
  border-radius: 10px;
  font-size: 14px;
}

.radios {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.radio {
  display: flex;
  align-items: center;
  gap: 6px;
}

.checkbox {
  display: flex;
  align-items: center;
  gap: 8px;
}

.actions {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.btn {
  padding: 10px 12px;
  border: 1px solid #ddd;
  border-radius: 10px;
  background: #fafafa;
  cursor: pointer;
}

.btn:hover {
  background: #f2f2f2;
}

.secondary {
  opacity: 0.85;
}

.error {
  color: #b00020;
  font-size: 13px;
}
</style>