from kopper.station import Station


def get_name_from_code(enum_cls, code):
    """constants에 있는 enum 클래스의 키 값 반환.
    
    Args:
        constants.enum_class (Enum): Enum이 상속된 클래스
        constants.enum_class.value (Enum.value): Enum이 상속된 클래스 value 값

    Returns:
        str: constants.enum_class.key, value 값과 일치하는 key 값

    >>> from constants.days import DAYS
    >>> get_name_from_code(DAYS, 0)
    '월'

    >>> from constants.train_type import TRAIN_TYPE
    >>> get_name_from_code(TRAIN_TYPE, '09')
    'ITX_청춘'
    >>> get_name_from_code(TRAIN_TYPE, '10')
    'ITX_청춘'
    """

    names_single = [
        name for name, member in enum_cls.__members__.items()
        if member.value == code
    ]
    names_multiple = [
        name for name, member in enum_cls.__members__.items()
        if type(member.value) == tuple and code in member.value
    ]

    if not names_single and not names_multiple:
        raise ValueError("""Trains information is not enough.
            Please, add info(name, code) in 'enum/trains.py'.
            """)

    return names_single[0] if len(names_single) else names_multiple[0]


def get_stations(parsed_train_stations):
    """선택한 기차가 통과하는 정거장에 대한 인스턴스 일괄 생성.
    
    일괄 생성된 정거장 인스턴스들은 Schedule 클래스에서 Argument로 사용.
    
    Args:
        parsed_train_stations: helper.parsing_raw_train_stations에서 반환된 파싱 정보. 

    Returns:
        list: [<class 'station.Station'>, <class 'station.Station'>, ...]

    Notes:
        Crawler.train_stations에서 선택한 기차의 시간표 정보(HTML source)로 얻은 뒤, helper.parsing_raw_train_stations에서 파싱된 정보를 인자로 사용합니다.

    """
    return [
        Station(raw_station_info) for raw_station_info in parsed_train_stations
    ]
