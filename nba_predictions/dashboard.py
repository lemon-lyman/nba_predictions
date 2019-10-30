import matplotlib.pyplot as plt
from matplotlib.dates import date2num
import datetime
import numpy as np

from models import Model


## Show statistics on the current success fo different models
## TODO:
## Success %
## Plot of past success
##      Scatter in background of actual data with moving average on top
##      OR
##      All moving overages overlaid onto one plot

def test_dashboard():

    month = '10'
    year = '2019'
    dates = []
    [[dates.append(month + '/' + str(day) + '/' + year) for _ in range(5)] for day in range(20, 27)]

    n = len(dates)
    model_a = Model(np.random.randint(0, 2, size=(n)), dates, 'CARMELO')
    model_b = Model(np.random.randint(0, 2, size=(n)), dates, 'CARM_ELO')
    model_c = Model(np.random.randint(0, 2, size=(n)), dates, 'Nick')
    model_d = Model(np.random.randint(0, 2, size=(n)), dates, 'Koen')
    model_e = Model(np.random.randint(0, 2, size=(n)), dates, 'Carlos')

    create_dashboard(model_a, model_b, model_c, model_d, model_e)


def create_ticks(dates, every=True):
    """

    :param dates: MM/DD/YYYY
    :return: tick_locations (datenum object), tick_labels
    """
    if every:
        ticks = format_dates(dates)
        tick_labels = [d.split('-')[1] + "/" + d.split('-')[2] for d in dates]
    else:
        datenums = format_dates(dates)
        first_date = datenums[0]
        last_date = datenums[-1]

        ticks = [first_date]

        while ticks[-1] < last_date:
            ticks.append(ticks[-1]+7)

        tick_labels_dt = [datetime.datetime.fromordinal(int(tick)) for tick in ticks]

        tick_labels = [tick.strftime('%m/%d') for tick in tick_labels_dt]

    return ticks, tick_labels

def format_dates(dates):

    datenums = []

    # for d in dates:
    #     d_split = d.split('/')
    #     dt = datetime.date(int(d_split[-1]),
    #                        int(d_split[0]),
    #                        int(d_split[1]))
    #     datenums.append(date2num(dt))

    for d in dates:
        d_split = d.split('-')
        dt = datetime.date(int(d_split[0]),
                           int(d_split[1]),
                           int(d_split[2]))
        datenums.append(date2num(dt))

    return datenums

def create_dashboard(*args):
    """

    :param args: Model(), Model(), Model()...
    :return:
    """

    sec_in_week = ()

    color_dict = {'RAPTOR': 'goldenrod',
                  'CARM-ELO': 'sandybrown',
                  'ELO': 'cornflowerblue',
                  'LVI': 'r',
                  'Nick': 'cyan',
                  'Koen': 'g',
                  'Carlos': 'magenta'}

    plt.style.use('dark_background')
    fig, ax = plt.subplots()
    print()

    for model in args:
        ax.plot(format_dates(model.consolidated_dates),
                model.consolidated_predictions,
                color=color_dict[model.label],
                linewidth=2)

        if model.label == "RAPTOR":
            ax.set_title(str(len(model.prediction_history)) + " Games")

        print(model.label + ": {:.3f} ".format(model.accuracy*100))

    ax.plot([format_dates([model.dates[0]]),
             format_dates([model.dates[-1]])], [.5, .5], c='darkgrey', ls='--', zorder=-1, alpha=.5)

    xticks, xtick_labels = create_ticks(model.dates)

    ax.set_xticks(xticks)
    ax.set_xticklabels(xtick_labels, rotation=45)

    ## TODO: Watchout - assumes dates attribute of models is all the same
    ax.set_xlim([format_dates([model.dates[0]])[0],
                 format_dates([model.dates[-1]])[0]])
    ax.set_ylim([.5, 1])
    ax.legend(["{:.1f}% ".format(model.accuracy*100) + model.label for model in args])
    ax.yaxis.grid(alpha=.2)
    fig.set_size_inches(9, 5)


    plt.show()

if __name__ == "__main__":
    test_dashboard()
