import logging
import os



try:
    if os.path.exists('test.jpg'):
        os.remove('test.jpg')




except Exception as e:
    logging.info(f'Ошибка при удалении файла {'test.jpg'}. {e}')
