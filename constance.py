class Constance:
    history = []
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
    historyI1I2 = []
    root = None
    isManualRecord = True
    intervalTime = 0.1
    
    formulaIP1 = None
    symbolIP1 = "I1"
    fromValueIP1 = 0
    toValueIP1 = 30
    decimalPlacesIP1 = 2

    formulaIP2 = None
    symbolIP2 = "I2"
    fromValueIP2 = 0
    toValueIP2 = 30
    decimalPlacesIP2 = 2

    ind = []

    indexSeparate = 0