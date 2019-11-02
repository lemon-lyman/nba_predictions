from record import create_record
from dashboard import create_dashboard
import models
import datetime
import numpy as np
import sys


## Goal: Monitor ongoing performance of odds, FTE, personal models, etc.

if __name__ == "__main__":

    po = None
    if len(sys.argv) > 1:
        if "po" in sys.argv:
            po = True

    record = create_record(pull_override=po)

    nick = models.create_user_model(record, "Nick")
    carlos = models.create_user_model(record, "Carlos")
    koen = models.create_user_model(record, "Koen")

    raptor = models.create_raptor_model(record, pull_override=po)
    elo = models.create_elo_model(record, pull_override=po)
    lvi = models.create_lvi_model(record)

    create_dashboard(nick,
                     carlos,
                     koen,
                     raptor,
                     elo,
                     lvi)
