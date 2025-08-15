class DTDParams:
    """DTD或display descriptor參數"""

    FIRST_DESCRIPTOR_ADDR = 0x36  # perferred timing 的位址
    DESCRIPTOR_SIZE = 18  # 每個DTD或display descriptor的大小
    EDID_BLOCK_SIZE = 128  # EDID的最大長度
    perferred_timing_info = "Undefined"
    perferred_HActive: int = 0
    perferred_VActive: int = 0
    timing_resolution = "Undefined"
    DESCRIPTOR_TAGS = {
        0xFF: "display_serial_number",
        0xFE: "ascii_string",
        0xFD: "display_range_limits",
        0xFC: "display_product_name",
        0xFB: "color_point_data",
        0xFA: "standard_timing",
        0xF9: "dcm_data",
        0xF8: "cvt_timing",
        0xF7: "established_timings_3",
        0x10: "dummy_descriptor",
    }


def parse(
    raw_data: bytes,
    start_addr: int = DTDParams.FIRST_DESCRIPTOR_ADDR,
    offset: int = DTDParams.DESCRIPTOR_SIZE,
) -> str:
    product_name: str = ""
    current_addr = start_addr  # 當前的DTD位址
    dtd_len = (DTDParams.EDID_BLOCK_SIZE - current_addr) // DTDParams.DESCRIPTOR_SIZE
    # 在base EDID處理perferred timing的解析
    if raw_data[:8] == bytes([0x00, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0x00]):
        current_addr += DTDParams.DESCRIPTOR_SIZE  # 取得下一個DTD的位址
        dtd_len = 3

    # 最多3組
    for _ in range(dtd_len):
        # 如果下一組DTD的位址超過EDID的最大長度，就跳出迴圈
        if offset + DTDParams.DESCRIPTOR_SIZE > DTDParams.EDID_BLOCK_SIZE:
            break
        is_display_descriptor = (
            raw_data[current_addr] == 0 and raw_data[current_addr + 1] == 0
        )

        if is_display_descriptor:
            product_name = get_product_name(raw_data, current_addr)
            if product_name:
                break

        current_addr += DTDParams.DESCRIPTOR_SIZE  # 取得下一個DTD的位址

    return product_name


def get_product_name(raw_data: bytes, offset: int) -> str:
    product_name: str = ""
    tag = raw_data[offset + 3]
    descriptor_type = DTDParams.DESCRIPTOR_TAGS.get(tag, "reserved")
    decriptor_data = raw_data[offset + 5 : offset + DTDParams.DESCRIPTOR_SIZE]

    if descriptor_type == "display_product_name":
        product_name = f"{decriptor_data.decode('utf-8').strip()}"

    return product_name
