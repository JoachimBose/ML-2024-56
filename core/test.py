import subprocess
import logging
from config import potential_passes

def test_compile(selected_pass: str) -> None:
    cmd =  ["python3", "./compile.py", "bicg", selected_pass]
    print(f"python3 compile.py bicg {selected_pass}")
    error = subprocess.run(
        cmd,
        check=True,
        capture_output=True,
        text=True
    )
    test = error
    logging.debug(f"{test}")

# print("[")
# for p in sorted(potential_passes):
#     print(f"    \"{p}\",")
# print("]")

# for i, _ in enumerate(potential_passes):
#     selected = "0" * len(potential_passes)
#     selected = selected[:i] + "1" + selected[i + 1:]
#     test_compile(selected)
# test_compile("1" * len(potential_passes))
print(len(potential_passes))    
