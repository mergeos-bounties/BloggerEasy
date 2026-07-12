"""Modern dark theme for BloggerEasy Qt desktop."""

STYLESHEET = """
* {
  font-family: "Segoe UI", "Inter", sans-serif;
  font-size: 13px;
  color: #e2e8f0;
}
QMainWindow, QWidget#central {
  background: #0c1222;
}
QFrame#sidebar {
  background: #0a0f1c;
  border-right: 1px solid #1e293b;
}
QLabel#brand {
  font-size: 20px;
  font-weight: 800;
  color: #38bdf8;
  padding: 6px 4px 0 4px;
}
QLabel#brandSub {
  color: #64748b;
  font-size: 11px;
  padding: 0 4px 12px 4px;
}
QLabel#h1 {
  font-size: 22px;
  font-weight: 700;
  color: #f8fafc;
}
QLabel#h2 {
  color: #94a3b8;
  font-size: 13px;
}
QLabel#hint {
  color: #64748b;
  font-size: 12px;
}
QFrame#card {
  background: #111827;
  border: 1px solid #1f2937;
  border-radius: 14px;
}
QFrame#dropZone {
  background: #0f172a;
  border: 2px dashed #334155;
  border-radius: 16px;
}
QFrame#dropZone[active="true"] {
  border-color: #38bdf8;
  background: #0c1a2e;
}
QLineEdit, QComboBox, QSpinBox, QTextEdit, QPlainTextEdit {
  background: #0f172a;
  border: 1px solid #334155;
  border-radius: 10px;
  padding: 8px 12px;
  selection-background-color: #0284c7;
}
QComboBox::drop-down { border: none; width: 28px; }
QListWidget {
  background: #0f172a;
  border: 1px solid #1e293b;
  border-radius: 12px;
}
QListWidget::item {
  padding: 10px;
  border-radius: 8px;
}
QListWidget::item:selected {
  background: #0c4a6e;
  color: #e0f2fe;
}
QStatusBar {
  background: #0a0f1c;
  color: #64748b;
  border-top: 1px solid #1e293b;
}
QProgressBar {
  background: #1e293b;
  border: none;
  border-radius: 6px;
  text-align: center;
  color: #e2e8f0;
  height: 14px;
}
QProgressBar::chunk {
  background: qlineargradient(x1:0,y1:0,x2:1,y2:0, stop:0 #0ea5e9, stop:1 #38bdf8);
  border-radius: 6px;
}
QRadioButton { spacing: 8px; }
QRadioButton::indicator {
  width: 16px; height: 16px;
  border-radius: 8px;
  border: 2px solid #475569;
  background: #0f172a;
}
QRadioButton::indicator:checked {
  background: #38bdf8;
  border-color: #7dd3fc;
}
"""
