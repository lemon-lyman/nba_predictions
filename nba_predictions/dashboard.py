import matplotlib.pyplot as plt
import numpy as np
from oddspy.prediction_format import Model


## Show statistics on the current success fo different models
## TODO:
## Success %
## Plot of past success
##      Scatter in background of actual data with moving average on top
##      OR
##      All moving overages overlaid onto one plot

def test_dashboard():
    n = 100
    model_a = Model(np.random.randint(0, 2, size=(n)), np.arange(n), 'FTE')
    model_b = Model(np.random.randint(0, 2, size=(n)), np.arange(n), 'LVI')
    model_c = Model(np.random.randint(0, 2, size=(n)), np.arange(n), 'Nick')
    model_d = Model(np.random.randint(0, 2, size=(n)), np.arange(n), 'Koen')
    model_e = Model(np.random.randint(0, 2, size=(n)), np.arange(n), 'Carlos')

    create_dashboard(model_a, model_b, model_c, model_d, model_e)



def create_dashboard(*args):
    """

    :param args: list of Models()
    :return:
    """

    color_dict = {'FTE': 'b',
                  'LVI': 'r',
                  'Nick': 'orange',
                  'Koen': 'g',
                  'Carlos': 'magenta'}

    plt.style.use('dark_background')
    fig, ax = plt.subplots()

    for model in args:
        ax.plot(model.dates, model.ongoing_average(), color=color_dict[model.label])

    ax.plot([model.dates[0], model.dates[-1]], [.5, .5], c='darkgrey', zorder=-1)
    ax.set_xlim([model.dates[0], model.dates[-1]])
    ax.set_ylim([0, 1])
    ax.legend([model.label for model in args])

    plt.show()

if __name__ == "__main__":
    test_dashboard()
