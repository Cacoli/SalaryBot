# SalaryBot 

A UiPath automation bot that processes salary-related tasks, reducing manual effort and human error in payroll workflows.

## What It Does

SalaryBot automates salary processing tasks using UiPath. It reads input data (e.g. from Excel), performs calculations, and generates output — all without manual intervention once triggered.

## Requirements

- [UiPath Studio](https://www.uipath.com/product/studio) installed on your machine
- Microsoft Excel (if the bot reads/writes Excel files)
- Windows OS

## How to Run

Since this bot is not hosted on any server, it must be run manually via UiPath Studio:

1. Clone or download this repository
   ```
   git clone https://github.com/Cacoli/SalaryBot.git
   ```
2. Open UiPath Studio
3. Click **Open Project** and navigate to the folder where you cloned the repo
4. Open `Main.xaml`
5. Update any input file paths or config values if needed
6. Click **Run** to execute the bot

## Project Structure

```
SalaryBot/
├── Main.xaml          # Entry point of the automation
├── project.json       # UiPath project configuration
└── ...                # Other workflow files
```

## Notes

- This project is currently run locally and has not been deployed to UiPath Orchestrator
- Make sure all input files are in place before running the bot

## Future Plans

- [ ] Deploy to UiPath Orchestrator for scheduled/remote runs
- [ ] Add error handling and logging
- [ ] Support multiple input formats
