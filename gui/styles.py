DARK_STYLESHEET = """
QMainWindow {
    background-color: #121212;
}

QLabel#pageTitle {
    color: #e8e8e8;
    font-size: 22px;
    font-weight: bold;
}

QLabel#pageSubtitle {
    color: #9d9d9d;
    font-size: 13px;
}

QLabel#sectionHint {
    color: #858585;
    font-size: 12px;
    margin-top: 2px;
    margin-bottom: 8px;
}

QLabel#tableSectionTitle {
    color: #c8c8c8;
    font-size: 12px;
    font-weight: bold;
    margin-top: 12px;
    margin-bottom: 4px;
}

QFrame#infoStrip {
    background-color: #252526;
    border: 1px solid #3e3e42;
    border-radius: 8px;
    padding: 2px;
}

QLabel#infoStripText {
    color: #b8b8b8;
    font-size: 12px;
    padding: 10px 14px;
}

QLabel#dataStatusBanner {
    border-radius: 8px;
    padding: 10px 14px;
    font-size: 12px;
}

QLabel#dataStatusBanner[warning="true"] {
    background-color: #3d2e10;
    border: 1px solid #8a6d2a;
    color: #f0d090;
}

QLabel#dataStatusBanner[warning="false"] {
    background-color: #1a2e24;
    border: 1px solid #2d6a4f;
    color: #a8d5ba;
}

QLabel#emptyStateTitle {
    color: #e8e8e8;
    font-size: 18px;
    font-weight: bold;
}

QLabel#assignmentSummary {
    color: #9d9d9d;
    font-size: 13px;
}

QScrollArea {
    border: none;
    background-color: transparent;
}

QScrollArea > QWidget > QWidget {
    background-color: transparent;
}

QSplitter::handle {
    background-color: #3e3e42;
    width: 3px;
}

QSplitter::handle:hover {
    background-color: #007acc;
}

QStatusBar {
    background-color: #252526;
    color: #b0b0b0;
    border-top: 1px solid #3e3e42;
    font-size: 12px;
    padding: 4px 8px;
}

QTabWidget::pane {
    border: 1px solid #333333;
    background-color: #1e1e1e;
    border-radius: 4px;
}

QTabBar::tab {
    background-color: #252526;
    color: #cccccc;
    padding: 12px 25px;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
    margin-right: 2px;
    font-weight: bold;
}

QTabBar::tab:selected {
    background-color: #007acc;
    color: white;
}

QTabBar::tab:hover:!selected {
    background-color: #3e3e42;
}

QGroupBox {
    color: #4fc1ff;
    font-size: 14px;
    font-weight: bold;
    border: 1px solid #333333;
    border-radius: 8px;
    margin-top: 25px;
    padding-top: 15px;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 5px;
}

QPushButton {
    background-color: #333333;
    color: white;
    border: none;
    border-radius: 4px;
    padding: 10px 20px;
    font-weight: bold;
    font-size: 13px;
}

QPushButton:hover {
    background-color: #454545;
}

QPushButton:pressed {
    background-color: #007acc;
}

QPushButton#primaryAction {
    background-color: #0e639c;
}

QPushButton#primaryAction:hover {
    background-color: #1177bb;
}

QPushButton#dangerAction {
    background-color: #941111;
}

QPushButton#dangerAction:hover {
    background-color: #b31515;
}

QLineEdit, QSpinBox, QComboBox {
    background-color: #2d2d2d;
    color: #e0e0e0;
    border: 1px solid #3e3e42;
    border-radius: 4px;
    padding: 8px;
    font-size: 13px;
}

QLineEdit:focus, QSpinBox:focus, QComboBox:focus {
    border: 1px solid #007acc;
}

QTableWidget {
    background-color: #1e1e1e;
    color: #d4d4d4;
    gridline-color: #333333;
    border: none;
    selection-background-color: #264f78;
    alternate-background-color: #252526;
}

QHeaderView::section {
    background-color: #252526;
    color: #cccccc;
    padding: 8px;
    border: 1px solid #333333;
    font-weight: bold;
}

QProgressBar {
    border: 1px solid #333333;
    border-radius: 10px;
    text-align: center;
    background-color: #2d2d2d;
    color: white;
    height: 25px;
    font-weight: bold;
}

QProgressBar::chunk {
    background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #007acc, stop:1 #4fc1ff);
    border-radius: 10px;
}

QTextEdit {
    background-color: #1e1e1e;
    color: #9cdcfe;
    font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
    border: 1px solid #333333;
    padding: 10px;
    line-height: 1.5;
}

QLabel {
    color: #cccccc;
    font-size: 13px;
}

QScrollBar:vertical {
    border: none;
    background: #1e1e1e;
    width: 12px;
    margin: 0px 0 0px 0;
}

QScrollBar::handle:vertical {
    background: #333333;
    min-height: 20px;
    border-radius: 6px;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    border: none;
    background: none;
}
"""
