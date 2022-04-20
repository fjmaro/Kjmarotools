"""conversion tools"""
import datetime


def datetime2string(date_time: datetime.datetime,
                    sp0="-", sp1=" ", sp2=":") -> str:
    """
    --------------------------------------------------------------------------
    Convert datetime to string in a flexible format configuring sp0/sp1/sp2.
    - YYYY<sp0>MM<sp0>DD<sp1>HH<sp2>MM<sp2>SS
    --------------------------------------------------------------------------
    """
    return date_time.strftime(f"%Y{sp0}%m{sp0}%d{sp1}%H{sp2}%M{sp2}%S")


def string2datetime(date_time: str, sp0="-", sp1=" ", sp2=":"
                    ) -> datetime.datetime:
    """
    --------------------------------------------------------------------------
    Convert string to datetime in a flexible format configuring sp0/sp1/sp2.
    - YYYY<sp0>MM<sp0>DD<sp1>HH<sp2>MM<sp2>SS
    --------------------------------------------------------------------------
    """
    ymd = date_time.split(sp1)[0].split(sp0)
    hms = date_time.split(sp1)[1].split(sp2)
    return datetime.datetime(int(ymd[0]), int(ymd[1]), int(ymd[2]),
                             int(hms[0]), int(hms[1]), int(hms[2]))


def deg2dms_zone(degrees=0.0, zones_pos_neg=("+", "-")) -> tuple:
    """Convert degrees to Deg-min-sec-zone +/- or N/S or X/X"""
    mnt = 60.0 * (degrees - int(degrees))
    seg = 60.0 * (mnt - int(mnt))
    zne = zones_pos_neg[0] if degrees >= 0 else zones_pos_neg[1]
    return abs(int(degrees)), abs(int(mnt)), abs(seg), zne


def dms_zone2deg(dgs=0.0, mns=0.0, scs=0.0, zone_positive=True) -> float:
    """Convert Deg-min-sec-zone (zone=1 or -1)... to deg"""
    deg_out = dgs + mns / 60 + scs / 3600
    return deg_out if zone_positive else -deg_out
