# Toggl Stats
A program to generate some statistics on Toggle (time tracker) entries.

## Usage
1. Log into toggle.com
2. Go to "Reports" > "Detailed" and select time range
3. Under "Export" click "Download as CSV"
4. Copy .CSV file to `data` directory in `ToggleStats` repo
5. run `python main.py` with additional arguments to generate statistics


### Arguments
| Argument | Description |
| --- | --- |
| `--heatmap` | shows heatmap of focused time per week and hour |
| `--weekday` | shows focused time based on weekday |
