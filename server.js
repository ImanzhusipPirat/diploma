require("dotenv").config();
const express = require("express");
const mongoose = require("mongoose");
const cors = require("cors");

const app = express();
app.use(express.json());
app.use(cors());
console.log("🔍 MONGO_URL:", process.env.MONGO_URL);

// Подключение к MongoDB
mongoose.connect(process.env.MONGO_URL, { useNewUrlParser: true, useUnifiedTopology: true })
  .then(() => console.log("✅ MongoDB подключен"))
  .catch(err => console.error("❌ Ошибка подключения:", err));

// **Схема пользователя**
const userSchema = new mongoose.Schema({
  name: String,
  email: String
});
const User = mongoose.model("User", userSchema);

// **Схема ивентов**
const eventSchema = new mongoose.Schema({
  title: String,
  date: Date,
  description: String
});
const Event = mongoose.model("Event", eventSchema);

// **API Маршруты**
// 🔹 Получить всех пользователей
app.get("/api/users", async (req, res) => {
  const users = await User.find();
  res.json(users);
});

// 🔹 Добавить пользователя
app.post("/api/users", async (req, res) => {
  const newUser = new User(req.body);
  await newUser.save();
  res.json({ message: "✅ Пользователь добавлен!", user: newUser });
});

// 🔹 Получить все ивенты
app.get("/api/events", async (req, res) => {
  const events = await Event.find();
  res.json(events);
});

// 🔹 Добавить ивент
app.post("/api/events", async (req, res) => {
  const newEvent = new Event(req.body);
  await newEvent.save();
  res.json({ message: "✅ Ивент создан!", event: newEvent });
});

// Запуск сервера
const PORT = process.env.PORT || 5000;
app.listen(PORT, () => console.log(`🚀 Сервер работает на http://localhost:${PORT}`));
