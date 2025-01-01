import video_merger
import os
import subprocess
import time
import questionary
from questionary import Style

# Создаем стиль для questionary
custom_style = Style([
    ('question', 'fg:#0066ff bold'),
    ('answer', 'fg:#00cc00 bold'),
    ('pointer', 'fg:#ff3300 bold'),
    ('highlighted', 'fg:#00cc00 bold'),
    ('selected', 'fg:#00cc00 bold'),
    ('separator', 'fg:#0066ff'),
    ('instruction', 'fg:#0066ff'),
    ('text', 'fg:#ffffff'),
])

def check_ffmpeg():
    """Проверка наличия FFmpeg в системе"""
    try:
        result = subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True)
        print("✓ FFmpeg найден:", result.stdout.split('\n')[0])
        return True
    except FileNotFoundError:
        return False

def list_video_files(directory):
    """Показать список видео файлов в директории"""
    video_extensions = ('.mp4', '.mov', '.avi', '.MP4', '.MOV', '.AVI')
    files = []
    for file in os.listdir(directory):
        if any(file.endswith(ext) for ext in video_extensions) and file.lower() != "ending.mp4":
            files.append(file)
    return sorted(files)

def print_separator():
    print("\n" + "─" * 70 + "\n")

def format_time(seconds):
    """Форматирование времени в читаемый вид"""
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    if hours > 0:
        return f"{int(hours)}ч {int(minutes)}м {int(seconds)}с"
    elif minutes > 0:
        return f"{int(minutes)}м {int(seconds)}с"
    else:
        return f"{int(seconds)}с"

def show_help():
    """Показать справку по использованию программы"""
    while True:
        print("\n" + "═" * 70)
        print("║" + " " * 28 + "СПРАВКА" + " " * 34 + "║")
        print("═" * 70)

        help_section = questionary.select(
            "Выберите раздел справки:",
            choices=[
                "📝 Общее описание",
                "🛠️ Подготовка к работе",
                "📋 Поддерживаемые форматы",
                "⚠️ Ограничения",
                "📊 Результаты работы",
                "⌨️ Горячие клавиши",
                "↩️ Вернуться в главное меню"
            ],
            style=custom_style
        ).ask()

        if help_section == "📝 Общее описание":
            print("\n" + "─" * 70)
            print("📝 ОБЩЕЕ ОПИСАНИЕ")
            print("─" * 70)
            print("Программа предназначена для автоматического добавления концовки")
            print("к видеороликам. Она может обрабатывать сразу несколько видео,")
            print("добавляя к каждому указанную концовку.")
            print("\nОсобенности:")
            print("• Автоматическое масштабирование концовки под размер видео")
            print("• Сохранение качества исходного видео")
            print("• Параллельная обработка для ускорения работы")
            print("• Поддержка различных форматов видео")

        elif help_section == "🛠️ Подготовка к работе":
            print("\n" + "─" * 70)
            print("🛠️ ПОДГОТОВКА К РАБОТЕ")
            print("─" * 70)
            print("1. Подготовьте файлы:")
            print("   • Поместите видео для обработки в папку со скриптом")
            print("   • Поместите файл концовки (ending.mp4) в ту же папку")
            print("\n2. Убедитесь, что установлен FFmpeg")
            print("\n3. Запустите программу и следуйте инструкциям")

        elif help_section == "📋 Поддерживаемые форматы":
            print("\n" + "─" * 70)
            print("📋 ПОДДЕРЖИВАЕМЫЕ ФОРМАТЫ")
            print("─" * 70)
            print("Видео файлы:")
            print("• MP4 (.mp4)")
            print("• MOV (.mov)")
            print("• AVI (.avi)")
            print("\nФайл концовки:")
            print("• Должен быть в формате MP4")
            print("• Должен иметь имя 'ending.mp4'")

        elif help_section == "⚠️ Ограничения":
            print("\n" + "─" * 70)
            print("⚠️ ОГРАНИЧЕНИЯ")
            print("─" * 70)
            print("• Максимальное количество видео: 100")
            print("• Имя файла концовки: строго 'ending.mp4'")
            print("• Требуется установленный FFmpeg")
            print("• Достаточно свободного места на диске")
            print("  (примерно в 3 раза больше размера исходных видео)")

        elif help_section == "📊 Результаты работы":
            print("\n" + "─" * 70)
            print("📊 РЕЗУЛЬТАТЫ РАБОТЫ")
            print("─" * 70)
            print("• Создается папка 'output' для готовых видео")
            print("• Имена обработанных файлов: merged_[исходное имя]")
            print("• Сохраняется оригинальное качество видео")
            print("• Концовка масштабируется под размер основного видео")
            print("• Программа показывает статистику обработки")

        elif help_section == "⌨️ Горячие клавиши":
            print("\n" + "─" * 70)
            print("⌨️ ГОРЯЧИЕ КЛАВИШИ")
            print("─" * 70)
            print("↑/↓     - Навигация по меню")
            print("Enter   - Выбор пункта меню")
            print("Esc     - Возврат/Отмена")
            print("Q       - Выход из программы")

        else:  # Вернуться в главное меню
            break

        print("\n" + "─" * 70)
        if not questionary.confirm(
            "Показать другой раздел справки?",
            default=True,
            style=custom_style
        ).ask():
            break

def show_welcome():
    """Показать приветственный экран"""
    print("\n" + "═" * 70)
    print("║" + " " * 24 + "ВИДЕО ПРОЦЕССОР v2.0" + " " * 24 + "║")
    print("═" * 70)

def main():
    try:
        show_welcome()
        
        # Проверяем наличие FFmpeg
        if not check_ffmpeg():
            print("\n❌ ОШИБКА: FFmpeg не найден!")
            if questionary.confirm(
                "Хотите установить FFmpeg?",
                default=True,
                style=custom_style
            ).ask():
                # Здесь можно добавить автоматическую установку FFmpeg
                print("Пожалуйста, скачайте FFmpeg с официального сайта: https://ffmpeg.org/download.html")
            return

        # Получаем путь к папке скрипта
        script_dir = os.path.dirname(os.path.abspath(__file__))
        input_videos_dir = script_dir
        ending_video_path = os.path.join(script_dir, "ending.mp4")
        output_videos_dir = os.path.join(script_dir, "output")

        # Проверяем наличие ending.mp4
        if not os.path.exists(ending_video_path):
            print("\n❌ Файл 'ending.mp4' не найден!")
            return

        # Показываем список найденных видео
        videos = list_video_files(input_videos_dir)
        if not videos:
            print("\n❌ В папке нет видео файлов для обработки!")
            return

        if len(videos) > 100:
            print("\n❌ Превышен лимит видео (максимум 100)!")
            return

        # Показываем информацию о найденных файлах
        print("\n📁 Рабочая директория:", script_dir)
        print(f"\n📽️ Найдено видео для обработки ({len(videos)}):")
        for i, video in enumerate(videos, 1):
            print(f"   {i}. {video}")

        print_separator()

        while True:
            action = questionary.select(
                "Выберите действие:",
                choices=[
                    "✨ Начать обработку",
                    "📖 Показать справку",
                    "❌ Выйти"
                ],
                style=custom_style
            ).ask()

            if action == "✨ Начать обработку":
                # Подтверждение параметров
                print("\n📋 Параметры обработки:")
                print(f"   • Количество видео: {len(videos)}")
                print(f"   • Концовка: ending.mp4")
                print(f"   • Папка для готовых видео: {os.path.basename(output_videos_dir)}")
                
                if questionary.confirm(
                    "\nНачать обработку видео?",
                    default=True,
                    style=custom_style
                ).ask():
                    print("\n🎬 Начинаем обработку видео...")
                    start_time = time.time()
                    
                    video_merger.add_ending_to_videos(input_videos_dir, ending_video_path, output_videos_dir)
                    
                    total_time = time.time() - start_time
                    print_separator()
                    print(f"✨ Обработка успешно завершена!")
                    print(f"⏱️ Общее время обработки: {format_time(total_time)}")
                    print(f"📁 Готовые видео находятся в папке: {output_videos_dir}")
                    break
            
            elif action == "📖 Показать справку":
                show_help()
            
            else:  # Выход
                print("\n👋 До свидания!")
                return

    except Exception as e:
        print(f"\n❌ ОШИБКА: {str(e)}")
        print("\nПодробности ошибки:")
        import traceback
        print(traceback.format_exc())

    print_separator()
    input("Нажмите Enter для выхода...")

if __name__ == "__main__":
    main() 