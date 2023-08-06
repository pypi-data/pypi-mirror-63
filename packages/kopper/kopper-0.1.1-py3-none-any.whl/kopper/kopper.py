from kopper.algorithms import *
from kopper.crawler import Crawler
from kopper.helper import *
from kopper.parser import *
from kopper.schedule import Schedule
from kopper.train import Train


class Kopper(object):
    """Kopper 메인 클래스
    """
    def __init__(self):
        self._crawler = Crawler()

    def trains_info(self, depart_date, depart_time, depart, arrival,
                    train_type):
        """출발일자, 출발시간, 출발역, 도착역, 기차 유형을 요청한 결과 반환.

        Args:
            depart_date (str): 출발일자(YYYYmmdd)
            depart_time (str): 출발시간(HHMMSS)
            depart (STATIONS.value): 출발역
            arrival (STATIONS.value): 출발역
            train_type (TRAIN_TYPE.value): 기차 유형

        Returns:
            list: [<class 'train.Train'>, ...]
        """
        status_code, raw_html = self._crawler.trains_info(
            depart_date, depart_time, depart, arrival, train_type)
        parsed_trains_info = parsing_raw_trains_info(raw_html)

        return [
            Train(parsed_train_info)
            for parsed_train_info in parsed_trains_info
        ]

    def train_schedule(self, train):
        """선택한 기차 시간표를 요청한 결과 반환.

        Args:
            train (class 'train.Train'): 기차 인스턴스

        Returns:
            <class 'schedule.Schedule'>
        """
        status_code, raw_html = self._crawler.train_stations(train)
        parsed_train_stations = parsing_raw_train_stations(raw_html)
        train_stations = get_stations(parsed_train_stations)

        return Schedule(train, train_stations)

    def train_srcar_length(self, train):
        """선택한 기차 칸 번호를 요청한 결과 반환.

        Args:
            train (class 'train.Train'): 기차 인스턴스

        Returns:
            list: 기차 칸 번호 리스트
        """
        status_code, raw_html = self._crawler.train_srcar_length(train)
        return parsing_raw_srcar_length(raw_html)

    def train_seats_by_schedule(self, train, schedule, srcar_length):
        """선택한 기차 정보와 운행 시간표를 참고하여 일괄적으로 좌석 상태를 요청하고 결과 반환.

        Args:
            train (class 'train.Train'): 기차 인스턴스
            schedule (class 'schedule.Schedule'): 기차 시간표 인스턴스
            srcar_length (list): 기차 칸 번호 리스트

        Returns:
            dict: | { '정거장 A': { '칸 번호 1': { '1A 좌석': 0, '1B 좌석': 1, ..., }, 
            | '칸 번호 2': { ..., } }, 
            | '정거장 B': { ... }, 
            | ... 
            | }
        """
        raw_train_seats_info = self._crawler.train_seats_by_schedule(
            train, schedule, srcar_length)
        return parsing_raw_seats_by_schedule(raw_train_seats_info)

    def report_routes(self, schedule, parsed_seats_info):
        """train_routes의 정차역을 index를 통해 정보를 출력합니다.

        Args:
            deaprt_station_idx: 출발 정차역 index
            arrival_station_idx: 도착 정차역 index
        """
        graph = make_graph(parsed_seats_info)
        list_route_indexs = get_routes_idx(graph)
        for route_indexs in list_route_indexs:
            schedule.print_routes(route_indexs[0], route_indexs[1])
