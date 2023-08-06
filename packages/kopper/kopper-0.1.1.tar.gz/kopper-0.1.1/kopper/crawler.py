from datetime import datetime
from requests import Session
import requests

from kopper.helper import get_name_from_code

from kopper.constants.days import DAYS
from kopper.constants.links import LINKS
from kopper.constants.parameters import PARAMETERS
from kopper.constants.stations import STATIONS
from kopper.constants.train_type import TRAIN_TYPE


class Crawler(object):
    """Korail 홈페이지에서 정보 수집 클래스
    """
    def __init__(self):
        self._session = Session()

    def trains_info(self, depart_date, depart_time, depart, arrival,
                    train_type):
        """출발일자, 출발시간, 출발역, 도착역, 기차 유형을 요청하고 HTML source 수집.

        Args:
            depart_date (str): 출발일자(YYYYmmdd)
            depart_time (str): 출발시간(HHMMSS)
            depart (STATIONS.value): 출발역
            arrival (STATIONS.value): 출발역
            train_type (TRAIN_TYPE.value): 기차 유형

        Returns:
            str: HTML source
        """
        _params = PARAMETERS.train_info.value

        _date = datetime.strptime(depart_date, "%Y%m%d")
        _time = datetime.strptime(depart_time, "%H%M%S")

        _params.update({
            "selGoDay":
            '{:02d}'.format(_date.day),  # selected depart day
            "selGoHour":
            '{:02d}'.format(_time.hour),  # selected depart hour (HH)
            "selGoMonth":
            '{:02d}'.format(_date.month),  # selected depart month
            "selGoTrain":
            train_type.value[0] if type(train_type.value) is tuple else
            train_type.value,  # train type code
            "selGoYear":
            '{:d}'.format(_date.year),  # selected depart year
            "start":
            datetime.strftime(_date, "%Y.%m.%d").replace(
                ".0", "."),  # selected depart date (yyyy.M.d)
            "txtGoAbrdDt":
            datetime.strftime(_date,
                              "%Y%m%d"),  # selected depart date (yyyyMMdd)
            "txtGoEnd":
            get_name_from_code(STATIONS,
                               arrival.value),  # arrival station name
            "txtGoHour":
            depart_time,  # selected depart time (HHmmss)
            "txtGoStart":
            get_name_from_code(STATIONS,
                               depart.value),  # department station name
            "txtGoYoil":
            get_name_from_code(
                DAYS, _date.weekday()),  # selected a day code of the week.
        })

        response = self._session.post(LINKS.train_info.value, data=_params)
        html = response.text

        return response.status_code, html

    def train_stations(self, train):
        """선택한 기차 시간표를 요청하고 HTML source 수집.

        Args:
            train (class 'train.Train'): 기차 인스턴스

        Returns:
            str: HTML source
        """
        return self._train_stations(train.run_date, train.depart_date,
                                    train.train_no, train.train_group_code)

    def _train_stations(self, run_date, depart_date, train_no,
                        train_group_code):
        """선택한 기차 시간표를 요청하고 HTML source 수집.

        Args:
            run_date (str): 운행일자(YYYYmmdd)
            depart_date (str): 출발일자(YYYYmmdd)
            train_no (str): 기차 번호
            train_no (str): 기차 그룹 코드

        Returns:
            str: HTML source
        """
        _params = PARAMETERS.route_info.value

        _params.update({
            'txtRunDt': run_date,  # YYYYmmdd
            'txtDptDt': depart_date,  # YYYYmmdd
            'txtTrnNo': train_no,
            'txtTrnGpCd': train_group_code,
        })

        response = requests.get(LINKS.route_info.value, params=_params)
        html = response.text

        return response.status_code, html

    def train_srcar_length(self, train):
        """선택한 기차 칸 번호를 요청하고 HTML source 수집.

        Args:
            train (class 'train.Train'): 기차 인스턴스

        Returns:
            str: HTML source
        """
        _params = PARAMETERS.srcar_length_info.value

        _params.update({
            'txtArvRsStnCd':
            '{:04d}'.format(int(train.arrival_station_code)
                            ),  # arrival station code (NNNN: zero filed)
            'txtArvStnRunOrdr':
            train.raw_train_info[
                'h_arv_stn_run_ordr'],  # used by train instance (NNNNNN:zero filed)
            'txtArvTm':
            train.arrival_time,  # arrival time (HHMMSS)
            'txtDptDt':
            train.depart_date,  # depart date (YYYYmmdd)
            'txtDptRsStnCd':
            '{:04d}'.format(int(train.depart_station_code)
                            ),  # depart station code (NNNN: zero filed)
            'txtDptStnRunOrdr':
            train.raw_train_info[
                'h_dpt_stn_run_ordr'],  # used by train instance (NNNNNN:zero filed)
            'txtDptTm':
            train.depart_time,  # depart time (HHMMSS)
            'txtPsrmClCd':
            '1',
            'txtRunDt':
            train.depart_date,  # depart date (YYYYmmdd)
            'txtSeatAttCd':
            '015',
            'txtSrcarNo':
            '1',
            'txtTotPsgCnt':
            '1',
            'txtTrnClsfCd':
            train.train_classification_code,  # train's classification code
            'txtTrnGpCd':
            train.train_group_code,  # train's group code
            'txtTrnNo':
            train.train_no,  # train's no
        })

        response = requests.get(LINKS.srcar_length_info.value, params=_params)
        html = response.text

        return response.status_code, html

    def train_seats_by_schedule(self, train, schedule, srcar_length):
        """선택한 기차 정보와 운행 시간표를 참고하여 일괄적으로 좌석 상태를 요청하고 HTML source 수집.

        Args:
            train (class 'train.Train'): 기차 인스턴스
            schedule (class 'schedule.Schedule'): 기차 시간표 인스턴스
            srcar_length (list): 기차 칸 번호 리스트

        Returns:
            dict: HTML source
        """
        seats_info = {}

        for route in schedule.train_routes:
            seats_info[route] = {}

            for srcar_no in srcar_length:
                _, html = self.train_seat_by_route(train, route, srcar_no)
                seats_info[route][srcar_no] = html

        return seats_info

    def train_seat_by_route(self, train, station, srcar_no):
        """| 선택한 기차 정보와 운행 시간표의 정차역 정보, 기차 칸 번호를 참고하여 정차역에서 다음 정차역까지 좌석 상태를 요청하고 HTML source 수집.

        Args:
            train (class 'train.Train'): 기차 인스턴스
            schedule (class 'station.Station'): 정차역 인스턴스
            srcar_no: 기차 칸 번호

        Returns:
            dict: HTML source
        """
        _params = PARAMETERS.seat_info.value

        _params.update({
            'txtArvRsStnCd':
            '{:04d}'.format(int(station.next_station.station_code)
                            ),  # arrival station code (NNNN: zero filed)
            'txtArvStnRunOrdr':
            '{:06d}'.format(station.arrival_order
                            ),  # used by train instance (NNNNNN:zero filed)
            'txtDptRsStnCd':
            '{:04d}'.format(int(station.station_code)
                            ),  # depart station code (NNNN: zero filed)
            'txtDptStnRunOrdr':
            '{:06d}'.format(station.depart_order
                            ),  # used by train instance (NNNNNN:zero filed)
            'txtRunDt':
            train.depart_date,  # depart date (YYYYmmdd)
            'txtSrcarNo':
            srcar_no,  # selected #. of 'arrSrcarNo'
            'txtTrnClsfCd':
            train.train_classification_code,  # train's classification code
            'txtTrnGpCd':
            train.train_group_code,  # train's group code
            'txtTrnNo':
            train.train_no,  # train's no
        })

        response = self._session.post(LINKS.seat_info.value, data=_params)
        html = response.text

        return response.status_code, html
