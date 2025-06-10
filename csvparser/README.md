Python Scripting Prompt: Network Device Inventory & Maintenance Check (Google Gemini response from the prompt: "Give me a Python scripting prompt. Perhaps something related to parsing csv files?")

Scenario:

You are an infrastructure engineer at a trading firm. Your team maintains a large number of network devices (routers, switches, firewalls) that are critical for ultra-low latency trading. You have been given a network_devices.csv file that lists these devices with some key attributes.

You also know that for compliance and performance, certain devices might require a firmware upgrade or a configuration audit based on their age and type.

Your Task:

Write a Python script that:

    Reads the network_devices.csv file.
        File Format:
        device_id,hostname,ip_address,device_type,location,firmware_version,install_date,last_audit_date
        RTR001,core-router-01,10.0.0.1,Router,Datacenter A,1.5.0,2022-01-15,2024-11-01
        SWT005,edge-switch-05,10.0.1.5,Switch,Trading Floor,2.1.3,2023-03-20,2025-01-20
        FWL002,firewall-02,10.0.2.2,Firewall,DMZ,3.0.1,2021-08-10,2024-06-10
        RTR002,core-router-02,10.0.0.2,Router,Datacenter B,1.4.5,2021-02-28,2024-05-15
        SWT010,trading-switch-10,10.0.1.10,Switch,Trading Floor,2.2.0,2024-05-01,2025-06-01
        FWL003,firewall-03,10.0.2.3,Firewall,Datacenter A,3.0.0,2022-11-05,2025-02-15
        RTR003,market-data-router,10.0.0.3,Router,Trading Floor,1.5.1,2023-07-12,2025-04-01

    Identifies Devices Needing Attention:
        Firmware Upgrade Needed: Any device where device_type is 'Router' or 'Firewall' and firmware_version is older than '1.5.1' for Routers or '3.0.1' for Firewalls. (Assume simple string comparison for version for this exercise, but acknowledge in comments that real-world version comparison is more complex).
        Configuration Audit Needed: Any device where install_date is older than 2 years from today's date (June 10, 2025) AND last_audit_date is older than 1 year from today's date.
            You'll need to parse the dates (e.g., using datetime module).

    Generates an Actionable Report:
        Create a summary report that lists:
            All devices identified for a Firmware Upgrade, including their hostname, ip_address, device_type, and firmware_version.
            All devices identified for a Configuration Audit, including their hostname, ip_address, install_date, and last_audit_date.
            Bonus: If a device needs both, indicate that clearly.

    Outputs the Report:
        Print the report to the console in a clear, readable format.
        Bonus: Save the report to a new text file named device_maintenance_report.txt.

Key Python Skills to Practice:

    csv module for reading CSV files.
    Working with dictionaries (to represent each device row).
    Conditional logic (if/elif/else).
    Looping (for loops).
    Date and time manipulation using the datetime module.
    Basic string operations.
    File I/O (reading and writing text files).

Setup:

    Create a file named network_devices.csv and paste the CSV content provided above into it.
    Start writing your Python script in the same directory.

Good luck! This prompt will test your fundamental Python skills in a practical, infrastructure-relevant context.
