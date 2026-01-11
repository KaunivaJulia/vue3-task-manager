<template>
  <!-- Карточка-обёртка: общий внешний вид для разных страниц/блоков -->
  <div class="card">
    <!-- 1) ИМЕНОВАННЫЙ СЛОТ: header -->
    <div class="card-header">
      <slot name="header">
        <h3 class="title">Заголовок</h3>
      </slot>
    </div>

    <!-- 2) ОБЫЧНЫЙ СЛОТ -->
    <div class="card-body">
      <slot />
    </div>

    <!-- 3) SCOPED SLOT: footer -->
    <!-- Мы передаём наружу переменную now через :now="now" -->
    <div class="card-footer">
      <slot name="footer" :now="now">
        <small>Сгенерировано: {{ now }}</small>
      </slot>
    </div>
  </div>
</template>

<script setup>
/*
  now — данные, которые “живут” внутри LayoutCard.
*/
const now = new Date().toLocaleString();
</script>

<style scoped>
.card {
  border: 1px solid #e6e6e6;
  border-radius: 16px;
  padding: 16px;
  background: linear-gradient(180deg, #ffffff, #fbfbfb);
  box-shadow: 0 10px 24px rgba(0, 0, 0, 0.06);
}

.card-header {
  margin-bottom: 10px;
}

.title {
  margin: 0;
}

.card-footer {
  margin-top: 10px;
  opacity: 0.75;
}
</style>