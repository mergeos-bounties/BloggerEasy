"""BloggerEasy Qt desktop — URL or image → Blogger XML theme."""

from __future__ import annotations

import json
from pathlib import Path

from PySide6.QtCore import Qt, QSize, QThread, Signal, QUrl
from PySide6.QtGui import QDesktopServices, QPixmap
from PySide6.QtWidgets import (
    QButtonGroup,
    QComboBox,
    QFileDialog,
    QFormLayout,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QRadioButton,
    QStackedWidget,
    QStatusBar,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from bloggereasy import __version__
from bloggereasy.config import OUT_DIR, SAMPLES_DIR
from bloggereasy.gui.styles import STYLESHEET
from bloggereasy.integrations.sdk import (
    generate_from_html,
    generate_from_image,
    generate_from_url,
)
from bloggereasy.theme.presets import PRESETS
from bloggereasy.theme.validate import validate_theme_file


def _card() -> QFrame:
    f = QFrame()
    f.setObjectName("card")
    return f


def _primary(text: str) -> QPushButton:
    b = QPushButton(text)
    b.setCursor(Qt.CursorShape.PointingHandCursor)
    b.setStyleSheet(
        "QPushButton { background: qlineargradient(x1:0,y1:0,x2:1,y2:0,"
        " stop:0 #0ea5e9, stop:1 #0284c7); color: white; border: none;"
        " border-radius: 10px; padding: 12px 20px; font-weight: 700; font-size: 14px; }"
        "QPushButton:hover { background: #38bdf8; color: #0c4a6e; }"
        "QPushButton:disabled { background: #334155; color: #94a3b8; }"
    )
    return b


def _secondary(text: str) -> QPushButton:
    b = QPushButton(text)
    b.setCursor(Qt.CursorShape.PointingHandCursor)
    b.setStyleSheet(
        "QPushButton { background: #1e293b; color: #e2e8f0; border: 1px solid #334155;"
        " border-radius: 10px; padding: 10px 16px; font-weight: 600; }"
        "QPushButton:hover { background: #334155; border-color: #38bdf8; }"
    )
    return b


def _ghost(text: str) -> QPushButton:
    b = QPushButton(text)
    b.setCursor(Qt.CursorShape.PointingHandCursor)
    b.setCheckable(True)
    b.setStyleSheet(
        "QPushButton { text-align: left; background: transparent; border: none;"
        " border-radius: 10px; padding: 12px 14px; color: #94a3b8; font-weight: 600; }"
        "QPushButton:hover { background: #1e293b; color: #e2e8f0; }"
        "QPushButton:checked { background: #0c4a6e; color: #e0f2fe; }"
    )
    return b


class GenerateWorker(QThread):
    finished_ok = Signal(dict)
    failed = Signal(str)

    def __init__(
        self,
        mode: str,
        *,
        url: str = "",
        image_path: Path | None = None,
        html_path: Path | None = None,
        out_path: Path,
        template: str = "simple",
        title: str = "My Blog",
    ) -> None:
        super().__init__()
        self.mode = mode
        self.url = url
        self.image_path = image_path
        self.html_path = html_path
        self.out_path = out_path
        self.template = template
        self.title = title

    def run(self) -> None:
        try:
            if self.mode == "url":
                result = generate_from_url(
                    self.url.strip(),
                    self.out_path,
                    template=self.template,
                    cache_dir=OUT_DIR,
                )
            elif self.mode == "image":
                if not self.image_path or not self.image_path.exists():
                    raise FileNotFoundError("Image file not found")
                result = generate_from_image(
                    self.image_path,
                    self.out_path,
                    title=self.title or "My Blog",
                    template=self.template if self.template != "simple" else "from-image",
                )
            elif self.mode == "html":
                if not self.html_path or not self.html_path.exists():
                    raise FileNotFoundError("HTML file not found")
                result = generate_from_html(
                    self.html_path,
                    self.out_path,
                    template=self.template,
                )
            else:
                raise ValueError(f"Unknown mode {self.mode}")
            self.finished_ok.emit(result)
        except Exception as exc:  # noqa: BLE001
            self.failed.emit(str(exc))


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle(f"BloggerEasy · URL / Image → Blogger Theme · v{__version__}")
        self.resize(1120, 760)
        self.setMinimumSize(QSize(920, 600))
        self.setStyleSheet(STYLESHEET)
        self._worker: GenerateWorker | None = None
        self._image_path: Path | None = None
        self._html_path: Path | None = None
        self._last_output: Path | None = None

        central = QWidget()
        central.setObjectName("central")
        self.setCentralWidget(central)
        root = QHBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        side = QFrame()
        side.setObjectName("sidebar")
        side.setFixedWidth(210)
        sl = QVBoxLayout(side)
        sl.setContentsMargins(14, 18, 14, 14)
        brand = QLabel("✦ BloggerEasy")
        brand.setObjectName("brand")
        sl.addWidget(brand)
        sub = QLabel("Theme from web or image")
        sub.setObjectName("brandSub")
        sl.addWidget(sub)

        self._nav: list[QPushButton] = []
        self._keys = ["convert", "result", "templates", "import", "demo"]
        labels = {
            "convert": "✨  Create theme",
            "result": "📄  Output",
            "templates": "🎨  Templates",
            "import": "⬆️  Import to Blogger",
            "demo": "▶  Sample demo",
        }
        for k in self._keys:
            b = _ghost(labels[k])
            b.clicked.connect(lambda _=False, key=k: self._goto(key))
            self._nav.append(b)
            sl.addWidget(b)
        sl.addStretch(1)
        sl.addWidget(QLabel(f"v{__version__} · offline-ready"))
        root.addWidget(side)

        self.stack = QStackedWidget()
        root.addWidget(self.stack, 1)

        self.pages = {
            "convert": self._page_convert(),
            "result": self._page_result(),
            "templates": self._page_templates(),
            "import": self._page_import(),
            "demo": self._page_demo(),
        }
        for w in self.pages.values():
            self.stack.addWidget(w)

        self.setStatusBar(QStatusBar())
        self._status("Ready · paste a URL or choose an image design")
        self._goto("convert")
        self._set_mode("url")

    def _status(self, msg: str) -> None:
        self.statusBar().showMessage(msg)

    def _goto(self, key: str) -> None:
        idx = self._keys.index(key)
        self.stack.setCurrentIndex(idx)
        for i, b in enumerate(self._nav):
            b.setChecked(i == idx)

    # ----- Convert -----
    def _page_convert(self) -> QWidget:
        page = QWidget()
        lay = QVBoxLayout(page)
        lay.setContentsMargins(28, 24, 28, 24)
        lay.setSpacing(14)

        t = QLabel("Create a Blogger theme")
        t.setObjectName("h1")
        lay.addWidget(t)
        s = QLabel(
            "Input a public website URL or a design image → export XML → "
            "upload in Blogger Theme → Backup/Restore."
        )
        s.setObjectName("h2")
        s.setWordWrap(True)
        lay.addWidget(s)

        # Mode radios
        mode_card = _card()
        ml = QHBoxLayout(mode_card)
        ml.setContentsMargins(18, 14, 18, 14)
        self.mode_group = QButtonGroup(self)
        self.radio_url = QRadioButton("🌐  Website URL")
        self.radio_image = QRadioButton("🖼️  Design image")
        self.radio_html = QRadioButton("📝  Local HTML")
        self.radio_url.setChecked(True)
        for i, r in enumerate((self.radio_url, self.radio_image, self.radio_html)):
            self.mode_group.addButton(r, i)
            ml.addWidget(r)
        ml.addStretch(1)
        self.radio_url.toggled.connect(lambda on: on and self._set_mode("url"))
        self.radio_image.toggled.connect(lambda on: on and self._set_mode("image"))
        self.radio_html.toggled.connect(lambda on: on and self._set_mode("html"))
        lay.addWidget(mode_card)

        # Input card
        self.input_card = _card()
        il = QVBoxLayout(self.input_card)
        il.setContentsMargins(18, 18, 18, 18)
        il.setSpacing(12)

        # URL row
        self.url_row = QWidget()
        ur = QVBoxLayout(self.url_row)
        ur.setContentsMargins(0, 0, 0, 0)
        ur.addWidget(QLabel("Website URL (public HTML page)"))
        self.url_edit = QLineEdit()
        self.url_edit.setPlaceholderText("https://example.com/  or any public blog homepage")
        ur.addWidget(self.url_edit)
        hint = QLabel("Respect site Terms of Service. Only public pages — no login required.")
        hint.setObjectName("hint")
        ur.addWidget(hint)
        il.addWidget(self.url_row)

        # Image row
        self.image_row = QWidget()
        ir = QVBoxLayout(self.image_row)
        ir.setContentsMargins(0, 0, 0, 0)
        self.drop = QFrame()
        self.drop.setObjectName("dropZone")
        self.drop.setMinimumHeight(140)
        dl = QVBoxLayout(self.drop)
        self.image_preview = QLabel("Drop a mockup / screenshot here\nor click Browse image")
        self.image_preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_preview.setObjectName("h2")
        self.image_preview.setWordWrap(True)
        dl.addWidget(self.image_preview)
        ir.addWidget(self.drop)
        img_btns = QHBoxLayout()
        browse_img = _secondary("Browse image…")
        browse_img.clicked.connect(self._browse_image)
        img_btns.addWidget(browse_img)
        img_btns.addStretch(1)
        ir.addLayout(img_btns)
        title_row = QFormLayout()
        self.title_edit = QLineEdit("My Blog")
        title_row.addRow("Blog title", self.title_edit)
        ir.addLayout(title_row)
        ir.addWidget(QLabel("Colors are sampled from the image (Pillow) into the theme skin."))
        il.addWidget(self.image_row)

        # HTML row
        self.html_row = QWidget()
        hr = QVBoxLayout(self.html_row)
        hr.setContentsMargins(0, 0, 0, 0)
        self.html_path_label = QLabel("No HTML file selected")
        self.html_path_label.setObjectName("h2")
        hr.addWidget(self.html_path_label)
        browse_html = _secondary("Browse HTML…")
        browse_html.clicked.connect(self._browse_html)
        hr.addWidget(browse_html, alignment=Qt.AlignmentFlag.AlignLeft)
        samples = _secondary("Use bundled sample…")
        samples.clicked.connect(self._pick_sample)
        hr.addWidget(samples, alignment=Qt.AlignmentFlag.AlignLeft)
        il.addWidget(self.html_row)

        lay.addWidget(self.input_card)

        # Options
        opt = _card()
        of = QFormLayout(opt)
        of.setContentsMargins(18, 14, 18, 14)
        self.template = QComboBox()
        for name in PRESETS:
            self.template.addItem(name)
        self.template.setCurrentText("simple")
        of.addRow("Template style", self.template)
        out_row = QHBoxLayout()
        self.out_edit = QLineEdit(str(OUT_DIR / "theme.xml"))
        out_browse = _secondary("…")
        out_browse.setFixedWidth(44)
        out_browse.clicked.connect(self._browse_out)
        out_row.addWidget(self.out_edit, 1)
        out_row.addWidget(out_browse)
        of.addRow("Output XML", out_row)
        lay.addWidget(opt)

        self.progress = QProgressBar()
        self.progress.setRange(0, 0)
        self.progress.setVisible(False)
        lay.addWidget(self.progress)

        gen = _primary("Generate Blogger XML theme")
        gen.clicked.connect(self.run_generate)
        lay.addWidget(gen, alignment=Qt.AlignmentFlag.AlignLeft)

        self.convert_log = QTextEdit()
        self.convert_log.setReadOnly(True)
        self.convert_log.setMaximumHeight(120)
        self.convert_log.setPlaceholderText("Status messages appear here…")
        lay.addWidget(self.convert_log)
        lay.addStretch(1)
        return page

    def _set_mode(self, mode: str) -> None:
        self._mode = mode
        self.url_row.setVisible(mode == "url")
        self.image_row.setVisible(mode == "image")
        self.html_row.setVisible(mode == "html")
        if mode == "image" and self.template.currentText() == "simple":
            self.template.setCurrentText("from-image")
        if mode == "url" and self.template.currentText() == "from-image":
            self.template.setCurrentText("simple")

    def _browse_image(self) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Choose design image",
            "",
            "Images (*.png *.jpg *.jpeg *.webp *.bmp);;All files (*.*)",
        )
        if path:
            self._set_image(Path(path))

    def _set_image(self, path: Path) -> None:
        self._image_path = path
        pix = QPixmap(str(path))
        if not pix.isNull():
            self.image_preview.setPixmap(
                pix.scaled(
                    420,
                    160,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )
            )
        else:
            self.image_preview.setText(path.name)
        stem = path.stem.replace("_", "-")
        self.out_edit.setText(str(OUT_DIR / f"{stem}-image.xml"))
        self._status(f"Image: {path.name}")

    def _browse_html(self) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self, "Choose HTML file", "", "HTML (*.html *.htm);;All files (*.*)"
        )
        if path:
            self._html_path = Path(path)
            self.html_path_label.setText(str(self._html_path))
            self.out_edit.setText(str(OUT_DIR / f"{self._html_path.stem}.xml"))

    def _pick_sample(self) -> None:
        samples = (
            sorted((SAMPLES_DIR / "html").glob("*.html")) if (SAMPLES_DIR / "html").exists() else []
        )
        if not samples:
            QMessageBox.information(self, "BloggerEasy", "No samples under data/samples/html")
            return
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Bundled samples",
            str(SAMPLES_DIR / "html"),
            "HTML (*.html)",
        )
        if path:
            self._html_path = Path(path)
            self.html_path_label.setText(str(self._html_path))
            self.out_edit.setText(str(OUT_DIR / f"{self._html_path.stem}.xml"))
            mapping = {
                "portfolio.html": "portfolio",
                "news_portal.html": "news",
                "dark_dev.html": "dark",
                "magazine.html": "magazine",
            }
            self.template.setCurrentText(mapping.get(self._html_path.name, "simple"))

    def _browse_out(self) -> None:
        path, _ = QFileDialog.getSaveFileName(
            self, "Save Blogger theme XML", self.out_edit.text(), "XML (*.xml)"
        )
        if path:
            self.out_edit.setText(path)

    def run_generate(self) -> None:
        if self._worker and self._worker.isRunning():
            return
        out = Path(self.out_edit.text().strip() or str(OUT_DIR / "theme.xml"))
        if not out.suffix:
            out = out.with_suffix(".xml")
        out.parent.mkdir(parents=True, exist_ok=True)
        tmpl = self.template.currentText() or "simple"
        mode = self._mode

        if mode == "url":
            url = self.url_edit.text().strip()
            if not url.startswith(("http://", "https://")):
                QMessageBox.warning(self, "BloggerEasy", "Enter a valid http(s) URL.")
                return
            if out.name == "theme.xml":
                out = OUT_DIR / "from_url.xml"
                self.out_edit.setText(str(out))
            self._worker = GenerateWorker(mode, url=url, out_path=out, template=tmpl)
        elif mode == "image":
            if not self._image_path:
                QMessageBox.warning(self, "BloggerEasy", "Choose a design image first.")
                return
            self._worker = GenerateWorker(
                mode,
                image_path=self._image_path,
                out_path=out,
                template=tmpl,
                title=self.title_edit.text().strip() or "My Blog",
            )
        else:
            if not self._html_path:
                QMessageBox.warning(self, "BloggerEasy", "Choose an HTML file first.")
                return
            self._worker = GenerateWorker(
                mode, html_path=self._html_path, out_path=out, template=tmpl
            )

        self.progress.setVisible(True)
        self.convert_log.append(f"Generating ({mode}) → {out} …")
        self._worker.finished_ok.connect(self._gen_ok)
        self._worker.failed.connect(self._gen_fail)
        self._worker.start()

    def _gen_ok(self, result: dict) -> None:
        self.progress.setVisible(False)
        path = Path(str(result.get("output") or ""))
        self._last_output = path
        self.convert_log.append(f"✓ Wrote {path} ({result.get('bytes')} bytes)")
        self.convert_log.append(f"Validation: {result.get('validation')}")
        self.result_path.setText(str(path))
        structure = result.get("structure") or {}
        summary = {
            "mode": result.get("mode"),
            "title": structure.get("title"),
            "layout": structure.get("layout"),
            "colors": structure.get("colors"),
            "template": structure.get("template") or self.template.currentText(),
            "validation": result.get("validation"),
            "import_hint": result.get("import_hint"),
            "output": str(path),
        }
        self.result_json.setPlainText(json.dumps(summary, indent=2, ensure_ascii=False))
        if path.exists():
            preview = path.read_text(encoding="utf-8", errors="replace")
            self.result_xml.setPlainText(preview[:8000] + ("\n…" if len(preview) > 8000 else ""))
        self._status(f"Theme ready · {path.name}")
        self._goto("result")

    def _gen_fail(self, msg: str) -> None:
        self.progress.setVisible(False)
        self.convert_log.append(f"✗ Error: {msg}")
        QMessageBox.warning(self, "BloggerEasy", msg)
        self._status("Generation failed")

    # ----- Result -----
    def _page_result(self) -> QWidget:
        page = QWidget()
        lay = QVBoxLayout(page)
        lay.setContentsMargins(28, 24, 28, 24)
        t = QLabel("Generated theme")
        t.setObjectName("h1")
        lay.addWidget(t)
        s = QLabel("XML ready for Blogger Theme → Backup/Restore → Upload")
        s.setObjectName("h2")
        lay.addWidget(s)

        card = _card()
        cl = QVBoxLayout(card)
        cl.setContentsMargins(18, 18, 18, 18)
        self.result_path = QLabel("No file yet — create a theme first.")
        self.result_path.setObjectName("h2")
        self.result_path.setWordWrap(True)
        cl.addWidget(self.result_path)
        row = QHBoxLayout()
        open_btn = _primary("Open XML file")
        open_btn.clicked.connect(self._open_output)
        folder_btn = _secondary("Open folder")
        folder_btn.clicked.connect(self._open_folder)
        val_btn = _secondary("Validate again")
        val_btn.clicked.connect(self._validate_last)
        row.addWidget(open_btn)
        row.addWidget(folder_btn)
        row.addWidget(val_btn)
        row.addStretch(1)
        cl.addLayout(row)
        lay.addWidget(card)

        self.result_json = QTextEdit()
        self.result_json.setReadOnly(True)
        self.result_json.setMaximumHeight(180)
        lay.addWidget(self.result_json)

        xl = QLabel("XML preview")
        xl.setObjectName("h2")
        lay.addWidget(xl)
        self.result_xml = QTextEdit()
        self.result_xml.setReadOnly(True)
        self.result_xml.setStyleSheet("font-family: Consolas, monospace; font-size: 12px;")
        lay.addWidget(self.result_xml, 1)
        return page

    def _open_output(self) -> None:
        if not self._last_output or not self._last_output.exists():
            QMessageBox.information(self, "BloggerEasy", "No output file yet.")
            return
        QDesktopServices.openUrl(QUrl.fromLocalFile(str(self._last_output.resolve())))

    def _open_folder(self) -> None:
        path = self._last_output.parent if self._last_output else OUT_DIR
        path.mkdir(parents=True, exist_ok=True)
        QDesktopServices.openUrl(QUrl.fromLocalFile(str(path.resolve())))

    def _validate_last(self) -> None:
        if not self._last_output or not self._last_output.exists():
            QMessageBox.information(self, "BloggerEasy", "No output file yet.")
            return
        result = validate_theme_file(self._last_output)
        self.result_json.append("\n" + json.dumps(result, indent=2))
        if result.get("ok"):
            self._status("Validation OK")
        else:
            QMessageBox.warning(self, "BloggerEasy", f"Validation issues: {result}")

    # ----- Templates -----
    def _page_templates(self) -> QWidget:
        page = QWidget()
        lay = QVBoxLayout(page)
        lay.setContentsMargins(28, 24, 28, 24)
        t = QLabel("Style templates")
        t.setObjectName("h1")
        lay.addWidget(t)
        s = QLabel("Preset applied on top of parsed structure / image palette")
        s.setObjectName("h2")
        lay.addWidget(s)
        lst = QListWidget()
        for name, meta in PRESETS.items():
            item = QListWidgetItem(f"{name}  —  {meta}")
            item.setData(Qt.ItemDataRole.UserRole, name)
            lst.addItem(item)
        lst.itemDoubleClicked.connect(self._apply_template_item)
        lay.addWidget(lst, 1)
        tip = QLabel("Double-click to select template on the Create theme page.")
        tip.setObjectName("hint")
        lay.addWidget(tip)
        return page

    def _apply_template_item(self, item: QListWidgetItem) -> None:
        name = item.data(Qt.ItemDataRole.UserRole)
        if name:
            self.template.setCurrentText(str(name))
            self._goto("convert")
            self._status(f"Template: {name}")

    # ----- Import guide -----
    def _page_import(self) -> QWidget:
        page = QWidget()
        lay = QVBoxLayout(page)
        lay.setContentsMargins(28, 24, 28, 24)
        t = QLabel("Import into Blogger")
        t.setObjectName("h1")
        lay.addWidget(t)
        card = _card()
        cl = QVBoxLayout(card)
        cl.setContentsMargins(20, 20, 20, 20)
        steps = QLabel(
            "<ol style='line-height:1.7'>"
            "<li>Open <b>Blogger</b> → your blog → <b>Theme</b>.</li>"
            "<li>Click the menu <b>⋮</b> → <b>Backup</b> (download current theme first).</li>"
            "<li>Choose <b>Restore</b> / <b>Upload</b> and select the generated <code>.xml</code>.</li>"
            "<li>Confirm upload — Blogger applies layout, CSS skin, and widgets.</li>"
            "<li>Preview the blog; tweak colors under Theme customize if needed.</li>"
            "</ol>"
            "<p style='color:#94a3b8'>File location defaults to <code>data/out/</code> in this project.</p>"
            "<p style='color:#64748b'>Tip: always keep a backup of your previous theme before restore.</p>"
        )
        steps.setWordWrap(True)
        steps.setTextFormat(Qt.TextFormat.RichText)
        cl.addWidget(steps)
        open_blogger = _primary("Open blogger.com")
        open_blogger.clicked.connect(
            lambda: QDesktopServices.openUrl(QUrl("https://www.blogger.com/"))
        )
        cl.addWidget(open_blogger, alignment=Qt.AlignmentFlag.AlignLeft)
        lay.addWidget(card)
        lay.addStretch(1)
        return page

    # ----- Demo -----
    def _page_demo(self) -> QWidget:
        page = QWidget()
        lay = QVBoxLayout(page)
        lay.setContentsMargins(28, 24, 28, 24)
        t = QLabel("Offline sample demo")
        t.setObjectName("h1")
        lay.addWidget(t)
        s = QLabel("Generate themes for every HTML under data/samples/html (no network).")
        s.setObjectName("h2")
        lay.addWidget(s)
        btn = _primary("Run sample batch")
        btn.clicked.connect(self.run_demo_batch)
        lay.addWidget(btn, alignment=Qt.AlignmentFlag.AlignLeft)
        self.demo_log = QTextEdit()
        self.demo_log.setReadOnly(True)
        lay.addWidget(self.demo_log, 1)
        return page

    def run_demo_batch(self) -> None:
        root = OUT_DIR / "demo"
        root.mkdir(parents=True, exist_ok=True)
        samples = (
            sorted((SAMPLES_DIR / "html").glob("*.html")) if (SAMPLES_DIR / "html").exists() else []
        )
        self.demo_log.clear()
        if not samples:
            self.demo_log.append("No samples found.")
            return
        template_for = {
            "portfolio.html": "portfolio",
            "news_portal.html": "news",
            "dark_dev.html": "dark",
            "magazine.html": "magazine",
        }
        for path in samples:
            out = root / f"{path.stem}.xml"
            tmpl = template_for.get(path.name, "simple")
            try:
                result = generate_from_html(path, out, template=tmpl)
                ok = result["validation"].get("ok")
                self.demo_log.append(f"{'✓' if ok else '·'} {path.name} → {out.name} ok={ok}")
            except Exception as exc:  # noqa: BLE001
                self.demo_log.append(f"✗ {path.name}: {exc}")
        self.demo_log.append(f"\nDone → {root}")
        self.demo_log.append("Import any XML: Blogger → Theme → Backup/Restore → Upload")
        self._last_output = root / f"{samples[0].stem}.xml"
        self._status(f"Demo complete · {len(samples)} themes")
