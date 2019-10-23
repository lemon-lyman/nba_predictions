from record import create_record
from dashboard import create_dashboard
import models
import datetime
import numpy as np


## Goal: Monitor ongoing performance of odds, FTE, personal models, etc.
## TODO: Create universal format of predictions {prediction, probability/prediction-strength}
if __name__ == "__main__":

    po = False

    record = create_record(pull_override=po)

    carmelo = models.create_carmelo_model(record, pull_override=po)
    carm_elo = models.create_carm_elo_model(record, pull_override=po)
    elo = models.create_elo_model(record, pull_override=po)

    create_dashboard(nick,
                     carmelo,
                     carm_elo,
                     elo)
