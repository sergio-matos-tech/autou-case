# AutoU - Intelligent Email Classifier 🚀

<!-- Optional: Add a GIF or a screenshot of your application in action here. -->

## 📝 Overview

This project is a web application developed as a solution for the **AutoU Practical Case**. Its goal is to streamline email management by leveraging artificial intelligence to automatically classify incoming messages and suggest appropriate responses. This frees up valuable team time for more critical tasks.

The application analyzes email content—whether pasted directly into the UI or uploaded as a `.txt` or `.pdf` file—and uses the **OpenAI API** to determine if it is **Productive** (requiring a specific action) or **Unproductive** (requiring no immediate action).<br><br>
➡️ **Requirements:** https://autou-digital.notion.site/Case-Pr-tico-AutoU-Desenvolvimento-18836ce78e5580d0b59bcf9610b27769
## ✨ Use Example <br>
<img width="1282" height="796" alt="image" src="https://github.com/user-attachments/assets/687d9b8d-3cb9-4660-b4d2-501840cb12ef" />
<img width="1282" height="796" alt="image" src="https://github.com/user-attachments/assets/107e5422-e6ce-447c-bd00-1591156b10ad" />




➡️ **Access the Live Demo Here:➡️** (https://autou-case-sergiomatos.onrender.com/)

---

## ✨ Key Features

* **AI-Powered Classification:**
  Leverages OpenAI's powerful GPT model to perform nuanced analysis of the email's content, tone, and intent. It accurately categorizes emails as *Productive* (e.g., support requests, status updates, urgent questions) or *Unproductive* (e.g., newsletters, thank-you notes, general announcements).

* **Automated Response Suggestions:**
  For *Productive* emails, the AI generates a professional, context-aware response that acknowledges the user's request and outlines the next steps. For *Unproductive* emails, it provides a brief and courteous acknowledgment, efficiently closing the communication loop without unnecessary back-and-forth.

* **Multiple Input Methods:**
  Offers flexibility by allowing users to either paste raw email text directly into a textarea for instant analysis or upload email files in common formats like `.txt` and `.pdf`. The backend handles text extraction from PDFs seamlessly.

* **Dynamic Example Generation:**
  A unique feature that allows users to instantly generate realistic sample emails (both productive and unproductive) via the UI. This makes it easy to test the application's functionality without needing to provide your own email data.

* **Clean & Responsive UI:**
  The interface is designed to be intuitive and user-friendly, ensuring a smooth experience. It is fully responsive and works flawlessly across desktops, tablets, and mobile devices.

---

## 🛠️ Tech Stack

### Backend

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge\&logo=python\&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge\&logo=flask\&logoColor=white)
![Gunicorn](https://img.shields.io/badge/Gunicorn-499848?style=for-the-badge\&logo=gunicorn\&logoColor=white)

### Frontend

![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge\&logo=html5\&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge\&logo=css3\&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge\&logo=javascript\&logoColor=black)

### AI & NLP

![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=for-the-badge\&logo=openai\&logoColor=white)

### Deployment

![Render](https://img.shields.io/badge/Render-46E3B7?style=for-the-badge\&logo=render\&logoColor=white)

---

## ⚙️ Getting Started Locally

Follow these steps to set up and run the project in your local environment.

### Prerequisites

* Python (3.11 or higher recommended)
* Git
* An OpenAI API Key

### Installation Steps

1. **Clone the repository:**

   ```bash
   git clone https://github.com/your-username/autou-case.git
   cd autou-case
   ```

2. **Create and activate a virtual environment:**

   ```bash
   # Create the environment
   python -m venv venv

   # Activate on Linux/macOS
   source venv/bin/activate

   # Activate on Windows
   .\venv\Scripts\activate
   ```

3. **Install project dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**

   * Create a file named `.env` in the project's root directory.
   * Add your OpenAI API key to this file:

     ```env
     OPENAI_API_KEY='sk-YourSecretKeyGoesHere'
     ```

5. **Run the application:**

   ```bash
   python -m app.app
   ```

   The `-m` flag ensures Python treats the app directory as a package, preventing import errors.

---
