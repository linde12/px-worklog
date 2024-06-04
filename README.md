## PX Worklog

Tool to automatically report 8 hours of work to PX.

The idea is that you only look at PX once per month to report deviations and attest the reports. The
rest of the days you can focus on your _actual_ work.

## Usage

1. Install the requirements:

```bash
pip install -r requirements.txt
```

2. Export your PX password as an environment variable:

```bash
export PX_PASSWORD=your_password
```

3. Run the script:

```bash
python cli.py -u USERNAME -w 202430 --project 1234 --activity 3
```
