from monitor_info import MonitorManager
from typing import List, Dict
from enum import IntEnum
import product_name


def format_bytes(data: bytes):
    # 將 bytes 轉換為十六進位字串，每兩個字元一組
    hex_str = data.hex().upper()
    pairs = [hex_str[i : i + 2] for i in range(0, len(hex_str), 2)]

    # 每16組加換行符號
    lines: List[str] = []
    for i in range(0, len(pairs), 16):
        line = " ".join(pairs[i : i + 16])
        lines.append(line)

        # 每8行（128組）後加額外換行
        if (i // 16 + 1) % 8 == 0 and i + 16 < len(pairs):
            lines.append("")  # 空行

    return "\n".join(lines)


class BlockType(IntEnum):
    STANDARD = 0
    CTA_EXTENSION = 1
    DISPLAY_ID = 2
    BLOCK_MAP = 3


def main() -> list[dict[str, str]]:

    manager = MonitorManager()
    monotor_info = manager.monitor_read()
    EDID_info_list: list[dict[str, str]] = []

    if not monotor_info.active_monitors:
        print("未找到活耀顯示器資訊")
        return []

    print(f"偵測到 {len(monotor_info.active_monitors)} 個活躍顯示器")

    for index, monitor in enumerate(monotor_info.active_monitors, 1):
        raw_data = manager.display_monitor_info(
            index, monitor, monotor_info.registry_paths
        )
        """這裡放置想要進一步解析的內容"""
        if raw_data is None:
            continue
        EDID_info: Dict[str, str] = {}
        EDID_info["product_name"] = product_name.parse(raw_data)
        if not EDID_info["product_name"]:
            EDID_info["product_name"] = "內建顯示器"
        EDID_info["EDIDRawData"] = format_bytes(raw_data)

        EDID_info_list.append(EDID_info)

        """每次結束解析時,將raw_data拋出來"""

    print()
    print(EDID_info_list)
    print("\n程式執行完畢，如果有遺漏的顯示器，請將顯示設定改為延伸模式後再試一次")
    return EDID_info_list


if __name__ == "__main__":
    main()
