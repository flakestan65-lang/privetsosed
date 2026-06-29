from flask import Flask, request, render_template, jsonify
import subprocess
import json
import os
import re

app = Flask(__name__)

# Путь к скрипту шерлока (скачаем отдельно)
SHERLOCK_SCRIPT = "sherlock.py"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    data = request.json
    username = data.get('username', '').strip()
    platform = data.get('platform', 'all')

    if not username:
        return jsonify({'error': 'Введи хуйню, а не пустоту, блять'}), 400

    # Команда для шерлока
    cmd = ['python3', SHERLOCK_SCRIPT, username]
    if platform != 'all':
        cmd.extend(['--site', platform])

    # Запускаем и ловим вывод
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        output = result.stdout + result.stderr
        # Парсим вывод в читаемый вид
        parsed = parse_sherlock_output(output, username)
        return jsonify({'result': parsed})
    except subprocess.TimeoutExpired:
        return jsonify({'error': 'Таймаут, сука. Слишком долго ищет'}), 408
    except Exception as e:
        return jsonify({'error': f'Ошибка: {str(e)}'}), 500

def parse_sherlock_output(text, username):
    """
    Парсим вывод шерлока в человеческий вид
    """
    lines = text.split('\n')
    found = []
    not_found = []
    
    for line in lines:
        if f'[{username}]' in line:
            if 'Found:' in line:
                # Вытаскиваем сайт
                site = line.split('Found:')[1].strip()
                found.append(site)
            elif 'Not Found:' in line:
                site = line.split('Not Found:')[1].strip()
                not_found.append(site)
    
    # Если ничего не распарсилось — отдаём сырой вывод
    if not found and not not_found:
        return f"Результаты для {username}:\n{text}"
    
    result = f"🕵️ Найдено на {len(found)} ресурсах:\n"
    for site in found:
        result += f"  ✅ {site}\n"
    
    if not_found:
        result += f"\n❌ Не найдено на {len(not_found)} ресурсах:\n"
        for site in not_found[:10]:  # Показываем первые 10, чтобы не захламлять
            result += f"  ⛔ {site}\n"
        if len(not_found) > 10:
            result += f"  ... и ещё {len(not_found) - 10} сайтов\n"
    
    return result

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
