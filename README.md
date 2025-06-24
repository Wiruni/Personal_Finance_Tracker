# Personal_Finance_Tracker
A Python-based personal finance management application that helps users track their income and expenses efficiently. The project supports both Command-Line Interface (CLI) and Graphical User Interface (GUI using Tkinter) modes, offering flexibility for different user preferences.


## 🚀 Why Personal_Finance_Tracker?
This project simplifies transaction management and data persistence for personal finance applications. The core features include:
- 🧾 **Transaction Data Structure**: Provides a foundational format for storing and managing financial transactions efficiently.
- 🛠️ **Core Transaction Management**: Supports loading, adding, and bulk importing transactions to facilitate comprehensive financial tracking.
- 🖥️ **Dual Interface Options**: Offers both CLI and GUI interfaces, catering to diverse user preferences and accessibility needs.
- 📊 **Financial Reporting & Analysis**: Integrates seamlessly into larger systems for detailed financial insights and reporting.
- 🧩 **Extensible Architecture**: Designed for easy integration and customization, enabling developers to adapt it to various personal finance workflows.


## 🧰 Getting Started
### ✅ Prerequisites
This project requires the following dependencies:

- **Programming Language**: Python  
- **Package Manager**: Conda


## 📂 Project Structure

personal_finance_tracker/
│── main.py # Main launcher for CLI/GUI mode
│── cli.py # CLI menu functions
│── gui.py # GUI window and event handlers
│── core.py # Core transaction logic and shared methods
│── utils.py # Utility functions (save/load/search/sort)
│── transactions.json # Stores transaction data persistently
│── README.md # Project documentation



## 💾 Data Persistence

All transaction data is stored in `transactions.json`.  
> ⚠️ Make sure to include this file in your repo to avoid losing data between runs.



## 👨‍💻 How to Run

Launch the app from the terminal:

```bash
python main.py

Then choose:
1 to use the CLI Mode
2 to use the GUI Mode
