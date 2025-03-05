<template>
    <div class="flex items-center justify-center min-h-screen bg-gray-100">
      <div class="bg-white p-6 rounded-lg shadow-lg w-96">
        <h2 class="text-2xl font-semibold text-center mb-4">Вход</h2>
        <form @submit.prevent="loginUser" class="space-y-4">
          <input 
            v-model="username"
            type="text"
            placeholder="Имя пользователя"
            required
            class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
          />
          <input 
            v-model="password"
            type="password"
            placeholder="Пароль"
            required
            class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
          />
          <button 
            type="submit"
            class="w-full bg-green-500 text-white py-2 rounded-lg hover:bg-green-600 transition"
          >
            Войти
          </button>
        </form>
        <p v-if="message" :class="{'text-red-500': error, 'text-green-500': !error}" class="mt-4 text-center">
          {{ message }}
        </p>
      </div>
    </div>
  </template>
  
  <script>
  import axios from "axios";
  
  export default {
    data() {
      return {
        username: "",
        password: "",
        message: "",
        error: false
      };
    },
    methods: {
      async loginUser() {
        try {
          const res = await axios.post("http://127.0.0.1:8000/login", {
            username: this.username,
            password: this.password
          });
  
          localStorage.setItem("token", res.data.access_token); // Сохраняем токен
          this.message = "Вход успешен! Перенаправление...";
          this.error = false;
          setTimeout(() => this.$router.push("/profile"), 2000); // Переход на профиль
        } catch (error) {
          this.message = error.response?.data?.detail || "Ошибка входа";
          this.error = true;
        }
      }
    }
  };
  </script>
  