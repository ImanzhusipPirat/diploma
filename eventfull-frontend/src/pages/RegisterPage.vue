<template>
  <div class="container d-flex justify-content-center align-items-center vh-100">
    <div class="card p-4 shadow-lg" style="max-width: 400px; width: 100%">
      <h2 class="text-center mb-3">Регистрация</h2>
      <form @submit.prevent="registerUser">
        <div class="mb-3">
          <label class="form-label">Имя пользователя</label>
          <input v-model="username" type="text" class="form-control" required />
        </div>
        <div class="mb-3">
          <label class="form-label">Email</label>
          <input v-model="email" type="email" class="form-control" required />
        </div>
        <div class="mb-3">
          <label class="form-label">Пароль</label>
          <input v-model="password" type="password" class="form-control" required />
        </div>
        <button type="submit" class="btn btn-primary w-100">Зарегистрироваться</button>
        <p v-if="message" class="text-center text-danger mt-3">{{ message }}</p>
      </form>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      username: "",
      email: "",
      password: "",
      message: ""
    };
  },
  methods: {
    async registerUser() {
      try {
        const res = await axios.post("http://127.0.0.1:8000/register", {
          username: this.username,
          email: this.email,
          password: this.password
        });
        this.message = res.data.message;
      } catch (error) {
        this.message = error.response?.data?.detail || "Ошибка регистрации";
      }
    }
  }
};
</script>
