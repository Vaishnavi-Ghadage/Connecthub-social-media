 🌐 ConnectHub – Social Media Website

**ConnectHub** is a web-based social media platform developed using Django and Python. It allows users to connect with others, share posts, interact through likes and comments, and manage their personal profiles.

The project aims to provide a simple and interactive social networking experience where users can communicate and share content with their community.

 ✨ Features

- **User Authentication:** Secure user registration, login, and logout.
- **User Profiles:** Create and manage personal profiles.
- **Create Posts:** Share text and image-based posts.
- **Like & Unlike Posts:** Interact with posts shared by other users.
- **Comments:** Comment on posts and engage in discussions.
- **Follow System:** Follow and unfollow other users.
- **News Feed:** View posts shared by users.
- **Profile Management:** Update profile information and profile pictures.

 🛠️ Tech Stack

| Technology | Purpose                |
| Python     | Backend programming    |
| Django     | Web framework          |
| HTML5      | Structure              |
| CSS3       | Styling                |
| JavaScript | Frontend interactivity |
| SQLite     | Database               |

 📂 Project Structure

ConnectHub/
│
├── manage.py
├── db.sqlite3
│
├── social/
│   ├── migrations/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── templates/
│
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│
└── templates/


*Note: The directory structure may vary depending on the final project implementation.*

 ⚙️ Installation & Setup

Follow these steps to run ConnectHub locally.

**1. Clone the repository**

```bash
git clone https://github.com/Vaishnavi-Ghadage/Connecthub-social-media.git
```

**2. Navigate to the project directory**

```bash
cd Connecthub-social-media
```

**3. Create a virtual environment**

```bash
python -m venv venv
```

**4. Activate the virtual environment**

For Windows:

```bash
venv\Scripts\activate
```

**5. Install dependencies**

```bash
pip install django
```

**6. Apply database migrations**

```bash
python manage.py makemigrations
python manage.py migrate
```

**7. Run the development server**

```bash
python manage.py runserver
```

**8. Open in your browser**

```text
http://127.0.0.1:8000/
```

 🎯 Project Objective

The main objective of ConnectHub is to develop a dynamic social networking application that demonstrates full-stack web development concepts, including user authentication, database management, CRUD operations, and interactive user engagement.

 🚀 Future Enhancements

- Real-time messaging and chat functionality.
- Real-time notifications.
- Advanced search and filtering.
- Improved responsive UI.
- Post sharing and bookmarking.

 👩‍💻 Developer

**Vaishnavi Ghadage**

GitHub: [Vaishnavi-Ghadage](https://github.com/Vaishnavi-Ghadage)

---

⭐ If you like this project, consider giving it a star!

**Developed as part of the CodeAlpha Virtual Full Stack Java Internship.**
