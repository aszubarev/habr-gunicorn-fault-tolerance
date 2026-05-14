import socket
from datetime import datetime


class HTTP11Client:
    """
    Низкоуровневый HTTP/1.1 клиент с поддержкой постоянных соединений
    """

    def __init__(self, host, port=80, client_name : str = ''):
        """
        Инициализация клиента

        Args:
            host: хост (например, 'example.com')
            port: порт (80 для HTTP)
        """
        self.host = host
        self.port = port
        self.socket = None
        self.connected = False
        self._client_name = client_name

    @property
    def now(self):
        return datetime.now()

    def connect(self):
        """
        Устанавливает TCP соединение с сервером
        """
        if self.connected:
            print(f"[{self.now}][{self._client_name}]! Соединение уже установлено")
            return

        print(f"[{self.now}][{self._client_name}][Соединение] Создаем TCP сокет и подключаемся к {self.host}:{self.port}...")

        try:
            # Создаем TCP сокет
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # Устанавливаем таймаут для операций (опционально)
            self.socket.settimeout(30)

            # Устанавливаем соединение
            self.socket.connect((self.host, self.port))
            self.connected = True

            print(f"[{self.now}][{self._client_name}][Соединение] ✓ TCP соединение установлено")

        except socket.gaierror:
            print(f"[{self.now}][{self._client_name}][Соединение] ✗ Ошибка: не удалось разрешить имя хоста '{self.host}'")
            raise
        except socket.error as e:
            print(f"[{self.now}][{self._client_name}][Соединение] ✗ Ошибка сокета: {e}")
            raise
        except Exception as e:
            print(f"[{self.now}][{self._client_name}][Соединение] ✗ Неожиданная ошибка: {e}")
            raise

    def do_request(self, method='GET', path='/', headers=None, body=None):
        """
        Отправляет HTTP запрос и возвращает ответ

        Args:
            method: HTTP метод (GET, POST, PUT, DELETE и т.д.)
            path: путь запроса (например, '/index.html')
            headers: словарь с дополнительными заголовками
            body: тело запроса (для POST/PUT методов)

        Returns:
            dict: словарь с заголовками ответа и телом
        """
        if not self.connected:
            raise Exception("Соединение не установлено. Вызовите connect() сначала")

        # Формируем HTTP/1.1 запрос
        request = self._build_request(method, path, headers, body)

        print(f"[{self.now}][{self._client_name}][Запрос {method} {path}] Отправляем HTTP/1.1 запрос...")

        request_start_time = datetime.now()
        try:
            self.socket.send(request.encode('utf-8'))
            print(f"[{self.now}][{self._client_name}][Запрос {method} {path}]] ✓ Запрос отправлен")
        except socket.error as e:
            print(f"[{self.now}][{self._client_name}][Запрос {method} {path}]] ✗ Ошибка при отправке: {e}")
            raise

        # Получаем ответ
        print(f"[{self.now}][{self._client_name}][Ответ] Читаем ответ...")
        response = self._read_response()

        request_end_time = datetime.now()
        request_duration = request_end_time - request_start_time
        request_duration.total_seconds()

        print(f"[{self.now}][{self._client_name}][Ответ][{request_duration.total_seconds():.2f}] Получен. Статус {response['headers']['_status_line']}")

        return response

    def _build_request(self, method, path, headers=None, body=None):
        """
        Формирует HTTP/1.1 запрос в виде строки
        """
        # Стартовая строка
        request = f"{method} {path} HTTP/1.1\r\n"

        # Базовые заголовки
        request += f"Host: {self.host}\r\n"
        request += f"User-Agent: LowLevelHTTP11Client/1.0\r\n"

        # Используем keep-alive для постоянного соединения
        request += f"Connection: keep-alive\r\n"

        # Добавляем заголовки для тела запроса, если есть
        if body:
            request += f"Content-Length: {len(body)}\r\n"
            if headers and 'Content-Type' in headers:
                request += f"Content-Type: {headers['Content-Type']}\r\n"
            else:
                request += f"Content-Type: application/x-www-form-urlencoded\r\n"

        # Добавляем пользовательские заголовки
        if headers:
            for key, value in headers.items():
                # Пропускаем Content-Type, если уже добавили
                if key.lower() == 'content-type' and body:
                    continue
                request += f"{key}: {value}\r\n"

        # Завершаем заголовки
        request += f"\r\n"

        # Добавляем тело запроса, если есть
        if body:
            request += body

        return request

    def _read_response(self):
        """
        Читает HTTP ответ из сокета
        Возвращает словарь с заголовками и телом
        """
        response_data = b''

        # Читаем данные, пока не получим полный ответ
        # Для HTTP/1.1 нужно анализировать заголовки, чтобы знать, когда остановиться

        # Сначала читаем заголовки
        headers_data = b''
        while True:
            chunk = self.socket.recv(1)  # Читаем по байту для простоты
            if not chunk:
                # break
                raise Exception("Соединение разорвано")

            headers_data += chunk

            # Проверяем, достигли ли конца заголовков (\r\n\r\n)
            if headers_data.endswith(b'\r\n\r\n'):
                break

        # Парсим заголовки
        headers = self._parse_headers(headers_data.decode('utf-8', errors='replace'))

        # Определяем длину тела ответа
        content_length = None
        chunked = False

        for key, value in headers.items():
            if key.lower() == 'content-length':
                content_length = int(value)
            elif key.lower() == 'transfer-encoding' and 'chunked' in value.lower():
                chunked = True

        # Читаем тело ответа
        body = b''

        if chunked:
            # Читаем chunked encoding
            body = self._read_chunked_body()
        elif content_length is not None:
            # Читаем фиксированное количество байт
            remaining = content_length
            while remaining > 0:
                chunk = self.socket.recv(min(4096, remaining))
                if not chunk:
                    raise Exception(f"Неожиданный конец соединения, ожидалось {remaining} байт")
                body += chunk
                remaining -= len(chunk)
        else:
            # Нет информации о длине, читаем пока соединение не закроется
            # Это не идеально для keep-alive, но работает
            while True:
                try:
                    chunk = self.socket.recv(4096)
                    if not chunk:
                        break
                    body += chunk
                except socket.timeout:
                    # Таймаут может означать конец данных
                    break

        # Декодируем тело, если это текст
        body_text = self._decode_body(body, headers)

        return {
            'headers': headers,
            'raw_body': body,
            'body': body_text
        }

    def _parse_headers(self, headers_str):
        """
        Парсит строку заголовков HTTP ответа
        """
        lines = headers_str.split('\r\n')

        # Первая строка - статус
        status_line = lines[0]

        headers = {'_status_line': status_line}

        # Остальные строки - заголовки
        for line in lines[1:]:
            if ':' in line:
                key, value = line.split(':', 1)
                headers[key.strip()] = value.strip()

        return headers

    def _read_chunked_body(self):
        """
        Читает тело ответа в формате chunked encoding
        """
        body = b''

        while True:
            # Читаем размер чанка
            chunk_size_line = b''
            while True:
                byte = self.socket.recv(1)
                if not byte:
                    raise Exception("Неожиданный конец соединения при чтении размера чанка")
                chunk_size_line += byte
                if chunk_size_line.endswith(b'\r\n'):
                    break

            # Парсим размер чанка (шестнадцатеричный)
            chunk_size = int(chunk_size_line.strip().split(b';')[0], 16)

            # Если размер 0, это последний чанк
            if chunk_size == 0:
                # Пропускаем завершающие \r\n после последнего чанка
                self.socket.recv(2)
                break

            # Читаем сам чанк
            chunk = b''
            remaining = chunk_size
            while remaining > 0:
                data = self.socket.recv(min(4096, remaining))
                if not data:
                    raise Exception(f"Неожиданный конец соединения при чтении чанка")
                chunk += data
                remaining -= len(data)

            body += chunk

            # Пропускаем \r\n после чанка
            self.socket.recv(2)

        return body

    def _decode_body(self, body_bytes, headers):
        """
        Декодирует тело ответа в строку, пытаясь определить кодировку
        """
        # Пытаемся определить кодировку из заголовка Content-Type
        content_type = headers.get('Content-Type', '')
        charset = 'utf-8'  # по умолчанию

        if 'charset=' in content_type:
            charset = content_type.split('charset=')[-1].split(';')[0].strip()

        try:
            return body_bytes.decode(charset)
        except (UnicodeDecodeError, LookupError):
            # Пробуем другие распространенные кодировки
            for encoding in ['utf-8', 'latin-1', 'cp1251', 'iso-8859-1']:
                try:
                    return body_bytes.decode(encoding)
                except UnicodeDecodeError:
                    continue
            # Если ничего не помогло, возвращаем с заменой
            return body_bytes.decode('utf-8', errors='replace')

    def close(self):
        """
        Закрывает TCP соединение
        """
        if self.socket:
            print(f"\n[Закрытие] Закрываем TCP соединение...")
            self.socket.close()
            self.socket = None
            self.connected = False
            print(f"[Закрытие] ✓ Соединение закрыто")

    def __enter__(self):
        """Поддержка контекстного менеджера"""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Автоматическое закрытие при выходе из контекста"""
        self.close()
