"""Capture BloggerEasy Qt GUI screenshots into docs/screenshots/."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
OUT = ROOT / "docs" / "screenshots"
OUT.mkdir(parents=True, exist_ok=True)
SAMPLE_HTML = ROOT / "data" / "samples" / "html" / "portfolio.html"
SAMPLE_IMG = None
for cand in (ROOT / "docs" / "screenshots").glob("demo-*.png"):
    SAMPLE_IMG = cand
    break


def main() -> None:
    from PySide6.QtCore import QTimer
    from PySide6.QtWidgets import QApplication

    from bloggereasy.gui.main_window import MainWindow

    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    app.processEvents()

    shots: list[tuple[str, str, bool]] = [
        ("gui-convert-url.png", "convert", False),
        ("gui-convert-image.png", "convert", True),
        ("gui-result.png", "result", False),
        ("gui-import.png", "import", False),
        ("gui-demo.png", "demo", True),
    ]

    def grab(i: int = 0) -> None:
        if i >= len(shots):
            app.quit()
            return
        name, page, act = shots[i]
        win._goto(page)
        app.processEvents()
        if page == "convert" and not act:
            win.radio_url.setChecked(True)
            win.url_edit.setText("https://example.com/")
            win.template.setCurrentText("portfolio")
            app.processEvents()
        if page == "convert" and act:
            win.radio_image.setChecked(True)
            if SAMPLE_IMG and SAMPLE_IMG.exists():
                win._set_image(SAMPLE_IMG)
            win.title_edit.setText("Studio Blog")
            app.processEvents()
        if page == "demo" and act:
            win.run_demo_batch()
            app.processEvents()
        if page == "result" and not win._last_output and SAMPLE_HTML.exists():
            # seed a quick local HTML gen for result page
            from bloggereasy.config import OUT_DIR
            from bloggereasy.integrations.sdk import generate_from_html

            out = OUT_DIR / "gui_shot_portfolio.xml"
            r = generate_from_html(SAMPLE_HTML, out, template="portfolio")
            win._gen_ok(r)
            win._goto("result")
            app.processEvents()
        path = OUT / name
        win.grab().save(str(path), "PNG")
        print("wrote", path, path.stat().st_size)
        QTimer.singleShot(250, lambda: grab(i + 1))

    QTimer.singleShot(400, grab)
    app.exec()


if __name__ == "__main__":
    main()
