from queue import Queue
import re


def atoi(text):
    return int(text) if text.isdigit() else text


def natural_keys(text):
    '''
    Reference: https://stackoverflow.com/questions/5967500/how-to-correctly-sort-a-string-with-a-number-inside
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    (See Toothy's implementation in the comments)
    '''
    return [atoi(c) for c in re.split(r'(\d+)', text)]


def make_graph(parsed_seats_info):
    """파싱한 seats_info에서 예약 가능한 좌석 구간을 확인하기 위해 그래프 생성.

    Args:
        parsed_seats_info (dict): helper.parsing_raw_seats_info_by_schedule에서 반환된 파싱 정보.

    Returns:
        list: 2D-list graph

    Notes:
        | Crawler.train_seats_by_schedule에서 행선지 위의 모든 좌석 정보(HTML source)를 얻은 뒤,  
        | helper.parsing_raw_seats_info_by_schedule에서 파싱된 정보를 인자로 사용합니다.

    ..

    +-----------+-------------------+-------------------+-------------------+-------------------+
    |           |      srcar. 1     |      srcar. 2     |      srcar. 3     |      srcar. 4     |
    +-----------+----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+
    | route. 1  | 1A | 1B | 1C | 1D | 1A | 1B | 1C | 1D | 1A | 1B | 1C | 1D | 1A | 1B | 1C | 1D |
    +-----------+----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+
    | route. 2  | 1A | 1B | 1C | 1D | 1A | 1B | 1C | 1D | 1A | 1B | 1C | 1D | 1A | 1B | 1C | 1D |
    +-----------+----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+
    | route. 3  | 1A | 1B | 1C | 1D | 1A | 1B | 1C | 1D | 1A | 1B | 1C | 1D | 1A | 1B | 1C | 1D |
    +-----------+----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+
    | route. 4  | 1A | 1B | 1C | 1D | 1A | 1B | 1C | 1D | 1A | 1B | 1C | 1D | 1A | 1B | 1C | 1D |
    +-----------+----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+

    """
    graph = []

    for _, seats_info in parsed_seats_info.items():
        srcar_nums = list(seats_info.keys())
        srcar_nums.sort(key=natural_keys)

        row = []
        for srcar_no in srcar_nums:
            seats_nums = list(seats_info[srcar_no].keys())
            seats_nums.sort(key=natural_keys)

            for seat_no in seats_nums:
                row.append(seats_info[srcar_no][seat_no])

        graph.append(row)

    return graph


def get_routes_idx(graph, step=2):
    """ | 예약 가능한 좌석 구간의 (출발지, 도착지) index 값 반환.  
    | Schedule 클래스에서 구간 정보를 출력할 때 사용하는 index 값.

    Args:
        graph: make_graph에서 생성한 그래프

    Returns:
        list: | [ (출발지1, 도착지1), (출발지2, 도착지2), ...]  
        | 도착지1과 출발지2는 같은 정거장.
    """

    INF = 987654321

    q = Queue()

    row_size = len(graph)
    col_size = len(graph[0])

    for i in range(col_size):
        if graph[0][i] == 0:
            q.put({'cost': INF, 'station_idx': 0, 'seat_idx': i})
        if graph[-1][i] == 0:
            q.put({'cost': -INF, 'station_idx': row_size - 1, 'seat_idx': i})

    searched_routes = []

    while not q.empty():
        here = q.get()

        if here['cost'] > 0:
            next = ({
                'cost': here['cost'],
                'station_idx': here['station_idx'] + 1,
                'seat_idx': here['seat_idx']
            })
        else:
            next = ({
                'cost': here['cost'],
                'station_idx': here['station_idx'] - 1,
                'seat_idx': here['seat_idx']
            })

        if 0 <= next['station_idx'] < row_size:
            if graph[next['station_idx']][next['seat_idx']] == 0:
                graph[next['station_idx']][next['seat_idx']] = next['cost']
                q.put(next)

            elif graph[here['station_idx']][here['seat_idx']] * graph[
                    next['station_idx']][next['seat_idx']] < -INF:
                searched_routes = {
                    'route1': ({
                        'station_idx': 0,
                        'seat_idx': here['seat_idx']
                    }, {
                        'station_idx': here['station_idx'],
                        'seat_idx': here['seat_idx']
                    }),
                    'route2': ({
                        'station_idx': next['station_idx'],
                        'seat_idx': next['seat_idx']
                    }, {
                        'station_idx': row_size - 1,
                        'seat_idx': next['seat_idx']
                    })
                }
                break

    if len(searched_routes) == 0:
        return searched_routes

    if searched_routes['route1'][1]['seat_idx'] == searched_routes['route2'][
            0]['seat_idx']:
        return [(searched_routes['route1'][0]['station_idx'],
                 searched_routes['route2'][1]['station_idx'])]

    return [(searched_routes['route1'][0]['station_idx'],
             searched_routes['route1'][1]['station_idx']),
            (searched_routes['route2'][0]['station_idx'],
             searched_routes['route2'][1]['station_idx'])]
