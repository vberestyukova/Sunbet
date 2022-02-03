# Project for IoT course on the Faculty of Applied Mathematics and Control Processes of Saint Petersburg University 2020

Для развертывания необходим python3, далее: \
pip3 install -r requirements.txt \
gunicorn app:app --bind 0.0.0.0:8082 --worker-class aiohttp.GunicornWebWorker 

Сервис предоставляет пользовательсктий интерфейс и API для взаимодействия платы NodeMCU с ним. \
Исходный код, выполняемый на плате, можно увидеть в репозитории: \
https://github.com/MenacingDwarf/SunbedFree-NodeMCU
