import logging

# Настраиваем логгер
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Добавляем файловый хендлер логов
file_handler = logging.FileHandler('bot.log')
logger.addHandler(file_handler)

# Добавляем консольный хендлер логов
console_handler = logging.StreamHandler()
logger.addHandler(console_handler)
logging.basicConfig(level=logging.INFO)
