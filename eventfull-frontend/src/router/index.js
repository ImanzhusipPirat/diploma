import { createRouter, createWebHistory } from 'vue-router';
import HomePage from '../pages/HomePage.vue';
import RegisterPage from '../pages/RegisterPage.vue';
import LoginPage from '../pages/LoginPage.vue';
import ProfilePage from '../pages/ProfilePage.vue';
import EventsPage from '../pages/EventsPage.vue'; // Добавляем страницу событий

const routes = [
  { path: '/', component: HomePage },
  { path: '/register', component: RegisterPage },
  { path: '/login', component: LoginPage },
  { 
    path: '/profile', 
    component: ProfilePage,
    meta: { requiresAuth: true } // Только для авторизованных
  },
  { 
    path: '/events', 
    component: EventsPage, 
    meta: { requiresAuth: true } // Только для авторизованных
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

// Глобальная проверка авторизации
router.beforeEach((to, from, next) => {
  const isAuthenticated = localStorage.getItem('token'); // Проверяем токен
  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/login'); // Если не авторизован — кидаем на логин
  } else {
    next(); // Иначе даем пройти
  }
});

export default router;
