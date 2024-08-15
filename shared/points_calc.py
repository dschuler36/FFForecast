from shared.points_config import PointsConfig


def calculate_fantasy_points(pc: PointsConfig, qb_yd, qb_td, int, rec, rec_yd, rec_td, rush_yd, rush_td, fumble,
                            rushing_2pt_conversions, receiving_2pt_conversions, passing_2pt_conversions):
    qb_yd_bonus_pts = pc.pp_qb_yd_bonus if pc.qb_yd_bonus_thresh is not None and qb_yd >= pc.qb_yd_bonus_thresh else 0
    qb_yd_pts = qb_yd * pc.pp_qb_yd
    qb_td_pts = qb_td * pc.pp_qb_td
    int_pts = int * pc.pp_int
    rec_pts = rec * pc.pp_rec
    rec_yd_bonus_pts = pc.pp_rec_bonus if pc.rec_bonus_thresh is not None and rec_yd >= pc.rec_bonus_thresh else 0
    rec_yd_pts = rec_yd * pc.pp_rec_yd
    rec_td_pts = rec_td * pc.pp_rec_td
    rush_yd_bonus_pts = pc.pp_rush_bonus if pc.rush_bonus_thresh is not None and rush_yd >= pc.rush_bonus_thresh else 0
    rush_yd_pts = rush_yd * pc.pp_rush_yd
    rush_td_pts = rush_td * pc.pp_rush_td
    fumble_pts = fumble * pc.pp_fumble
    rushing_2pt_conversion_pts = rushing_2pt_conversions * pc.pp_rushing_2pt_conversions
    receiving_2pt_converstion_pts = receiving_2pt_conversions * pc.pp_receiving_2pt_conversions
    passing_2pt_conversion_pts = passing_2pt_conversions * pc.pp_passing_2pt_conversions
    return (qb_yd_bonus_pts + qb_yd_pts + qb_td_pts + int_pts + rec_pts + rec_yd_bonus_pts + rec_yd_pts + rec_td_pts +
            rush_yd_bonus_pts + rush_yd_pts + rush_td_pts + fumble_pts + rushing_2pt_conversion_pts +
            receiving_2pt_converstion_pts + passing_2pt_conversion_pts)