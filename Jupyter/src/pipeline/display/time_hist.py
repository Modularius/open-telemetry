from typing import List, Dict, Optional, Any
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import numpy as np
from ...es.request_body import RequestBody, convert_es_to_python_dateformat
from ...es.aggs import Filters, DateHistogram, Terms, Min, Max
from ...es.query import Term, Bool
from ..time_hist.messages import PipelineMessageTimeHistograms
from ..time_hist.runs import PipelineRuns
from ..time_hist.digitisers_present import PipelineDigitisersTimeHistograms


### Data Display

def hist_count_results(messages : PipelineMessageTimeHistograms, runs : Optional[PipelineRuns], date_format: str, bin_width: str, height: int = 4):
    expected_num_digitisers = 8

    plt.rcParams["figure.figsize"] = (14,height)
    if runs:
        _, ax = plt.subplots(3,1, layout='constrained')
    else:
        _, ax = plt.subplots(2,1, layout='constrained')

    plt.xticks(rotation=90)
    if runs:
        my_axis = ax[0]
        my_axis.set_ylabel(f"Digitiser Event Lists (Linear) / Run")
        colour = ["b" for _ in runs.run_start]
        my_axis.set_title('Runs')
        my_axis.bar(runs.run_start, runs.run_size, runs.run_duration, edgecolor = "black", color=colour, alpha=0.1)

    datetimes = [dt.strftime(convert_es_to_python_dateformat(date_format)) for dt in messages.time]
    x = np.arange(len(datetimes))
    my_axis = ax[1] if runs else ax[0]
    show_paired_bars(my_axis, "Digitiser and Frame Event Lists", f"Message Count (Linear) / {bin_width}", False, x, messages.num_digitiser_eventlists, "Digitiser Event Lists", messages.num_frames, f"Frames (scaled by {expected_num_digitisers})")
    my_axis.set_xticks([])
    my_axis.set_xlabel("")

    my_axis = ax[2] if runs else ax[1]
    show_paired_bars(my_axis, None, f"Message Count (Log) / {bin_width}", True, x, messages.num_discarded_digitiser_eventlists, "Discarded Digitiser Event Lists", messages.num_incomplete_frames, f"Incomplete Frames (scaled by {expected_num_digitisers})")
    if runs:
        #my_axis.set_xticks(ax[0].get_xticks(), ax[0].get_xticklabels())
        my_axis.set_xticks(x[::2], datetimes[::2])
    else:
        my_axis.set_xticks(x[::2], datetimes[::2])
    my_axis.set_xlabel(f"Date/Time ({date_format})")

    plt.show()

def show_paired_bars(my_axis, title: Optional[str], ylabel: str, log: bool, start, left_data, left_label, right_data, right_label):
    if title:
        my_axis.set_title(title)
    if log:
        my_axis.set_yscale("log")
    my_axis.set_ylabel(ylabel)
    my_axis.bar(start + 0.1, height = left_data, width=0.4, color=(1,0,0), label=left_label)
    my_axis.bar(start + 0.5, height = right_data, width=0.4, color=(0.4,0,0), label=right_label)
    my_axis.legend(loc='upper left', ncols=2)

def show_stacked_bars(my_axis, title: Optional[str], ylabel: str, log: bool, start, data: Dict[int, List[int]]):
    if title:
        my_axis.set_title(title)
    if log:
        my_axis.set_yscale("log")

    my_axis.set_ylabel(ylabel)
    color=[(1,0,0), (0,1,0), (0,0,1), (0.75,0,0.75), (0,0.75,0.75), (0.75,0.75,0.75), (0,0,0), (0.75,0.75,0)]

    num_bars = len(data)
    labels = data.keys()
    for index, label in enumerate(labels):
        my_axis.bar(start + (1 + index)/(num_bars + 2), height = data[label], width=1/(num_bars + 2), color = color[index % len(color)], label=label)
    my_axis.legend(loc='upper left', ncols=num_bars)



def hist_digitisers_count(messages : PipelineDigitisersTimeHistograms, date_format: str, bin_width: str, height: int = 4):
    expected_num_digitisers = 8

    plt.rcParams["figure.figsize"] = (14,height)
    _, ax = plt.subplots(1,1, layout='constrained')
    plt.xticks(rotation=90)
    
    datetimes = [dt.strftime(convert_es_to_python_dateformat(date_format)) for dt in messages.time]
    x = np.arange(len(datetimes))
    show_stacked_bars(ax, "Digitiser and Frame Event Lists", f"Message Count (Linear) / {bin_width}", False, x, messages.digitiser_count)

    ax.set_xticks(x[::2], datetimes[::2])
    ax.set_xlabel(f"Date/Time ({date_format})")

    plt.show()
