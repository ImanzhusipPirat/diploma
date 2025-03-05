<template>
    <div class="container mx-auto p-6">
      <h2 class="text-2xl font-semibold mb-4">События</h2>
  
      <form @submit.prevent="createEvent" class="space-y-4">
        <input v-model="newEvent.title" type="text" placeholder="Название" class="border p-2 w-full" required />
        <input v-model="newEvent.description" type="text" placeholder="Описание" class="border p-2 w-full" required />
        <input v-model="newEvent.date" type="date" class="border p-2 w-full" required />
        <input v-model="newEvent.location" type="text" placeholder="Место" class="border p-2 w-full" required />
        <button type="submit" class="bg-blue-500 text-white p-2 rounded">Создать событие</button>
      </form>
  
      <ul class="mt-6 space-y-2">
        <li v-for="event in events" :key="event._id" class="p-4 border rounded flex justify-between items-center">
          <div>
            <h3 class="text-lg font-semibold">{{ event.title }}</h3>
            <p>{{ event.description }}</p>
            <p><strong>Дата:</strong> {{ event.date }}</p>
            <p><strong>Место:</strong> {{ event.location }}</p>
          </div>
          <button @click="deleteEvent(event._id)" class="bg-red-500 text-white p-2 rounded">Удалить</button>
        </li>
      </ul>
    </div>
  </template>
  
  <script>
  import axios from "axios";
  
  export default {
    data() {
      return {
        newEvent: { title: "", description: "", date: "", location: "" },
        events: [],
      };
    },
    methods: {
      async createEvent() {
        const token = localStorage.getItem("token");
        await axios.post("http://127.0.0.1:8000/events", this.newEvent, {
          headers: { Authorization: `Bearer ${token}` }
        });
        this.loadEvents();
      },
      async loadEvents() {
        const res = await axios.get("http://127.0.0.1:8000/events");
        this.events = res.data;
      },
      async deleteEvent(eventId) {
        const token = localStorage.getItem("token");
        await axios.delete(`http://127.0.0.1:8000/events/${eventId}`, {
          headers: { Authorization: `Bearer ${token}` }
        });
        this.loadEvents();
      },
    },
    mounted() {
      this.loadEvents();
    },
  };
  </script>
  