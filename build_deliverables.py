import os
import sys
import base64
import subprocess
import time

def encode_image(path):
    if not os.path.exists(path):
        print(f"Warning: Image not found at {path}")
        return ""
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

def main():
    print("=" * 60)
    print("VOICE ARENA: DELIVERABLES COMPILATION PIPELINE")
    print("=" * 60)

    build_dir = os.path.join(os.getcwd(), "build")
    os.makedirs(build_dir, exist_ok=True)

    # 1. Base64 encode all generated charts
    chart_breakdown = encode_image("experiments/der_breakdown.png")
    chart_collar = encode_image("experiments/collar_sensitivity.png")
    chart_radar = encode_image("experiments/radar_benchmark.png")

    print(f"Encoded charts successfully (Breakdown: {len(chart_breakdown)} chars, Collar: {len(chart_collar)} chars, Radar: {len(chart_radar)} chars)")

    # 2. Process Main Document HTML
    with open("src/templates/main_doc.html", "r", encoding="utf-8") as f:
        main_html = f.read()

    main_html = main_html.replace("{{CHART_BREAKDOWN}}", chart_breakdown)
    main_html = main_html.replace("{{CHART_COLLAR}}", chart_collar)
    main_html = main_html.replace("{{CHART_RADAR}}", chart_radar)

    main_html_path = os.path.join(build_dir, "Ansh_Agnihotri_Q1_Main.html")
    with open(main_html_path, "w", encoding="utf-8") as f:
        f.write(main_html)
    print(f"Resolved Main Document HTML -> {main_html_path}")

    # 3. Process One-Pager HTML
    with open("src/templates/one_pager.html", "r", encoding="utf-8") as f:
        one_pager_html = f.read()

    one_pager_html_path = os.path.join(build_dir, "Ansh_Agnihotri_Q1_OnePager.html")
    with open(one_pager_html_path, "w", encoding="utf-8") as f:
        f.write(one_pager_html)
    print(f"Resolved One-Pager HTML -> {one_pager_html_path}")

    # 4. Process Leaderboard Sketch HTML
    with open("src/templates/leaderboard_sketch.html", "r", encoding="utf-8") as f:
        sketch_html = f.read()

    sketch_html_path = os.path.join(build_dir, "Ansh_Agnihotri_Leaderboard_Sketch.html")
    with open(sketch_html_path, "w", encoding="utf-8") as f:
        f.write(sketch_html)
    # Also save a copy as root interactive file
    with open("leaderboard_sketch_interactive.html", "w", encoding="utf-8") as f:
        f.write(sketch_html)
    print(f"Resolved Leaderboard Sketch HTML -> {sketch_html_path}")

    # 5. Compile to PDF using Chrome Headless
    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    if not os.path.exists(chrome_path):
        chrome_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

    print(f"Using browser binary: {chrome_path}")

    tasks = [
        ("Ansh_Agnihotri_Q1_Main.pdf", main_html_path, False),
        ("Ansh_Agnihotri_Q1_OnePager.pdf", one_pager_html_path, False),
        ("Ansh_Agnihotri_Leaderboard_Sketch.pdf", sketch_html_path, True),
        ("Leaderboard_Sketch.pdf", sketch_html_path, True)
    ]

    for pdf_name, html_input, is_landscape in tasks:
        target_pdf = os.path.join(os.getcwd(), pdf_name)
        file_url = f"file:///{os.path.abspath(html_input).replace(os.sep, '/')}"
        
        cmd = [
            chrome_path,
            "--headless=new",
            "--no-sandbox",
            "--disable-gpu",
            "--run-all-compositor-stages-before-draw",
            f"--print-to-pdf={target_pdf}",
            file_url
        ]

        print(f"\nCompiling {pdf_name}...")
        res = subprocess.run(cmd, capture_output=True, text=True)
        time.sleep(1)

        if os.path.exists(target_pdf):
            size_kb = os.path.getsize(target_pdf) / 1024.0
            print(f"-> SUCCESS: {pdf_name} generated ({size_kb:.1f} KB)")
        else:
            print(f"-> ERROR: Failed to generate {pdf_name}")
            print(f"Stderr: {res.stderr}")

    print("\n" + "=" * 60)
    print("COMPILATION COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    main()

