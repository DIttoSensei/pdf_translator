import subprocess
import os
import time
import sys

STEP_DELAY = 7  # 7-second buffer

def run_script(script_name):
    """Runs a python script and waits for it to finish."""
    print(f"\n🚀 [MAIN] Starting: {script_name}")
    try:
        subprocess.run([sys.executable, script_name], check=True)
        print(f"💤 Waiting {STEP_DELAY}s for system to settle...")
        time.sleep(STEP_DELAY) 
    except subprocess.CalledProcessError as e:
        print(f"❌ [MAIN] Error running {script_name}: {e}")
        sys.exit(1)


def main():
    print("--- PROCESS STARTED ---")

    # EXTRACT PDF CONTENTS FIRST
    run_script("pdf_extract.py")

    # SUMMARIZE THE EXTRACTED TEXT
    run_script('summarization_model.py')

    # TRANSLATE THE SUMMARIZED TEXT
    run_script('translating_model.py')

    # WRITE THE TRANSLATED TEXT TO A PDF
    run_script('write_to_pdf.py')


if __name__ == "__main__":
    main()