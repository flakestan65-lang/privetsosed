import subprocess
import json
import re
import os
from typing import Dict, List, Tuple

class SherlockSearch:
    """Класс для работы с оригинальным шерлоком"""
    
    def __init__(self, sherlock_path='sherlock.py'):
        self.sherlock_path = sherlock_path
        self._check_sherlock()
    
    def _check_sherlock(self):
        """Проверяем, существует ли файл шерлока"""
        if not os.path.exists(self.sherlock_path):
            raise FileNotFoundError(
                f"Шерлок не найден по пути {self.sherlock_path}\n"
                "Скачай с https://github.com/sherlock-project/sherlock"
            )
    
    def search(self, username: str, platform: str = 'all') -> Dict:
        """
        Выполняет поиск
        
        Args:
            username: логин для поиска
            platform: конкретная платформа или 'all'
        
        Returns:
            Dict с результатами
        """
        # Собираем команду
        cmd = ['python3', self.sherlock_path, username]
        
        if platform != 'all':
            cmd.extend(['--site', platform])
        
        # Добавляем JSON вывод для удобного парсинга
        cmd.append('--print-found')
        
        try:
            # Запускаем процесс
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60  # 60 секунд на поиск
            )
            
            # Парсим вывод
            return self._parse_output(result.stdout + result.stderr, username)
            
        except subprocess.TimeoutExpired:
            return {
                'status': 'timeout',
                'message': 'Поиск занял слишком много времени, сука!'
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Ошибка при выполнении: {str(e)}'
            }
    
    def _parse_output(self, output: str, username: str) -> Dict:
        """
        Парсит вывод шерлока в читаемый формат
        """
        lines = output.split('\n')
        found_sites = []
        not_found_sites = []
        errors = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Ищем паттерны
            if f'[{username}]' in line:
                # Разбираем строку
                if 'Found:' in line:
                    site = line.split('Found:')[1].strip()
                    # Убираем лишние символы
                    site = re.sub(r'\[.*?\]', '', site).strip()
                    found_sites.append(site)
                elif 'Not Found:' in line:
                    site = line.split('Not Found:')[1].strip()
                    site = re.sub(r'\[.*?\]', '', site).strip()
                    not_found_sites.append(site)
                elif 'Error:' in line:
                    error = line.split('Error:')[1].strip()
                    errors.append(error)
        
        # Формируем результат
        result = {
            'status': 'success',
            'username': username,
            'total_found': len(found_sites),
            'found_sites': found_sites,
            'not_found': not_found_sites[:20],  # Ограничиваем список
            'errors': errors,
            'raw_output': output[:1000]  # Для дебага
        }
        
        # Генерируем человекочитаемый текст
        result['formatted'] = self._format_result(result)
        
        return result
    
    def _format_result(self, data: Dict) -> str:
        """Форматирует результат в строку для вывода"""
        username = data['username']
        found = data['found_sites']
        not_found = data['not_found']
        
        if not found and not not_found:
            return f"🔍 По запросу '{username}' ничего не найдено, блять!"
        
        text = f"🕵️ РЕЗУЛЬТАТЫ ДЛЯ '{username}':\n\n"
        text += f"✅ НАЙДЕНО: {len(found)} сайтов\n"
        for site in found[:15]:  # Показываем первые 15
            text += f"  ▸ {site}\n"
        if len(found) > 15:
            text += f"  ... и ещё {len(found) - 15} сайтов\n"
        
        if not_found:
            text += f"\n❌ НЕ НАЙДЕНО: {len(not_found)} сайтов\n"
            for site in not_found[:5]:
                text += f"  ▸ {site}\n"
            if len(not_found) > 5:
                text += f"  ... и ещё {len(not_found) - 5} сайтов\n"
        
        return text
