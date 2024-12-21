from models import session, User, Post

# Добавление данных в таблицу Users
def add_users():
    users = [
        User(username="Виталик", email="userVit@zavod.com", password="gjdjw23rd"),
        User(username="Генадий", email="userGena2@zavod.com", password="fjw22fccv"),
        User(username="Семёныч", email="userSemen@zavod.com", password="pakgr23"),
        User(username="Михалыч", email="Mihal@zavod.com", password="pgk3212df"),
        User(username="Никита", email="Nikitos@zavod.com", password="password"),
    ]
    session.add_all(users)
    session.commit()
    print("Пользователи добавлены.")

# Добавление данных в таблицу Posts
def add_posts():
    posts = [
        Post(title="Резать", content="Режь метал пока горячо", user_id=1),
        Post(title="Плавить", content="Плавь метал чтобы резать", user_id=3),
        Post(title="Мыть", content="надо помыть цех", user_id=2),
        Post(title="Тягать чугун", content="Принеси чугун на переплавку", user_id=4),
        Post(title="Ничего не делать", content="Отдыхайте работяги", user_id=4),
    ]
    session.add_all(posts)
    session.commit()
    print("Задачи добавлены.")

# Извлечение всех пользователей
def get_all_users():
    users = session.query(User).all()
    for user in users:
        print(f"ID: {user.id}, Пользователь: {user.username}, Email: {user.email}")

# Извлечение всех постов с информацией о пользователях
def get_all_posts():
    posts = session.query(Post).all()
    for post in posts:
        print(f"ID Задачи: {post.id}, Суть: {post.title}, Ответственный: {post.user.username}")

# Извлечение постов конкретного пользователя
def get_posts_by_user(user_id):
    posts = session.query(Post).filter(Post.user_id == user_id).all()
    for post in posts:
        print(f"ID Задачи: {post.id}, Заголовок: {post.title}, Описание: {post.content}")

# Обновление email пользователя
def update_user_email(user_id, new_email):
    user = session.query(User).filter(User.id == user_id).first()
    if user:
        user.email = new_email
        session.commit()
        print(f"Email пользователя с ID {user_id} обновлен.")
    else:
        print("Пользователь не найден.")

# Обновление контента поста
def update_post_content(post_id, new_content):
    post = session.query(Post).filter(Post.id == post_id).first()
    if post:
        post.content = new_content
        session.commit()
        print(f"Описание задачи с ID {post_id} обновлено.")
    else:
        print("Задача не найдена.")

# Удаление поста
def delete_post(post_id):
    post = session.query(Post).filter(Post.id == post_id).first()
    if post:
        session.delete(post)
        session.commit()
        print(f"Задача с ID {post_id} удалена.")
    else:
        print("Задача не найдена.")

# Удаление пользователя и его постов
def delete_user_and_posts(user_id):
    user = session.query(User).filter(User.id == user_id).first()
    if user:
        session.query(Post).filter(Post.user_id == user_id).delete()
        session.delete(user)
        session.commit()
        print(f"Пользователь с ID {user_id} и его задачи удалены.")
    else:
        print("Пользователь не найден.")

# Основная программа
if __name__ == "__main__":

    add_users()
    add_posts()

    print("\nДобро пожаловать на завод")

    print("\nВсе пользователи:")
    get_all_users()

    print("\nВсе задачи:")
    get_all_posts()

    print("\nЗадачи пользователя с ID 1:")
    get_posts_by_user(1)

    print("\nОбновление email пользователя:")
    update_user_email(1, "NovoeMilo@zavod.com")

    print("\nОбновление контента задачи:")
    update_post_content(1, "За тебя все порезали")

    print("\nУдаление задачи:")
    delete_post(2)

    print("\nУдаление пользователя и его задач:")
    delete_user_and_posts(4)
