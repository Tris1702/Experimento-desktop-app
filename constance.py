class Constance:
    history = []
    historyTVV = []
    historyAV = [
        # {
        #     'ampe': 1,
        #     'voltage': 10,
        #     'time': '11:11:11'
        # },
        # {
        #     'ampe': 2,
        #     'voltage': 15,
        #     'time': '11:11:11'
        # },
        # {
        #     'ampe': 3,
        #     'voltage': 22,
        #     'time': '11:11:11'
        # },
        # {
        #     'ampe': 5,
        #     'voltage': 29,
        #     'time': '11:11:11'
        # },
        # {
        #     'ampe': 7,
        #     'voltage': 30,
        #     'time': '11:11:11'
        # }
    ]
    historyCV = [
    #     {
    #         'centimeter': 1,
    #         'voltage': 10,
    #         'time': '11:11:11'
    #     },
    #     {
    #         'centimeter': 2,
    #         'voltage': 15,
    #         'time': '11:11:11'
    #     },
    #     {
    #         'centimeter': 3,
    #         'voltage': 22,
    #         'time': '11:11:11'
    #     },
    #     {
    #         'centimeter': 5,
    #         'voltage': 29,
    #         'time': '11:11:11'
    #     },
    #     {
    #         'centimeter': 7,
    #         'voltage': 30,
    #         'time': '11:11:11'
    #     }
    ]
    historyTV = [
    #     {
    #         'timepoint': 1,
    #         'voltage': 10,
    #         'time': '11:11:11'
    #     },
    #     {
    #         'timepoint': 2,
    #         'voltage': 15,
    #         'time': '11:11:11'
    #     },
    #     {
    #         'timepoint': 3,
    #         'voltage': 22,
    #         'time': '11:11:11'
    #     },
    #     {
    #         'timepoint': 5,
    #         'voltage': 29,
    #         'time': '11:11:11'
    #     },
    #     {
    #         'timepoint': 7,
    #         'voltage': 30,
    #         'time': '11:11:11'
    #     }
    ]
    historyA2V1 = [
        # {
        #     'ampe2': 1,
        #     'voltage1': 10,
        #     'time': '11:11:11'
        # },
        # {
        #     'ampe2': 2,
        #     'voltage1': 15,
        #     'time': '11:11:11'
        # },
        # {
        #     'ampe2': 3,
        #     'voltage1': 22,
        #     'time': '11:11:11'
        # },
        # {
        #     'ampe2': 5,
        #     'voltage1': 29,
        #     'time': '11:11:11'
        # },
        # {
        #     'ampe2': 7,
        #     'voltage1': 30,
        #     'time': '11:11:11'
        # }
    ]
    historyI1I2 = [
        {
            'ampe2': 1,
            'ampe1': 10,
            'time': '11:11:11'
        },
        {
            'ampe2': 2,
            'ampe1': 15,
            'time': '11:11:11'
        },
        {
            'ampe2': 3,
            'ampe1': 22,
            'time': '11:11:11'
        },
        {
            'ampe2': 5,
            'ampe1': 29,
            'time': '11:11:11'
        },
        {
            'ampe2': 7,
            'ampe1': 30,
            'time': '11:11:11'
        }
    ]
    root = None
    isManualRecord = True
    intervalTime = 0.1
    
    formulaIP1 = "IP1/1.0"
    symbolIP1 = "U1"
    fromValueIP1 = 0
    toValueIP1 = 30
    unitIP1 = ""
    decimalPlacesIP1 = 2

    formulaIP2 = "IP2/1.0"
    symbolIP2 = "I2"
    fromValueIP2 = 0
    toValueIP2 = 30
    unitIP2 = ""
    decimalPlacesIP2 = 2

    ind = []