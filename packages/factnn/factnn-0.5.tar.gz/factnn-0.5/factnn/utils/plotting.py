from sklearn.metrics import roc_auc_score, r2_score, roc_curve
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import numpy as np
from photon_stream import plot as ps_plot
from fact.plotting import camera


def plot_event_distribution(events, feature):
    """
    Plot the distributions of a feature (i.e. Energy, Disp, etc) for a given set of files
    :param events:
    :param feature:
    :return:
    """




def plot_image_representations(event, generated_images=()):
    """
    Plot the default FACT representation, as well as different outputs from generators or preprocessors

    Currently, generated images are assumed to be 2D representations

    :param event:
    :return:
    """

    # Plot default FACT plot

    camera(event.photon_stream.list_of_lists)
    plt.show()

    # Plot generated_image
    for image in generated_images:
        plt.imshow(image)


def plot_event_compare(event, cleaned_event=None):
    """
    Plots some sanity checks of an event, potentially with the same plots for the cleaned event as well
    :param event: PhotonStream Event
    :param cleaned_event: Same PhotonStream Event after image cleaning
    :return:
    """

    # First event plotting hist and image
    hist_photons = event.photon_stream.image_sequence
    plt.hist(np.sum(hist_photons, axis=0), histtype='step')
    if cleaned_event is not None:
        hist_cleaned_photons = cleaned_event.photon_stream.image_sequence
        plt.hist(np.sum(hist_cleaned_photons, axis=0), histtype='step')
    plt.show()

    # Now the event itself
    ps_plot.event(event)
    plt.show()
    ps_plot.event(cleaned_event)

def plot_energy_confusion(prediction, truth, log_xy=True, log_z=True, ax=None):
    ax = ax or plt.gca()

    if log_xy is True:
        truth = np.log10(truth)
        prediction = np.log10(prediction)

    min_label = np.min(truth)
    min_pred = np.min(prediction)
    max_pred = np.max(prediction)
    max_label = np.max(truth)

    if min_label < min_pred:
        min_ax = min_label
    else:
        min_ax = min_pred

    if max_label > max_pred:
        max_ax = max_label
    else:
        max_ax = max_pred

    limits = [
        min_ax,
        max_ax
    ]
    print(limits)
    print("Max, min Label")
    print([min_label, max_label])

    counts, x_edges, y_edges, img = ax.hist2d(
        truth,
        prediction,
        bins=[100, 100],
        range=[limits, limits],
        norm=LogNorm() if log_z is True else None
    )
    ax.set_aspect(1)
    ax.figure.colorbar(img, ax=ax)

    if log_xy is True:
        ax.set_xlabel(r'$\log_{10}(E_{\mathrm{MC}} \,\, / \,\, \mathrm{GeV})$')
        ax.set_ylabel(r'$\log_{10}(E_{\mathrm{Est}} \,\, / \,\, \mathrm{GeV})$')
    else:
        ax.set_xlabel(r'$E_{\mathrm{MC}} \,\, / \,\, \mathrm{GeV}$')
        ax.set_ylabel(r'$E_{\mathrm{Est}} \,\, / \,\, \mathrm{GeV}$')

    return ax


def plot_disp_confusion(prediction, truth, log_xy=True, log_z=True, ax=None):
    ax = ax or plt.gca()

    if log_xy is True:
        truth = np.log10(truth)
        prediction = np.log10(prediction)

    min_label = np.min(truth)
    min_pred = np.min(prediction)
    max_pred = np.max(prediction)
    max_label = np.max(truth)

    if min_label < min_pred:
        min_ax = min_label
    else:
        min_ax = min_pred

    if max_label > max_pred:
        max_ax = max_label
    else:
        max_ax = max_pred

    limits = [
        min_ax,
        max_ax
    ]
    print(limits)
    print("Max, min Label")
    print([min_label, max_label])

    counts, x_edges, y_edges, img = ax.hist2d(
        truth,
        prediction,
        bins=[100, 100],
        range=[limits, limits],
        norm=LogNorm() if log_z is True else None
    )
    ax.set_aspect(1)
    ax.figure.colorbar(img, ax=ax)

    if log_xy is True:
        ax.set_xlabel(r'$log_{10}(Disp_{MC}) (mm)$')
        ax.set_ylabel(r'$log_{10}(Disp_{EST}) (mm)$')
    else:
        ax.set_xlabel(r'$Disp_{MC} (mm)$')
        ax.set_ylabel(r'$Disp_{EST} (mm)$')

    return ax


def plot_roc(truth, predictions, ax=None):
    ax = ax or plt.gca()

    ax.axvline(0, color='lightgray')
    ax.axvline(1, color='lightgray')
    ax.axhline(0, color='lightgray')
    ax.axhline(1, color='lightgray')

    mean_fpr, mean_tpr, _ = roc_curve(truth, predictions)

    ax.set_title('Area Under Curve: {:.4f}'.format(
        roc_auc_score(truth, predictions)
    ))

    ax.plot(mean_fpr, mean_tpr, label='ROC curve')
    ax.legend()
    ax.set_aspect(1)

    ax.set_xlabel('false positive rate')
    ax.set_ylabel('true positive rate')
    ax.figure.tight_layout()

    return ax


def plot_probabilities(performace_df, model=None, ax=None, classnames=('Proton', 'Gamma')):
    ax = ax or plt.gca()

    bin_edges = np.linspace(0, 1, 100 + 2)
    ax.hist(
        performace_df,
        bins=bin_edges, label="Proton", histtype='step',
    )
    if model is not None:
        ax.hist(
            model,
            bins=bin_edges, label="Gamma", histtype='step',
        )

    ax.legend()
    ax.set_xlabel('Gamma confidence'.format(classnames[1]))
    ax.figure.tight_layout()

    return ax
