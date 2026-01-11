import { createRouter, createWebHistory } from "vue-router";

// Страницы (pages) — компоненты, которые показываются по URL
import HomePage from "./pages/HomePage.vue";
import TasksLayout from "./pages/TasksLayout.vue";
import TasksPage from "./pages/TasksPage.vue";
import TaskNewPage from "./pages/TaskNewPage.vue";
import TaskEditPage from "./pages/TaskEditPage.vue";
import NotFoundPage from "./pages/NotFoundPage.vue";

/*
  routes — список маршрутов приложения.
  Каждый маршрут связывает path (URL) и component (что показывать).
*/
const routes = [
  /*
    Главная страница:
    URL: /
    name: 'home' — именованный маршрут
  */
  { path: "/", name: "home", component: HomePage },

  /*
    Вложенные маршруты для раздела задач.

    Родительский маршрут:
    /tasks -> компонент TasksLayout (общий каркас раздела)

    Внутри TasksLayout должен быть <RouterView />,
    куда будут вставляться дочерние страницы.
  */
  {
    path: "/tasks",
    component: TasksLayout,
    children: [
      /*
        Пустой path "" означает:
        этот маршрут будет по адресу "/tasks"
      */
      { path: "", name: "tasks", component: TasksPage },

      /*
        /tasks/new — страница создания задачи
      */
      { path: "new", name: "task-new", component: TaskNewPage },

      /*
        /tasks/:id/edit — страница редактирования
        :id — динамический параметр маршрута
        props: true — передаём params.id в компонент как prop "id"
      */
      {
        path: ":id/edit",
        name: "task-edit",
        component: TaskEditPage,
        props: true,
      },
    ],
  },

  /*
    404 (страница не найдена)
    pathMatch(.*)* — ловит любые пути, которые не подошли выше
  */
  { path: "/:pathMatch(.*)*", name: "not-found", component: NotFoundPage },
];

/*
  createWebHistory() — “красивые URL” без #.
*/
export const router = createRouter({
  history: createWebHistory(),
  routes,
});