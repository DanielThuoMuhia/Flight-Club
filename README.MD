# Flight Deal Finder

## 📖 Overview
The **Flight Deal Finder** is a Python application designed to monitor flight prices from a specified origin to various destinations. It sends notifications via WhatsApp whenever there are low-priced flights or when flight data is unavailable. This project integrates with Google Sheets to manage destination data effectively.

## 🚀 Features
- **Automatic IATA Code Retrieval:** Automatically updates IATA codes for destinations missing this information.
- **Flight Search:** Checks for flights within a specified date range and identifies the cheapest options.
- **Notifications:** Sends alerts via WhatsApp for:
  - **Low Price Alerts:** When a flight is found below the expected price.
  - **Data Availability Alerts:** Notifications when no flight data is available or when no valid flights are found.

## 🛠️ Technologies Used
- **Python 3.x**
- **Google Sheets API:** For managing destination data.
- **Flight Search API:** To fetch flight information.
- **WhatsApp API:** For sending notifications.
- **Datetime:** For handling date and time functionalities.

## 📥 Getting Started

### Prerequisites
Before running the application, ensure you have:
- **Python 3.x** installed on your machine.
- Required libraries. Install them using:
  ```bash
  pip install requests
