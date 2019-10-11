from record import create_record
from ftepy.fte_predictions import create_fte_model
from dashboard import create_dashboard
import datetime
import numpy as np


## Goal: Monitor ongoing performance of odds, FTE, personal models, etc.
## TODO: Create universal format of predictions {prediction, probability/prediction-strength}
if __name__ == "__main__":

    record = create_record()

    ## Create the various Model()s
    ## fte = create fte (record)
    ## LVI = create LVI (record)
    ## Nick = create Nick (record)

    # create_dashboard(FTE, LVI, Nick, Carlos, Koen)


