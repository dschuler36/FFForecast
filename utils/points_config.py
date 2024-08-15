class PointsConfig:
    def __init__(self, pp_qb_yd, pp_qb_td, pp_rec, pp_rec_yd, pp_rec_td, pp_rush_yd, pp_rush_td, pp_fumble, pp_int,
                 qb_yd_bonus_thresh, pp_qb_yd_bonus, rec_bonus_thresh, pp_rec_bonus, rush_bonus_thresh, pp_rush_bonus,
                 pp_rushing_2pt_conversions, pp_receiving_2pt_conversions, pp_passing_2pt_conversions):
        self.pp_qb_yd = pp_qb_yd
        self.pp_qb_td = pp_qb_td
        self.pp_rec = pp_rec
        self.pp_rec_yd = pp_rec_yd
        self.pp_rec_td = pp_rec_td
        self.pp_rush_yd = pp_rush_yd
        self.pp_rush_td = pp_rush_td
        self.pp_fumble = pp_fumble
        self.pp_int = pp_int
        self.qb_yd_bonus_thresh = qb_yd_bonus_thresh
        self.pp_qb_yd_bonus = pp_qb_yd_bonus
        self.rec_bonus_thresh = rec_bonus_thresh
        self.pp_rec_bonus = pp_rec_bonus
        self.rush_bonus_thresh = rush_bonus_thresh
        self.pp_rush_bonus = pp_rush_bonus
        self.pp_rushing_2pt_conversions = pp_rushing_2pt_conversions
        self.pp_receiving_2pt_conversions = pp_receiving_2pt_conversions
        self.pp_passing_2pt_conversions = pp_passing_2pt_conversions


STANDARD_PPR = PointsConfig(
    pp_qb_yd=0.01,
    pp_qb_td=4,
    pp_rec=1,
    pp_rec_yd=0.1,
    pp_rec_td=6,
    pp_rush_yd=0.1,
    pp_rush_td=6,
    pp_fumble=-2,
    pp_int=-2,
    qb_yd_bonus_thresh=None,
    pp_qb_yd_bonus=None,
    rec_bonus_thresh=None,
    pp_rec_bonus=None,
    rush_bonus_thresh=None,
    pp_rush_bonus=None,
    pp_rushing_2pt_conversions=2,
    pp_receiving_2pt_conversions=2,
    pp_passing_2pt_conversions=2
)

STANDARD_HALF_PPR = PointsConfig(
    pp_qb_yd=0.01,
    pp_qb_td=4,
    pp_rec=0.5,
    pp_rec_yd=0.1,
    pp_rec_td=6,
    pp_rush_yd=0.1,
    pp_rush_td=6,
    pp_fumble=-2,
    pp_int=-2,
    qb_yd_bonus_thresh=None,
    pp_qb_yd_bonus=None,
    rec_bonus_thresh=None,
    pp_rec_bonus=None,
    rush_bonus_thresh=None,
    pp_rush_bonus=None,
    pp_rushing_2pt_conversions=2,
    pp_receiving_2pt_conversions=2,
    pp_passing_2pt_conversions=2
)
