# 🎬 Видео Процессор v2.0

Простая программа для автоматического добавления концовки к видеороликам. Программа может обрабатывать сразу несколько видео, добавляя к каждому вашу концовку.

## ⚡ Быстрый старт

1. **Установите Python 3.10 или новее:**
   - Скачайте установщик с [официального сайта Python](https://www.python.org/downloads/)
   - При установке обязательно поставьте ✅ галочку "Add Python to PATH"
   - Нажмите "Install Now"

2. **Установите FFmpeg:**
   - Скачайте архив FFmpeg для Windows: [скачать FFmpeg](https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-full.7z)
   - Распакуйте архив
   - Переименуйте распакованную папку в `ffmpeg`
   - Переместите папку `ffmpeg` в корень диска C (путь должен быть `C:\ffmpeg`)
   - Добавьте FFmpeg в переменные среды Windows:
     1. Нажмите Win + R
     2. Введите `cmd`
     3. Вставьте команду: `setx PATH "%PATH%;C:\ffmpeg\bin"`
     4. Перезапустите компьютер

3. **Установите программу:**
   - Скачайте все файлы программы в одну папку
   - Откройте командную строку в этой папке
   - Выполните команду: `pip install questionary subprocess.run`

## 🎯 Как использовать

1. **Подготовьте файлы:**
   - Поместите видео для обработки в папку с программой
   - Поместите вашу концовку в ту же папку и назовите её `ending.mp4`

2. **Запустите программу:**
   - Дважды кликните на файл `main.py`
   - ИЛИ откройте командную строку в папке с программой и введите:
     ```
     python main.py
     ```

3. **Работа с программой:**
   - Используйте стрелки ↑↓ для навигации по меню
   - Enter для выбора
   - Следуйте инструкциям на экране

## 📋 Поддерживаемые форматы

- Видео: MP4, MOV, AVI
- Концовка: должна быть в формате MP4

## ⚠️ Ограничения

- Максимум 100 видео за раз
- Концовка должна называться именно `ending.mp4`
- Нужно свободное место на диске (примерно в 3 раза больше размера исходных видео)

## 🔍 Решение проблем

1. **Ошибка "Python не найден":**
   - Переустановите Python, обязательно поставив галочку "Add Python to PATH"

2. **Ошибка "FFmpeg не найден":**
   - Убедитесь, что FFmpeg находится в `C:\ffmpeg`
   - Перезапустите компьютер после установки FFmpeg

3. **Программа сразу закрывается:**
   - Запустите через командную строку, чтобы увидеть ошибку

## 💡 Советы

- Перед обработкой большого количества видео, протестируйте на одном
- Используйте справку в программе (кнопка "Показать справку")
- Проверяйте наличие свободного места на диске 
