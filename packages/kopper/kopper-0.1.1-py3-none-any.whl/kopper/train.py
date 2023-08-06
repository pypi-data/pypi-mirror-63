from datetime import datetime

from kopper.constants.train_type import TRAIN_TYPE
from kopper.helper import get_name_from_code


class Train(object):
    """기차 상세 정보: Schedule에 등록하여e Train 정보를 사용합니다.

    Attributes:
        depart_date (str): 출발 일자
        
        arrival_date (str): 도착일자

        depart_station_name: 출발역 이름
        
        arrival_station_name: 도착역 이름

        depart_station_code: 출발역 코드 번호
        
        arrival_station_code: 도착역 코드 번호

        depart_time: 출발 시간
        
        arrival_time: 도착 시간
        
        delay_hour: 지연 시간(분)

        train_no: 기차 번호
        
        train_type_code: 기차 유형 코드 번호
        
        train_type_name: 기차 유형 이름
        
        run_date: 기차 운행 일자

        raw_train_info: 기차 관련 원본 HTML source
        
        train_group_code: 기차 그룹 코드
        
        train_classification_code: 기차 분류 코드
    """

    def __init__(self, raw_train_info):
        self._raw_train_info = raw_train_info
        self._initialize()

    def _initialize(self):
        raw_info = self.raw_train_info

        self._arrival_date = datetime.strptime(raw_info['h_arv_dt'], '%Y%m%d')
        self._arrival_station_code = '{:02d}'.format(
            int(raw_info['h_arv_rs_stn_cd']))
        self._arrival_station_name = raw_info['h_arv_rs_stn_cd_nm']
        self._arrival_time = datetime.strptime(raw_info['h_arv_tm'], '%H%M%S')

        self._depart_date = datetime.strptime(raw_info['h_dpt_dt'], '%Y%m%d')
        self._depart_station_code = '{:02d}'.format(
            int(raw_info['h_dpt_rs_stn_cd']))
        self._depart_station_name = raw_info['h_dpt_rs_stn_cd_nm']
        self._depart_time = datetime.strptime(raw_info['h_dpt_tm'], '%H%M%S')

        self._train_no = raw_info['h_trn_no']
        self._train_type_code = raw_info['h_trn_clsf_cd']
        self._train_type_name = get_name_from_code(TRAIN_TYPE,
                                                   self._train_type_code)
        self._train_group_code = raw_info['h_trn_gp_cd']
        self._train_classification_code = raw_info['h_trn_clsf_cd']

        self._run_date = datetime.strptime(raw_info['h_run_dt'], '%Y%m%d')
        self._delay_hour = datetime.strptime(raw_info['h_dlay_hr'], '%H%M%S')

    @property
    def raw_train_info(self):
        return self._raw_train_info

    @property
    def arrival_date(self):
        return datetime.strftime(self._arrival_date, '%Y%m%d')

    @property
    def arrival_station_code(self):
        return self._arrival_station_code

    @property
    def arrival_station_name(self):
        return self._arrival_station_name

    @property
    def arrival_time(self):
        return datetime.strftime(self._arrival_time, '%H%M%S')

    @property
    def depart_date(self):
        return datetime.strftime(self._depart_date, '%Y%m%d')

    @property
    def depart_station_code(self):
        return self._depart_station_code

    @property
    def depart_station_name(self):
        return self._depart_station_name

    @property
    def depart_time(self):
        return datetime.strftime(self._depart_time, '%H%M%S')

    @property
    def train_no(self):
        return self._train_no

    @property
    def train_type_code(self):
        return self._train_type_code

    @property
    def train_type_name(self):
        return self._train_type_name

    @property
    def train_group_code(self):
        return self._train_group_code

    @property
    def train_classification_code(self):
        return self._train_classification_code

    @property
    def run_date(self):
        return datetime.strftime(self._run_date, '%Y%m%d')

    @property
    def delay_hour(self):
        return datetime.strftime(self._delay_hour, '%H%M%S')

    def __str__(self):
        # No.00101 \t KTX \t 서울(05:15) ------ 부산(07:51)
        return 'No.{} \t {} \t {}({}) ------ {}({})'.format(
            self.train_no, self.train_type_name, self.depart_station_name,
            self.depart_time, self.arrival_station_name, self.arrival_time)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return False
