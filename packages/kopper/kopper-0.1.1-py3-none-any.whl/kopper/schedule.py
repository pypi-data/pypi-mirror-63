class Schedule(object):
    """기차 운행 정보

    Attributes:
        train_routes: 선택한 기차 통과 정거장
    """
    def __init__(self, train, stations):
        self._train = train
        self._stations = stations

        self._initialize()

    def _initialize(self):
        sorted_stations = sorted(self._stations)

        train_routes = []

        for idx, (station, next_station) in enumerate(
                zip(sorted_stations[:-1], sorted_stations[1:])):
            station.depart_order = idx + 1
            station.arrival_order = idx + 2

            station.next_station = next_station

            train_routes.append(station)

        order_depart = 0
        order_arrival = len(train_routes)

        for order_idx, station in enumerate(train_routes):
            if '{:04d}'.format(int(
                    self._train.depart_station_code)) == station.station_code:
                order_depart = order_idx
                break

        for order_idx, station in enumerate(train_routes):
            if '{:04d}'.format(int(self._train.arrival_station_code)
                               ) == station.next_station_code:
                order_arrival = order_idx
                break

        self._sorted_routes = train_routes[order_depart:order_arrival + 1]

    def print_routes(self, depart_station_idx, arrival_station_idx):
        """train_routes의 정차역을 index를 통해 정보를 출력합니다.

        Args:
            deaprt_station_idx: 출발 정차역 index
            arrival_station_idx: 도착 정차역 index
        """
        depart_station = self.train_routes[depart_station_idx]
        arrival_station = self.train_routes[arrival_station_idx]

        print('{} ({}) - {} ({})'.format(
            depart_station.station_name,
            depart_station.depart_time,
            arrival_station.next_station.station_name,
            arrival_station.next_station.arrival_time,
        ))

    @property
    def train_routes(self):
        return self._sorted_routes

    def __str__(self):
        # 서울 (14:00) - 광명 (14:14)
        # 광명 (14:16) - 오송 (14:43)
        # 오송 (14:45) - 대전 (15:00)
        # 대전 (15:02) - 동대구 (15:45)
        # 동대구 (15:47) - 부산 (16:27)
        msg = ''
        for depart_route in self.train_routes:
            msg += '{} ({}) - {} ({}) \n'.format(
                depart_route.station_name, depart_route.depart_time,
                depart_route.next_station.station_name,
                depart_route.next_station.arrival_time)

        return msg.strip()
