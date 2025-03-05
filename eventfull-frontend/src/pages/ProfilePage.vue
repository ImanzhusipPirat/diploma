<template>
    <div class="flex flex-col items-center justify-center min-h-screen bg-gray-100">
      <div class="bg-white p-6 rounded-lg shadow-lg w-96">
        <h2 class="text-2xl font-semibold text-center mb-4">Личный кабинет</h2>
        <p v-if="user">Добро пожаловать, <strong>{{ user.username }}</strong>!</p>
        <button @click="logout" class="w-full bg-red-500 text-white py-2 rounded-lg hover:bg-red-600 transition mt-4">
          Выйти
        </button>
      </div>
    </div>
  </template>
  
  <script>
  import axios from "axios";
  
  export default {
    data() {
      return {
        user: null,
        message: ""
      };
    },
    async mounted() {
      try {
        const token = localStorage.getItem("token");
        if (!token) {
          this.$router.push("/login"); // Если нет токена – на логин
          return;
        }
  
        const res = await axios.get("http://127.0.0.1:8000/protected", {
          headers: { Authorization: `Bearer ${token}` }
        });
  
        this.user = res.data;
      } catch (error) {
        this.message = "Ошибка загрузки профиля";
        this.$router.push("/login"); // Если ошибка – на логин
      }
    },
    methods: {
      logout() {
        localStorage.removeItem("token"); // Удаляем токен
        this.$router.push("/login"); // Перенаправляем на логин
      }
    }
  };
  </script>
  