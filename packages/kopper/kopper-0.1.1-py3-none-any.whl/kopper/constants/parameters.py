import enum


class PARAMETERS(enum.Enum):
    train_info = {
        'checkStnNm': 'Y',
        'chkCpn': 'N',
        'radJobId': '1',
        'SeandYo': 'N',
        'selGoDay': '',     # selected depart day (dd)
        'selGoHour': '',    # selected depart hour (HH)
        'selGoMonth': '',   # selected depart month (MM)
        'selGoSeat1': '015',
        'selGoTrain': '',   # train type code
        'selGoYear': '',    # selected depart year
        'start': '',        # selected depart date (YYYY.m.d)
        'txtGoAbrdDt': '',  # selected depart date (YYYYmmdd)
        'txtGoEnd': '',     # arrival station name
        'txtGoHour': '',    # selected depart time (HHMMSS)
        'txtGoPage': '1',
        'txtGoStart': '',   # department station name
        'txtGoYoil': '',    # selected a day of the week
        'txtMenuId': '11',
        'txtPsgCnt1': '1',
        'txtPsgCnt2': '0',
        'txtPsgFlg_1': '1',
        'txtPsgFlg_2': '0',
        'txtPsgFlg_3': '0',
        'txtPsgFlg_4': '0',
        'txtPsgFlg_5': '0',
        'txtSeatAttCd_2': '000',
        'txtSeatAttCd_3': '000',
        'txtSeatAttCd_4': '015',
    }

    # 'txtRunDt' and 'txtDptDt' can have the same value.
    route_info = {
        'txtDptDt': '',     # YYYYmmdd
        'txtRunDt': '',     # YYYYmmdd 
        'txtTrnGpCd': '',   # train's group code
        'txtTrnNo': '',     # train's no
    }

    srcar_length_info = {
        'radJobId': '1',
        'txtArvRsStnCd': '',        # arrival station code (NNNN: zero filed)
        'txtArvStnRunOrdr': '',     # used by train instance (NNNNNN:zero filed)
        'txtArvTm': '',             # arrival time (HHMMSS)
        'txtDptDt': '',             # depart date (YYYYmmdd)
        'txtDptRsStnCd': '',        # depart station code (NNNN: zero filed)
        'txtDptStnRunOrdr': '',     # used by train instance (NNNNNN:zero filed)
        'txtDptTm': '',             # depart time (HHMMSS)
        'txtPsrmClCd': '1',
        'txtRunDt': '',             # depart date (YYYYmmdd)
        'txtSeatAttCd': '015',
        'txtSrcarNo': '1',
        'txtTotPsgCnt': '1',
        'txtTrnClsfCd': '',         # train's classification code
        'txtTrnGpCd': '',           # train's group code
        'txtTrnNo': '',             # train's no
    }
    
    seat_info = {
        'txtArvRsStnCd': '',        # arrival station code (NNNN: zero filed)
                                    # used by train instance
        'txtArvStnRunOrdr': '',     # used by train instance (NNNNNN:zero filed)
        'txtDptRsStnCd': '',        # depart station code (NNNN: zero filed)
        'txtDptStnRunOrdr': '',     # used by train instance (NNNNNN:zero filed)
                                    # used by train instance
        'txtPsrmClCd': '1',
        'txtRunDt': '',             # train departure date (YYYYmmdd)
        'txtSeatAttCd': '015',
        'txtSrcarNo': '',           # selected #. of 'arrSrcarNo'
        'txtTotPsgCnt': '1',
        'txtTrnClsfCd': '',         # used by train instance
        'txtTrnGpCd': '',           # used by train instance
        'txtTrnNo': '',             # used by train instance
    }

