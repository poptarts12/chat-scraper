# Chat Scraper

Chat Scraper is a browser extension and accompanying backend service designed to capture and persist in real-time all user interactions with ChatGPT. Conversations and messages are forwarded to a backend API where they are stored in a database, enabling later analysis and insights.

---

## 🔍 Features

* **Real‑time Capture**: Automatically detect new ChatGPT sessions and messages via a content script.
* **Persistent Storage**: Store conversations and messages in a relational database (PostgreSQL in production, SQLite for development).
* **User Management**: Register and authenticate users (JWT‑based) to secure data access.
* **Chrome Extension (Manifest V3)**:

  * **Content Script**: Observes the ChatGPT UI, detecting new chats and messages.
  * **Background Service Worker**: Maintains `currentConversationId`, handles message routing to the backend.
  * **Popup UI**: Simple login/register form for user authentication.
* **RESTful API**: FastAPI endpoints for managing users, conversations, and messages.
* **Security**: Password hashing with bcrypt and JWT tokens for API authentication.
* **Modular Codebase**: Clear separation between backend (`/backend/app`) and extension (`/extension`).

---

## 📦 Tech Stack

| Layer               | Technology                                            |
| ------------------- | ----------------------------------------------------- |
| **Backend**         | Python 3.8+, FastAPI, SQLAlchemy, PostgreSQL / SQLite |
| **Auth & Security** | PyJWT, bcrypt                                         |
| **Database**        | SQLAlchemy ORM, PostgreSQL (prod), SQLite (dev)       |
| **Extension**       | Chrome Extension Manifest V3, JavaScript / ES6        |
| **Build & Dev**     | Uvicorn, Docker (optional), pytest                    |

---

## 🚀 Getting Started

### Prerequisites

* Python 3.8 or higher
* Node.js (for any future front‑end build steps)
* (Optional) Docker & Docker Compose

### Setup Backend

```bash
# Clone the repo
git clone https://github.com/poptarts12/chat-scraper.git
cd chat-scraper/backend/app

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
# Create a .env file or export:
# DATABASE_URL, SECRET_KEY, DEBUG (True/False)

# Run the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

API will be available at `http://localhost:8000` with automatic docs at `http://localhost:8000/docs`.

### Load the Chrome Extension

1. Navigate to `chrome://extensions/` in your browser.
2. Enable **Developer mode** (top right).
3. Click **Load unpacked** and select the `/extension` folder from this project.
4. Pin the Chat Scraper extension to your toolbar.

---

## 🎯 Usage

1. **Login/Register**: Click the extension icon and complete the popup form to authenticate.
2. **Start Chat**: Open or refresh `https://chat.openai.com` and begin a new session.
3. **Data Flow**:

   * The **content script** detects new chats and messages.
   * Messages are sent to the **background service worker** which maintains the active conversation ID.
   * The **background** calls the backend API to create conversations and store messages.
4. **Inspect Data**: Open your database or use API endpoints (`/conversations`, `/messages`) to review stored data.

---

## 🔄 Roadmap & Improvements

* **Duplicate Detection**: Refine the logic for filtering duplicate messages on the backend.
* **Robust Selectors**: Harden content script selectors against ChatGPT UI changes.
* **UI Enhancements**: Add conversation history listing in the popup for easy navigation.
* **Testing**: Expand unit and integration tests for both backend and extension.
* **Error Handling**: Improve user‑friendly error messages and retry mechanisms.

---

## 🤝 Contributing

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/YourFeature`.
3. Commit your changes: `git commit -m "Add feature X"`.
4. Push to the branch: `git push origin feature/YourFeature`.
5. Open a Pull Request detailing your changes.

Please follow the existing code style and include tests for new features.

---
