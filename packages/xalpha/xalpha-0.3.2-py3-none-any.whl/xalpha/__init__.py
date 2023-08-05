__version__ = "0.3.2"
__author__ = "refraction-ray"
__name__ = "xalpha"

import xalpha.policy
import xalpha.remain
from xalpha.evaluate import evaluate
from xalpha.info import fundinfo, indexinfo, cashinfo, mfundinfo
from xalpha.multiple import mul, mulfix
from xalpha.realtime import rfundinfo, review
from xalpha.record import record
from xalpha.trade import trade
from xalpha.universal import get_daily, get_rt
