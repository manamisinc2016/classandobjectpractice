import hashlib
import time


class User:
    def __init__(self, nickname: str, password: str, age: int):
        self.nickname = nickname
        self.password = self.hash_password(password)
        self.age = age

    def hash_password(self, password: str) -> int:
        """Хэширует пароль для хранения"""
        return int(hashlib.sha256(password.encode()).hexdigest(), 16)

    def __str__(self):
        return f"User({self.nickname}, age={self.age})"


class Video:
    def __init__(self, title: str, duration: int, adult_mode: bool = False):
        self.title = title
        self.duration = duration
        self.time_now = 0
        self.adult_mode = adult_mode

    def __str__(self):
        return f"Video({self.title}, duration={self.duration}, adult_mode={self.adult_mode})"

    def __repr__(self):
        return self.__str__()


class UrTube:
    def __init__(self):
        self.users = []
        self.videos = []
        self.current_user = None

    def log_in(self, nickname: str, password: str):
        """Авторизация пользователя по никнейму и паролю"""
        for user in self.users:
            if user.nickname == nickname and user.password == User(nickname, password, 0).password:
                self.current_user = user
                print(f"Пользователь {nickname} вошёл в систему")
                return
        print("Неверный логин или пароль")

    def register(self, nickname: str, password: str, age: int):
        """Регистрация нового пользователя"""
        for user in self.users:
            if user.nickname == nickname:
                print(f"Пользователь {nickname} уже существует")
                return
        new_user = User(nickname, password, age)
        self.users.append(new_user)
        self.current_user = new_user
        print(f"Пользователь {nickname} успешно зарегистрирован и вошёл в систему")

    def log_out(self):
        """Выход текущего пользователя"""
        if self.current_user:
            print(f"Пользователь {self.current_user.nickname} вышел из системы")
        self.current_user = None

    def add(self, *videos: Video):
        """Добавление видео в библиотеку, если его ещё нет"""
        for video in videos:
            if video.title not in [v.title for v in self.videos]:
                self.videos.append(video)
                print(f"Видео '{video.title}' добавлено")
            else:
                print(f"Видео '{video.title}' уже существует и не будет добавлено")

    def get_videos(self, search_word: str):
        """Поиск видео по ключевому слову"""
        search_word = search_word.lower()
        result = [video.title for video in self.videos if search_word in video.title.lower()]
        return result

    def watch_video(self, video_title: str):
        """Просмотр видео по названию"""
        if not self.current_user:
            print("Войдите в аккаунт, чтобы смотреть видео")
            return

        video = next((v for v in self.videos if v.title == video_title), None)
        if not video:
            print("Видео не найдено")
            return

        if video.adult_mode and self.current_user.age < 18:
            print("Вам нет 18 лет, пожалуйста покиньте страницу")
            return

        print(f"Начинаем просмотр видео: {video.title}")
        for second in range(video.time_now + 1, video.duration + 1):
            print(second, end=' ', flush=True)
            time.sleep(0.1)  # Замедление времени для демонстрации
        print("\nКонец видео")
        video.time_now = 0  # Сброс времени просмотра


# --- Тестовый код --- #

ur = UrTube()

# Создание видео
v1 = Video('Лучший язык программирования 2024 года', 10)
v2 = Video('Для чего девушкам парень программист?', 10, adult_mode=True)

# Добавление видео
ur.add(v1, v2)

# Проверка поиска
print(ur.get_videos('лучший'))  # ['Лучший язык программирования 2024 года']
print(ur.get_videos('ПРОГ'))  # ['Лучший язык программирования 2024 года', 'Для чего девушкам парень программист?']

# Попытка посмотреть видео без авторизации
ur.watch_video('Для чего девушкам парень программист?')  # Войдите в аккаунт, чтобы смотреть видео

# Регистрация и попытка посмотреть видео
ur.register('vasya_pupkin', 'lolkekcheburek', 13)  # Регистрация и вход
ur.watch_video('Для чего девушкам парень программист?')  # Вам нет 18 лет, пожалуйста покиньте страницу

# Регистрация нового пользователя
ur.register('urban_pythonist', 'iScX4vIJClb9YQavjAgF', 25)  # Регистрация и вход
ur.watch_video('Для чего девушкам парень программист?')  # Видео воспроизводится

# Попытка зарегистрировать уже существующего пользователя
ur.register('vasya_pupkin', 'F8098FM8fjm9jmi', 55)  # Пользователь vasya_pupkin уже существует

# Проверка текущего пользователя
print(ur.current_user)  # urban_pythonist

# Попытка воспроизвести несуществующее видео
ur.watch_video('Лучший язык программирования 2024 года!')  # Видео не найдено
