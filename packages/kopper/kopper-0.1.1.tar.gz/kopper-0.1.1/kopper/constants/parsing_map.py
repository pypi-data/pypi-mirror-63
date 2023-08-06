import enum


class PARSING_MAP(enum.Enum):
    train_info = [
        'txtGoAbrdDt', 'txtGoStartCode', 'txtGoEndCode', 'selGoTrain',
        'selGoRoom', 'txtGoHour', 'txtGoTrnNo', 'useSeatFlg', 'useServiceFlg',
        'selGoSeat', 'selGoSeat1', 'selGoSeat2', 'txtPsgCnt1', 'txtPsgCnt2',
        'selGoService', 'h_trn_seq', 'h_chg_trn_dv_cd', 'h_chg_trn_seq',
        'h_dpt_rs_stn_cd', 'h_dpt_rs_stn_cd_nm', 'h_arv_rs_stn_cd',
        'h_arv_rs_stn_cd_nm', 'h_trn_no', 'h_yms_apl_flg', 'h_trn_clsf_cd',
        'h_trn_gp_cd', 'h_seat_att_cd', 'h_run_dt', 'h_dpt_dt', 'h_dpt_tm',
        'h_arv_dt', 'h_arv_tm', 'h_dlay_hr', 'h_rsv_wait_ps_cnt',
        'h_dtour_flg', 'h_car_tp_cd', 'h_trn_cps_cd1', 'h_trn_cps_cd2',
        'h_trn_cps_cd3', 'h_trn_cps_cd4', 'h_trn_cps_cd5',
        'h_no_ticket_dpt_rs_stn_cd', 'h_no_ticket_arv_rs_stn_cd',
        'h_nonstop_msg', 'h_dpt_stn_cons_ordr', 'h_arv_stn_cons_ordr',
        'h_dpt_stn_run_ordr', 'h_arv_stn_run_ordr', 'h_stnd_rest_seat_cnt',
        'h_free_rest_seat_cnt'
    ]

    station_info = [
        'station_name',
        'arrival_time',
        'depart_time',
        'delay_minutes',
    ]
