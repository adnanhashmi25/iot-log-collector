Project Title: Automated Log Collection from IoT Devices
Project Overview:
Previously, collecting logs from IoT devices was a slow, manual process. Engineers had to:
•	Log in to a central server via SSH.
•	Manually SSH into each IoT device using its Operation & Maintenance (O&M) IP.
•	Execute commands one by one using tools like Putty, Xshell, or TeraTerm.
•	TeraTerm allowed batch execution but opened multiple GUI windows, making it impractical for handling large-scale log collection.
To solve this, I developed a fully automated solution that allows log collection from 1,000+ IoT devices simultaneously using Python (Paramiko & Pexpect) deployed on a central server. Additionally, the solution was enhanced to allow targeted log collection from specific IoT components (such as GPS or DSP), increasing flexibility and scalability.
Furthermore, I introduced a scheduled log collection feature that allows engineers to automate recurring log retrieval at predefined times without manual intervention. By integrating the tool with crontab, engineers can now schedule logs (e.g., temperature logs at 5 AM daily) and retrieve them automatically using a separate retrieval tool.
Role and Responsibilities:
•	Designed & implemented the automation for SSH-based log retrieval.
•	Developed a remote execution workflow to process a list of IoT device IPs.
•	Integrated file management to handle log storage and automated cleanup.
•	Optimized batch processing, making large-scale log retrieval feasible.
•	Enhanced the system to support component-specific log retrieval, improving efficiency and adaptability.
•	Implemented scheduled log collection using crontab, eliminating the need for manual execution.

Technologies Used:
•	Programming Language: Python
•	Libraries & Tools: Paramiko, Pexpect, Linux Bash scripting, Crontab
•	System Components: Central VM, Remote Server, IoT Devices

Challenges and Solutions:
1️ Manual SSH Logins Slowed Down Operations
•	Before: Engineers had to log in to each IoT device manually, causing delays.
•	Solution: The script reads a list of IPs and logs in automatically, executing commands in parallel.
2️ Handling Large-Scale Log Collection Efficiently
•	Before: TeraTerm GUI-based batch automation wasn’t scalable (opened too many windows).
•	Solution: Python automation executed commands remotely on a server, enabling headless execution with no GUI limitations.
3️ Automating File Transfer & Cleanup
•	Before: Engineers had to manually retrieve logs, delete temp files, and manage storage.
•	Solution: The script:
o	Uploads a zip file with device IPs & commands.
o	Executes the script remotely on the server.
o	Downloads collected logs to the engineer’s machine.
o	Deletes temporary files to maintain a clean environment.
4️ Expanding Scalability with Component-Level Targeting
•	Before: The tool only collected general system logs.
•	Solution: Enhanced functionality to allow targeted log collection from specific IoT components (such as GPS or DSP), improving data retrieval efficiency and adaptability.
5️ Introducing Scheduled Log Collection for Full Automation
•	Before: Engineers had to manually launch the tool each time they needed logs.
•	Solution: Integrated crontab-based scheduling, allowing automated retrieval at predefined times (e.g., collect temperature logs at 5 AM daily).
•	Additional Tool for Retrieval: Implemented a companion tool that fetches the scheduled logs, ensuring seamless automation.


Outcomes and Impact:
•	Scalability: Engineers can now collect logs from 1,000+ sites at once instead of one-by-one manual SSH sessions. 
•	Efficiency Gains: Reduced log collection time from hours to minutes, enabling faster troubleshooting. 
•	Zero Manual Effort: Engineers no longer need to manually navigate SSH sessions—everything runs with a single command. 
•	Optimized Resource Utilization: The solution runs directly on the server, avoiding unnecessary GUI-based tools. 
•	Fully Automated Workflow: Scheduled log collection ensures logs are always available when needed, without requiring manual execution. 
•	Future-Proof Design: The system can be easily extended for additional IoT components as required.
