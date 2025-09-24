# 🐍 Python Web Browser by Keshav Singh

A feature-rich, modern web browser built from scratch using Python, PyQt5, and QtWebEngine. This project demonstrates how to create a good-looking, functional desktop application with a custom dark theme, tabs, and modern user experience features.


---

## ✨ Features

* **Modern Dark Theme**: A sleek, custom-styled dark interface using QSS (Qt Style Sheets).
* **Tabbed Browsing**: Open multiple web pages in different tabs, just like a modern browser.
* **Professional Icons**: Uses the `qtawesome` library for high-quality Font Awesome icons.
* **Smart URL/Search Bar**: Type a URL to navigate or enter any text to perform a Google search.
* **Right-Click Menu**: A context menu with essential actions like Back, Forward, Reload, and **Inspect Element**.
* **Zoom Controls**: Easily zoom pages in and out.
* **Loading Progress Bar**: A subtle progress bar indicates when a page is loading.
* **Download Support**: Basic handling for file downloads (downloads are accepted and progress is logged to the terminal).

---

## 🛠️ Tech Stack

* **Language**: Python 3
* **GUI Framework**: PyQt5
* **Browser Engine**: PyQtWebEngine (based on Google's Chromium project)
* **Icons**: qtawesome

---

## 🚀 Getting Started

Follow these instructions to get a copy of the project up and running on your local machine.

### Prerequisites

Make sure you have **Python 3** installed on your system. You can download it from [python.org](https://www.python.org/downloads/).

### Installation

1.  **Clone the repository (or download the code)**
    If you have Git installed, you can clone the repository. Otherwise, just download the `web_borwser.py` file.
    ```sh
    git clone https://github.com/coderkeshav-yt/web-browser.git
    cd your-repository-directory
    ```

2.  **Create a Virtual Environment (Recommended)**
    It's good practice to create a virtual environment to keep dependencies isolated.
    ```sh
    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate

    # For Windows
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Install Required Libraries**
    Install all the necessary packages using pip.
    ```sh
    pip install PyQt5
    pip install PyQtWebEngine
    pip install qtawesome
    ```

---

## ▶️ How to Run

Once the setup is complete, you can run the browser with the following command:

```sh
python web_borwser.py
```
This will launch the browser application window.

---

## 👤 Author

* **Keshav Singh**

---

## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for details.
