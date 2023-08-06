device_list = [
    {
        'name': 'auto',
        'dev_type': 0,
        'protocol_version': 0,
        'userapp_start': 0,
        'userapp_size':  0,
        'note': 'Default, auto detext device type.'
        # 預設值，選用此參數會自動判斷裝置。
    },
    {
        'name': 'asa_m128_v1',
        'dev_type': 1,
        'protocol_version': 1,
        'userapp_start': 0x00000000,
        'userapp_size':  0x0001F000,
        'note': ''
    },
    {
        'name': 'asa_m128_v2',
        'dev_type': 2,
        'protocol_version': 1,
        'userapp_start': 0x00000000,
        'userapp_size':  0x0001F000,
        'note': ''
    },
    {
        'name': 'asa_m128_v3',
        'dev_type': 3,
        'protocol_version': 2,
        'userapp_start': 0x00000000,
        'userapp_size':  0x0001F000,
        'note': ''
    },
    {
        'name': 'asa_m3_v1',
        'dev_type': 4,
        'protocol_version': 2,
        'userapp_start': 0x00001000,
        'userapp_size':  0x0007F000,
        'note': ''
    }
]
