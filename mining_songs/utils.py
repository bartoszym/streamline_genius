def progress_bar(current: int, max: int):
    length = 30
    progress_percent = (current / max) * 100
    done = int(current * length // max)
    bar = "X" * done + "-" * (length - done)
    print("Progress: |" + bar + f"| {progress_percent:.2f}% Complete")
