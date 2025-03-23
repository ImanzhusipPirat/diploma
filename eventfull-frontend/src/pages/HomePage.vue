<template>
  <div class="wrapper">
    <!-- Навигация -->
    <nav class="navbar">
      <router-link to="/" class="nav-link">Главная</router-link>
      <router-link to="/events" class="nav-link">События</router-link>
      <router-link to="/profile" class="nav-link">Профиль</router-link>
    </nav>

    <!-- Контент -->
    <div class="overlay">
      <div class="content">
        <h1>Добро пожаловать в Eventfull</h1>
        <p>Создавайте, находите и участвуйте в лучших событиях!</p>
        <div class="buttons">
          <router-link to="/register" class="btn btn-primary">Регистрация</router-link>
          <router-link to="/login" class="btn btn-outline-light">Вход</router-link>
        </div>
      </div>
    </div>

    <!-- Динамический контент -->
    <router-view />
  </div>
</template>

<script>
export default {
  name: "HomePage"
};
</script>

<style scoped>
/* Контейнер с фоном */
.wrapper {
  position: relative;
  width: 100vw;
  height: 100vh;
  background: url('@/assets/background.jpg') no-repeat center center/cover;
  display: flex;
  flex-direction: column;
  align-items: center;
}

/* Навигация */
.navbar {
  position: absolute;
  top: 10px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 20px;
  font-size: 18px;
}

.nav-link {
  color: white;
  text-decoration: none;
}

.nav-link:hover {
  text-decoration: underline;
}

/* Затемнение для контента */
.overlay {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.4);
}

/* Контент */
.content {
  background: rgba(0, 0, 0, 0.7);
  padding: 20px 40px;
  border-radius: 10px;
  text-align: center;
  color: white;
}

/* Кнопки */
.buttons {
  display: flex;
  gap: 15px;
  justify-content: center;
}
</style>
