import subprocess
import os
import json
import time
import multiprocessing
from concurrent.futures import ThreadPoolExecutor, as_completed

def get_video_info(video_path):
    """Получение информации о видео через ffprobe"""
    cmd = [
        'ffprobe',
        '-v', 'quiet',
        '-print_format', 'json',
        '-show_streams',
        video_path
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        info = json.loads(result.stdout)
        video_stream = next(s for s in info['streams'] if s['codec_type'] == 'video')
        return {
            'width': int(video_stream['width']),
            'height': int(video_stream['height']),
            'fps': eval(video_stream['r_frame_rate'])
        }
    except Exception as e:
        print(f"❌ Ошибка при получении информации о видео {video_path}: {e}")
        return None

def process_single_video(args):
    """Обработка одного видео"""
    input_video, input_videos_dir, ending_video_path, output_videos_dir, index, total = args
    
    try:
        input_video_path = os.path.join(input_videos_dir, input_video)
        output_video_path = os.path.join(output_videos_dir, f"merged_{input_video}")
        
        print(f"\n🎬 Обработка видео [{index}/{total}]: {input_video}")
        start_time = time.time()

        # Получаем информацию о видео
        main_video_info = get_video_info(input_video_path)
        if not main_video_info:
            return False, input_video, "Ошибка получения информации о видео"

        # Создаем временные файлы
        temp_ending = os.path.join(output_videos_dir, f"temp_ending_{os.path.splitext(input_video)[0]}.mp4")
        temp_input = os.path.join(output_videos_dir, f"temp_input_{os.path.splitext(input_video)[0]}.mp4")

        # Оптимизированные параметры FFmpeg
        threads = multiprocessing.cpu_count()  # Получаем количество ядер процессора
        
        # Масштабирование концовки с оптимизацией
        scale_cmd = [
            'ffmpeg', '-y',
            '-i', ending_video_path,
            '-vf', f'scale={main_video_info["width"]}:{main_video_info["height"]}',
            '-r', str(main_video_info["fps"]),
            '-c:v', 'libx264',
            '-preset', 'ultrafast',  # Самый быстрый пресет
            '-tune', 'fastdecode',
            '-threads', str(threads),
            '-c:a', 'aac',
            '-b:a', '128k',  # Уменьшаем битрейт аудио
            temp_ending
        ]
        subprocess.run(scale_cmd, check=True, capture_output=True)

        # Оптимизация входного видео
        input_cmd = [
            'ffmpeg', '-y',
            '-i', input_video_path,
            '-c:v', 'libx264',
            '-preset', 'ultrafast',
            '-tune', 'fastdecode',
            '-threads', str(threads),
            '-c:a', 'aac',
            '-b:a', '128k',
            temp_input
        ]
        subprocess.run(input_cmd, check=True, capture_output=True)

        # Создаем файл со списком видео для конкатенации
        concat_file = os.path.join(output_videos_dir, f"concat_list_{os.path.splitext(input_video)[0]}.txt")
        with open(concat_file, 'w', encoding='utf-8') as f:
            f.write(f"file '{temp_input}'\n")
            f.write(f"file '{temp_ending}'\n")

        # Объединение видео с оптимизацией
        concat_cmd = [
            'ffmpeg', '-y',
            '-f', 'concat',
            '-safe', '0',
            '-i', concat_file,
            '-c:v', 'libx264',
            '-preset', 'ultrafast',
            '-tune', 'fastdecode',
            '-threads', str(threads),
            '-c:a', 'aac',
            '-b:a', '128k',
            output_video_path
        ]
        subprocess.run(concat_cmd, check=True, capture_output=True)

        # Удаляем временные файлы
        os.remove(temp_ending)
        os.remove(temp_input)
        os.remove(concat_file)
        
        processing_time = time.time() - start_time
        print(f"✓ Видео обработано за {format_time(processing_time)}")
        
        return True, input_video, processing_time
        
    except Exception as e:
        return False, input_video, str(e)

def add_ending_to_videos(input_videos_dir, ending_video_path, output_videos_dir):
    input_videos_dir = os.path.normpath(input_videos_dir)
    ending_video_path = os.path.normpath(ending_video_path)
    output_videos_dir = os.path.normpath(output_videos_dir)

    try:
        os.makedirs(output_videos_dir, exist_ok=True)
    except OSError as e:
        print(f"❌ Ошибка при создании директории {output_videos_dir}: {e}")
        return

    try:
        input_videos = [f for f in os.listdir(input_videos_dir)
                       if os.path.isfile(os.path.join(input_videos_dir, f))
                       and f.lower().endswith(('.mp4', '.mov', '.avi'))
                       and f.lower() != "ending.mp4"]
        input_videos.sort()
    except OSError as e:
        print(f"❌ Ошибка при чтении папки {input_videos_dir}: {e}")
        return

    total_videos = len(input_videos)
    print(f"Найдено видео файлов для обработки: {total_videos}")

    # Подготавливаем аргументы для параллельной обработки
    max_workers = min(multiprocessing.cpu_count(), total_videos)
    args_list = [(video, input_videos_dir, ending_video_path, output_videos_dir, i+1, total_videos) 
                 for i, video in enumerate(input_videos)]

    successful = 0
    failed = 0
    
    # Параллельная обработка видео
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(process_single_video, args) for args in args_list]
        
        for future in as_completed(futures):
            success, video_name, result = future.result()
            if success:
                successful += 1
            else:
                failed += 1
                print(f"❌ Ошибка при обработке {video_name}: {result}")

    print(f"\n📊 Итоги обработки:")
    print(f"   ✓ Успешно обработано: {successful}")
    if failed > 0:
        print(f"   ❌ Ошибок обработки: {failed}")

def format_time(seconds):
    if seconds < 60:
        return f"{seconds:.1f} сек"
    minutes = seconds // 60
    seconds = seconds % 60
    return f"{int(minutes)} мин {int(seconds)} сек"

if __name__ == "__main__":
    print("Этот файл является модулем и не предназначен для прямого запуска")
