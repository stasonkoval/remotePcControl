import os
import pyautogui
import ctypes

from flask import Flask, render_template_string

app = Flask(__name__)

@app.route('/')
@app.route('/index')
@app.route('/help')
def index():
    return render_template_string('''
        <html>
            <head>
                <title>Справка по серверу</title>
            </head>
            <body>
                <h1>Доступные страницы</h1>
                <ul>
                    <li><a href="/">Главная</a></li>
                    <li><a href="/suspend">Перевести систему в спящий режим</a></li>
                    <li><a href="/space">Нажать пробел</a></li>
                </ul>
            </body>
        </html>
    ''')

@app.route('/suspend', methods=['GET'])
def suspend_system():
    try:
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
        return "System is being suspended", 200
    except Exception as e:
        return str(e), 500

@app.route('/space', methods=['GET'])
def press_space():
    try:
        pyautogui.press('space')
        return "Space key pressed", 200
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    # Получаем хэндл окна консоли
    whnd = ctypes.windll.kernel32.GetConsoleWindow()

    # Если окно есть, скрываем его
    if whnd != 0:
        ctypes.windll.user32.ShowWindow(whnd, 0)
        
    # Запуск сервера
    app.run(host='0.0.0.0', port=8888)
    
    