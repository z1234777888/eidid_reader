import sys


from icon.icon_data import get_moni_icon
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QTextEdit,
)
from datetime import datetime

from PyQt6.QtWidgets import (
    QLabel,
    QPushButton,
    QFileDialog,
    QMessageBox,
    QComboBox,
    QCheckBox,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QTextCursor

from edid_main import main as edid_parser

# 內嵌字體 Inconsolata SemiExpanded
from fonts.embedded_fonts import load_embedded_fonts


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.is_dark_mode = False
        self.product_name: list[str] = []
        self.edid_data_store: dict[str, str] = {}  # 搭配product_name與comboBox
        self.parsed_data_list: list[dict[str, str]] = []
        self.separator_lines = False

        self.themes = {
            "light": """
                QMainWindow {
                    background-color: #FFFFFF;
                    color: #000000;
                }
                QLabel {
                    background-color: #FFFFFF;
                    color: #000000;
                }
                QPushButton {
                    background-color: #F0F0F0;
                    color: #000000;
                    border: 1px solid #CCCCCC;
                    padding: 5px;
                    border-radius: 3px;
                }
                QPushButton:hover {
                    background-color: #E0E0E0;
                }
                QPushButton:focus {
                    border: 1px solid #CCCCCC;
                    outline: none;
                }
                QComboBox {
                    background-color: #FFFFFF;
                    color: #000000;
                    border: 1px solid #CCCCCC;
                    padding: 5px;
                    border-radius: 3px;
                }
                /* 下拉箭頭區域 */
                QComboBox::drop-down {
                    border: none;
                    width: 20px;
                }
                /* 下拉選單的整體容器 */
                QComboBox QAbstractItemView {
                    background-color: #FFFFFF;   /* 選單背景色 */
                    color: #000000;              /* 文字顏色 */
                    border: 1px solid #CCCCCC;
                    selection-background-color: #07c7ed;  /* 選中項目的背景色 */
                    selection-color: #FFFFFF;             /* 選中項目的文字色 */
                    outline: none;
                }
                QComboBox QAbstractItemView::item:hover {
                    background-color: #e0f7fa;
                    color: #000000;
                }
                QTextEdit {
                    background-color: #F5F5F5;
                    color: #000000;
                    border: 1px solid #CCCCCC;
                    font-family: Inconsolata semiexpanded;
                }
                QMessageBox {
                    background-color: #FFFFFF;
                    color: #000000;
                    border: 1px solid #CCCCCC;
                    font-family: Inconsolata semiexpanded;
                }
                QCheckBox {
                    background-color: #FFFFFF;
                    color: #000000;
                }
                QCheckBox::indicator {
                    width: 16px;
                    height: 16px;
                    border: 1px solid #888;
                    border-radius: 1px;
                    background-color: #444;
                }
                QCheckBox::indicator:checked {
                    background-color: #07c7ed;
                    border-color: #000000;
                }
                QCheckBox::indicator:unchecked {
                    width: 16px;
                    height: 16px;
                    background-color: #DEDEDE;
                }
                QCheckBox::indicator:hover {
                    border-color: #aaa;
                }
                
            """,
            "dark": """
                QMainWindow {
                    background-color: #1E1E1E;
                    color: #FFFFFF;
                }
                QLabel {
                    background-color: #1E1E1E;
                    color: #FFFFFF;
                }
                QPushButton {
                    background-color: #3D3D3D;
                    color: #FFFFFF;
                    border: 1px solid #555555;
                    padding: 5px;
                    border-radius: 3px;
                }
                QPushButton:hover {
                    background-color: #4D4D4D;
                }
                QPushButton:focus {
                    border: 1px solid #555555;
                    outline: none;
                }
                QComboBox {
                    background-color: #2D2D2D;
                    color: #FFFFFF;
                    border: 1px solid #3D3D3D;
                    padding: 5px;
                    border-radius: 3px;
                }
                /* 下拉箭頭區域 */
                QComboBox::drop-down {
                    border: none;
                    width: 20px;
                }
                /* 下拉選單的整體容器 */
                QComboBox QAbstractItemView {
                    background-color: #2D2D2D;   /* 選單背景色 */
                    color: #FFFFFF;              /* 文字顏色 */
                    border: 1px solid #3D3D3D;
                    selection-background-color: #07c7ed;  /* 選中項目的背景色 */
                    selection-color: #FFFFFF;             /* 選中項目的文字色 */
                    outline: none;
                }
                QComboBox QAbstractItemView::item:hover {
                    background-color: #e0f7fa;
                    color: #000000;
                }                
                QTextEdit {
                    background-color: #2D2D2D;
                    color: #58c2e5;
                    border: 1px solid #3D3D3D;
                    font-family: Inconsolata semiexpanded;
                }
                QMessageBox {
                    background-color: #1E1E1E;
                    color: #58c2e5;
                    border: 1px solid #2D2D2D;
                    font-family: Inconsolata semiexpanded;
                }
                QCheckBox {
                    background-color: #1E1E1E;
                    color: #FFFFFF;
                }
                QCheckBox::indicator:checked {
                    width: 16px;
                    height: 16px;
                    background-color: #ffb514;
                    border-color: #000000;
                }
                QCheckBox::indicator:unchecked {
                    width: 16px;
                    height: 16px;
                    background-color: #DEDEDE;
                }      

                         
            """,
        }

        self.initUI()

    def initUI(self):
        self.setWindowTitle("EDID讀取器")

        self.setWindowIcon(get_moni_icon())
        self.resize(840, 500)

        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Create toolbar
        toolbar = QHBoxLayout()

        # Font size controls
        font_label = QLabel("字體大小:")
        self.decrease_btn = QPushButton("-")
        self.decrease_btn.setFixedWidth(30)
        self.font_size_label = QLabel("13")
        self.font_size_label.setFixedWidth(30)
        self.font_size_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.increase_btn = QPushButton("+")
        self.increase_btn.setFixedWidth(30)

        # 顯示器數量label
        self.monitor_count_label = QLabel("目前顯示器數量: 0")
        self.monitor_count_label.setStyleSheet("margin-left: 60px;")  # 加一些間距
        self.include_description_checkbox = QCheckBox("添加描述(選擇其他顯示器觸發)")
        self.include_description_checkbox.setChecked(True)  # 預設開啟

        # Create text display
        self.text_display = QTextEdit()
        self.text_display.setReadOnly(True)
        self.text_display.setAcceptRichText(True)  # 允許富文本

        # INCONSOLATA_SEMIEXPANDED-REGULAR
        font_family = load_embedded_fonts()

        self.text_display.setFont(QFont(font_family, int(self.font_size_label.text())))
        # Other controls
        self.refresh_btn = QPushButton("重新整理")
        self.export_btn = QPushButton("匯出目前畫面")
        self.theme_btn = QPushButton("切換夜間模式")
        # ComboBox 初始化
        self.monitor_selector = QComboBox()
        self.monitor_selector.currentIndexChanged.connect(self.on_monitor_changed)

        self.labels = [font_label, self.font_size_label, self.monitor_count_label]

        # Add controls to toolbar
        toolbar.addWidget(font_label)
        toolbar.addWidget(self.decrease_btn)
        toolbar.addWidget(self.font_size_label)
        toolbar.addWidget(self.increase_btn)
        toolbar.addWidget(self.refresh_btn)
        toolbar.addWidget(self.export_btn)
        toolbar.addWidget(self.include_description_checkbox)
        toolbar.addWidget(self.monitor_count_label)
        toolbar.addWidget(self.monitor_selector)
        toolbar.addStretch()
        toolbar.addWidget(self.theme_btn)

        # Add widgets to main layout
        layout.addLayout(toolbar)
        layout.addWidget(self.text_display)

        self.buttons = [
            self.decrease_btn,
            self.increase_btn,
            self.refresh_btn,
            self.export_btn,
            self.theme_btn,
            self.monitor_selector,
            self.include_description_checkbox,
        ]
        # Connect font size buttons
        self.decrease_btn.clicked.connect(self.decrease_font_size)  # type: ignore
        self.increase_btn.clicked.connect(self.increase_font_size)  # type: ignore
        self.refresh_btn.clicked.connect(self.refresh_monitor_info)  # type: ignore
        self.export_btn.clicked.connect(self.export_info)  # type: ignore
        self.theme_btn.clicked.connect(self.toggle_theme)  # type: ignore

        # Initial refresh
        self.refresh_monitor_info()

    def decrease_font_size(self):
        self.adjust_font_size(-2)

    def increase_font_size(self):
        self.adjust_font_size(2)

    def adjust_font_size(self, delta: int):
        """Adjust the font size by the specified delta"""
        current_size = int(self.font_size_label.text())
        new_size = current_size + delta
        if 8 <= new_size <= 36:
            self.font_size_label.setText(str(new_size))
            font = self.text_display.font()
            font.setPointSize(new_size)
            self.text_display.setFont(font)

    def export_info(self):
        """Export the display information to various file formats"""

        product_name = self.monitor_selector.currentText() or "Unknown_Monitor"
        content = self.get_current_display_text()
        name = product_name
        if product_name == "顯示所有顯示器":
            name = ""
            name += "_".join(self.edid_data_store.keys())

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # 修改檔案類型選項，加入 bin 格式
        file_types = "Text Files (*.txt);;" "All Files (*.*)"

        filename, selected_filter = QFileDialog.getSaveFileName(
            self,
            "儲存檔案",
            f"{name}_{timestamp}",
            file_types,
        )

        if not filename:  # 用户取消了对话框
            return

        try:
            # 根据选择的文件类型或文件扩展名处理不同格式
            if selected_filter.startswith("Text Files") or filename.lower().endswith(
                ".txt"
            ):
                self._export_as_txt(filename, content)

            # 显示成功消息
            QMessageBox.information(
                self, "導出成功", f"EDID信息已成功導出到:\n{filename}"
            )

        except Exception as e:
            # 显示错误消息
            QMessageBox.critical(self, "導出失敗", f"導出文件時發生錯誤:\n{str(e)}")

    def _export_as_txt(self, filename: str, content: str):
        """導出txt格式"""
        # 如果文件名没有扩展名，添加.txt
        if not filename.lower().endswith(".txt"):
            filename += ".txt"

        with open(filename, "w", encoding="utf-8") as f:
            # # 加入標題
            # f.write("=" * 60 + "\n")
            # f.write("EDID 顯示器信息導出\n")
            # f.write(f"導出時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            # f.write("=" * 60 + "\n\n")

            # 寫入主要内容
            f.write(content)

            # # 添加文件尾部信息
            # f.write("\n\n" + "=" * 60 + "\n")
            # f.write("導出完成\n")
            # f.write("=" * 60 + "\n")

    def format_edid_data(self, data: dict[str, str]) -> str:
        """將 EDID 資料格式化為類似 format_data.txt 的格式"""
        if not data:
            return "無法讀取顯示器資訊"

        formatted_text: str = ""
        try:
            if "product_name" in data:
                name = data["product_name"]
                self.product_name.append(name)

                formatted_text += "Product Name: "
                formatted_text += name
                formatted_text += "\n\n"

                if "EDIDRawData" in data:
                    formatted_text += "EDID Raw Data: \n"
                    formatted_text += data["EDIDRawData"]

                    self.edid_data_store[name] = data["EDIDRawData"]
            formatted_text += "\n"

        except Exception as e:
            formatted_text += f"資料格式化時發生錯誤: {str(e)}\n"

        return formatted_text

    def combo_box_update(self, data: dict[str, str]):
        # ✅ 儲存格式化結果，並更新 ComboBox
        if "product_name" in data:
            name = data["product_name"]

            # 避免重複加入
            if self.monitor_selector.findText(name) == -1:
                self.monitor_selector.addItem(name)

    def on_monitor_changed(self, index: int):
        """ComboBox 切換時，更新顯示內容"""

        if index < 0:
            return

        # self.text_display.clear()
        # self.update_display()
        include_desc = self.include_description_checkbox.isChecked()
        content = ""
        name = self.monitor_selector.itemText(index)
        if name in self.edid_data_store:
            if include_desc:
                content = self.format_edid_data(
                    self.parsed_data_list[index - 1]
                )  # 更新格式化內容
            else:
                content = self.edid_data_store[name]  # 直接顯示原始EDID數據
            self.text_display.setPlainText(content)
        else:
            for index in range(len(self.parsed_data_list)):
                if "product_name" in self.parsed_data_list[index]:
                    content += f"{'='*16}第{index+1}個顯示器資訊{'='*16}\n"
                    content += (
                        self.format_edid_data(self.parsed_data_list[index]) + "\n"
                    )
            self.text_display.setPlainText(content)

    def get_current_display_text(self) -> str:
        """取得目前畫面顯示的文字（供匯出使用）"""
        return self.text_display.toPlainText()

    def update_display(self):
        """更新顯示內容基於選擇的資訊類型"""

        for index in range(len(self.parsed_data_list)):
            self.parsed_data = self.parsed_data_list[index]
            if self.parsed_data:

                content = self.format_edid_data(self.parsed_data)
                self.combo_box_update(self.parsed_data)
                self.text_display.append(f"{'='*16}第{index+1}個顯示器資訊{'='*16}")
                self.text_display.append(content)

                self.monitor_count_label.setText(f"目前顯示器數量: {index+1}")
            else:
                self.text_display.clear()
                self.text_display.append("無法讀取顯示器資訊，請確認顯示器連接正常")

        # 更新完內容移動游標到內容的開頭
        self.text_display.moveCursor(QTextCursor.MoveOperation.Start)

    def refresh_monitor_info(self):
        """Refresh monitor information"""
        self.text_display.clear()
        self.edid_data_store.clear()  # ✅ 清除舊資料

        # ✅ 重置 ComboBox，第一項固定為「顯示所有顯示器」
        self.monitor_selector.blockSignals(True)  # 避免觸發 on_monitor_changed
        self.monitor_selector.clear()
        self.monitor_selector.addItem("顯示所有顯示器")
        self.monitor_selector.blockSignals(False)

        try:
            # 調用 EDID 解析器
            self.parsed_data_list = edid_parser()
            self.update_display()

        except Exception as e:
            self.text_display.clear()
            self.text_display.append(f"讀取顯示器資訊時發生錯誤: {str(e)}")

        # 套用主題
        if self.is_dark_mode:
            self.setStyleSheet(self.themes["dark"])
        else:
            self.setStyleSheet(self.themes["light"])

    def toggle_theme(self):
        """Toggle between light and dark themes"""
        self.is_dark_mode = not self.is_dark_mode
        theme = "dark" if self.is_dark_mode else "light"

        # 直接使用主題字串
        self.setStyleSheet(self.themes[theme])

        # 更新按鈕文字
        self.theme_btn.setText("切換日間模式" if self.is_dark_mode else "切換夜間模式")


def main():
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
