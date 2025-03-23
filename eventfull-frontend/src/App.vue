<template>
  <div class="wrapper">
    <!-- Навигация -->
    <nav class="navbar">
      <router-link to="/" class="nav-link">Главная</router-link>
      <router-link to="/events" class="nav-link">События</router-link>
      <router-link to="/profile" class="nav-link">Профиль</router-link>
    </nav>

    <!-- Затемнение и контент -->
    <div class="overlay">
      <router-view />
    </div>
  </div>
</template>

<style scoped>
body {
    font-family: 'Poppins', sans-serif;
    color: #fff; /* Белый цвет текста */
    margin: 0;
    padding: 0;
}

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

/* Затемнение */
.overlay {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.4);
}

</style>
