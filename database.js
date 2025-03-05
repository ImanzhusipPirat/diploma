require("dotenv").config(); // Подключаем .env

const mongoose = require("mongoose");

const mongoUrl = process.env.MONGO_URL; // Берем URL из .env

// Подключение к MongoDB
mongoose.connect(mongoUrl, { useNewUrlParser: true, useUnifiedTopology: true })
  .then(() => console.log("✅ MongoDB подключен"))
  .catch(err => console.error("❌ Ошибка подключения:", err));

// Схема для ивентов
const eventSchema = new mongoose.Schema({
  title: String,
  date: Date,
  description: String
});

// Модель
const Event = mongoose.model("Event", eventSchema);

// Функция для создания ивента
const createEvent = async () => {
  const newEvent = new Event({
    title: "Hackathon",
    date: new Date("2025-03-10"),
    description: "Крутой IT-хакатон!"
  });

  await newEvent.save();
  console.log("🎉 Ивент создан!");
};

// Запускаем сохранение
createEvent();
