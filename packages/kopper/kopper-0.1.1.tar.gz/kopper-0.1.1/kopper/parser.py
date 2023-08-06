from bs4 import BeautifulSoup
import re

from kopper.constants.parsing_map import PARSING_MAP


def parsing_raw_trains_info(raw_html):
    """출발날짜, 출발시간, 출발역, 도착역, 기차유형 요청에 대한 응답 결과를 파싱.

    Args:
        raw_html (str): Crawler.trains_info에서 얻은 HTML source.

    Returns:
        list: [{"key": "value", ...}, {...}, ...]
    """

    rgx_pattern = r'train_info\((.*)\)'

    soup = BeautifulSoup(raw_html, "html.parser")

    js_soup_tags = soup.find_all("script", {
        "type": "text/javascript",
        "language": "javascripts"
    })

    trains = []

    for js_soup in js_soup_tags:
        js_text = ''.join(js_soup.text.split())
        raw_train_info = re.search(rgx_pattern,
                                   js_text).group(1).replace('"',
                                                             "").split(",")

        assert (len(PARSING_MAP.train_info.value) == len(raw_train_info))

        train_info = dict(zip(PARSING_MAP.train_info.value, raw_train_info))
        trains.append(train_info)

    if not trains:
        raise ValueError("""Trains information is not responsed.
            Probably the parmaters of Crawler.trains_info's passed are not valid.
            Please execute Crawler.trains_info function, again.
            """)

    return trains


def parsing_raw_train_stations(raw_html):
    """선택한 기차가 통과하는 정거장 목록 요청에 대한 응답 결과를 파싱.

    Args:
        raw_html (str): Crawler.train_stations에서 얻은 HTML source.

    Returns:
        list: [{"key": "value", ...}, {...}, ...]
    """

    soup = BeautifulSoup(raw_html, "html.parser")

    tbody_tag = soup.find("tbody")
    tr_tags = tbody_tag.find_all("tr")

    stations = []
    for tr_tag in tr_tags:
        td_tags = tr_tag.find_all("td")

        station_name = td_tags[0].text.strip()
        arrival_time = '00:00' if td_tags[1].text.strip(
        ) == '-' else td_tags[1].text.strip()
        depart_time = '00:00' if td_tags[2].text.strip(
        ) == '-' else td_tags[2].text.strip()
        delay_minutes = '0' if td_tags[3].text.strip(
        ) == '-' else td_tags[3].text.strip()

        raw_route_info = [
            station_name,
            arrival_time,
            depart_time,
            delay_minutes,
        ]

        station_info = dict(zip(PARSING_MAP.station_info.value,
                                raw_route_info))
        stations.append(station_info)

    if not stations:
        raise ValueError("""Stations information is not responsed.
            Probably the parmaters of Crawler.train_stations's passed are not valid.
            Please execute Crawler.trains_info function and pass train_info instance to Crawler.train_stations, again.
            """)

    return stations


def parsing_raw_srcar_length(raw_html):
    """선택한 기차가 이루고 있는 칸 번호 요청에 대한 응답 결과를 파싱.

    Args:
        raw_html (str): Crawler.train_srcar_length 얻은 HTML source.

    Returns:
        list: [1, 2, 3, ...]
    """

    soup = BeautifulSoup(raw_html, "html.parser")

    input_tag = soup.find('input', {'type': 'hidden', 'name': 'arrSrcarNo'})

    srcars = input_tag['value'].split(',')

    if not srcars:
        raise ValueError("""Srcar-Length information is not responsed.
            Probably train_info is not valid.
            Please execute Crawler.trains_info function and pass train_info instance to Crawler.train_srcar_length, again.
            """)

    return srcars


def parsing_raw_seat_by_srcar(raw_html):
    """선택한 기차의 특정 칸에 존재하는 좌석 상태 요청에 대한 응답 결과를 파싱.

    Args:
        raw_html (str): Crawler.train_seat_by_route 얻은 HTML source.

    Returns:
        dict: | {'1A 좌석': 0, '1B 좌석': 1, ...} 
        | 0: 빈자리, 1: 예약좌석
    """

    seat_status = {}

    soup = BeautifulSoup(raw_html, "html.parser")

    div_tag = soup.find('div', {'id': 'seat_box_id'})

    span_tags_on = div_tag.find_all("span", {"class": "ck_seat_td1_on"})
    span_tags_on += div_tag.find_all("span", {"class": "ck_seat_td2_on"})

    span_tags_off = div_tag.find_all("span", {"class": "ck_seat_td1_off"})
    span_tags_off += div_tag.find_all("span", {"class": "ck_seat_td2_off"})

    for span_tag in span_tags_on:
        seat_no = span_tag.text.strip()
        seat_status[seat_no] = 0  # empty seat

    for span_tag in span_tags_off:
        seat_no = span_tag.text.strip()
        seat_status[seat_no] = 1  # full seat

    return seat_status


def parsing_raw_seats_by_schedule(raw_html_dict):
    """선택한 기차, 시간표, 칸 정보에서 좌석 상태를 일괄 요청한 뒤 응답 결과를 dict로 묶은 정보를 일괄 파싱.

    Args:
        raw_html_dict (dict): Crawler.train_seats_by_schedule 얻은 HTML source.

    Returns:
        dict: | { '정거장 A': { '칸 번호 1': { '1A 좌석': 0, '1B 좌석': 1, ..., }, 
        | '칸 번호 2': { ..., } }, 
        | '정거장 B': { ... }, 
        | ... 
        | }
    """

    seats_status = {}

    for station, seats_info in raw_html_dict.items():
        seats_status[station] = {}

        for srcar_no, seat_info in seats_info.items():
            seats_status[station][srcar_no] = parsing_raw_seat_by_srcar(
                seat_info)

    return seats_status
