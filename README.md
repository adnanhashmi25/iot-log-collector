# Automated Log Collection from IoT Devices  

🚀 **Overview:**  
This tool automates log collection from IoT devices, replacing manual SSH-based retrieval with a scalable, efficient Python-based solution. It enables engineers to collect logs from **1,000+ devices simultaneously**, improving troubleshooting speed and efficiency.  

🔒 **Note:**  
- Due to NDA restrictions, **actual input files are not provided**.  
- Users must supply **their own configuration files**.  

---

## 📌 Installation & Setup  

### 1️⃣ Prerequisites  
Ensure you have the following installed:  
- **Python 3.x**  
- **Linux or Windows with SSH access**  

### 2️⃣ Clone the Repository  
git clone https://github.com/adnanhashmi25/iot-log-collector.git
cd iot-log-collector

### 3️⃣ Install Dependencies
paramiko library needed.

### 4️⃣ Provide Input Files
Place your device IP list and authentication details inside the /config folder.
Specify log retrieval commands in the script or configuration file.

### 5️⃣ Run the Log Collection Script
python log_collector.py

### 6️⃣ Output
Logs are retrieved and saved automatically in the /logs folder.
The system cleans up temporary files after execution.

📌 Features
✔ Automated SSH login to multiple IoT devices
✔ Parallel log retrieval from 1,000+ sites at once
✔ Customizable log commands for different device types
✔ Scheduled data collection using cron jobs

📜 Detailed Documentation
For a full project breakdown, visit the docs folder.
