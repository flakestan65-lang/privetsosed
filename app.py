from flask import Flask, request, render_template, jsonify
from sherlock_wrapper import SherlockSearch
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# Создаём экземпляр поисковика
searcher = SherlockSearch()

@app.route('/')
def index():
    """Главная страница"""
    return render_template('index.html')

@app.route('/api/search', methods=['POST'])
def search_api():
    """
    API эндпоинт для поиска
    Ожидает JSON: {"username": "test", "platform": "github"}
    """
    try:
        data = request.get_json()
        username = data.get('username', '').strip()
        platform = data.get('platform', 'all')
        
        if not username:
            return jsonify({
                'status': 'error',
                'message': 'Введи логин, долбаёб!'
            }), 400
        
        # Запускаем поиск
        result = searcher.search(username, platform)
        
        return jsonify({
            'status': 'success',
            'data': result
        })
        
    except Exception as e:
        app.logger.error(f'Ошибка: {str(e)}')
        return jsonify({
            'status': 'error',
            'message': f'Нахуй всё сломалось: {str(e)}'
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
