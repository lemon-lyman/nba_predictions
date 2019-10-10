import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def foo(*args):
    for idx, x in enumerate(args):
        print(idx)