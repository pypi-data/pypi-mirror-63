# -*- coding: utf-8 -*-
import pandas as pd

from .ecg_clean import ecg_clean
from .ecg_peaks import ecg_peaks
from .ecg_rate import ecg_rate


def ecg_process(ecg_signal, sampling_rate=1000, method="neurokit"):
    """Process an ECG signal.

    Convenience function that automatically processes an ECG signal.

    Parameters
    ----------
    ecg_signal : list, array or Series
        The raw ECG channel.
    sampling_rate : int
        The sampling frequency of `ecg_signal` (in Hz, i.e., samples/second).
        Defaults to 1000.
    method : str
        The processing pipeline to apply. Defaults to "neurokit".

    Returns
    -------
    signals : DataFrame
        A DataFrame of the same length as the `ecg_signal` containing the
        following columns:
        - *"ECG_Raw"*: the raw signal.
        - *"ECG_Clean"*: the cleaned signal.
        - *"ECG_R_Peaks"*: the R-peaks marked as "1" in a list of zeros.
        - *"ECG_Rate"*: heart rate interpolated between R-peaks.
    info : dict
        A dictionary containing the samples at which the R-peaks occur,
        accessible with the key "ECG_Peaks".

    See Also
    --------
    ecg_clean, ecg_findpeaks, ecg_fixpeaks, ecg_rate, ecg_plot

    Examples
    --------
    >>> import neurokit2 as nk
    >>>
    >>> ecg = nk.ecg_simulate(duration=15, sampling_rate=1000, heart_rate=80)
    >>> signals, info = nk.ecg_process(ecg, sampling_rate=1000)
    >>> nk.ecg_plot(signals)
    """
    ecg_cleaned = ecg_clean(ecg_signal,
                            sampling_rate=sampling_rate,
                            method=method)

    instant_peaks, rpeaks, = ecg_peaks(ecg_cleaned=ecg_cleaned,
                                       sampling_rate=sampling_rate,
                                       method=method,
                                       correct_artifacts=True)
    rate = ecg_rate(rpeaks,
                    sampling_rate=sampling_rate,
                    desired_length=len(ecg_cleaned))

    signals = pd.DataFrame({"ECG_Raw": ecg_signal,
                            "ECG_Clean": ecg_cleaned,
                            "ECG_Rate": rate})
    signals = pd.concat([signals, instant_peaks], axis=1)
    info = rpeaks
    return signals, info
