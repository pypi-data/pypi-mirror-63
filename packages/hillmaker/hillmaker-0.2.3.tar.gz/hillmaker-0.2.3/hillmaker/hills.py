"""Hillmaker"""

# Copyright 2015 Mark Isken
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pandas as pd
import os

from hillmaker.bydatetime import make_bydatetime
from hillmaker.summarize import summarize
from hillmaker.hmlib import HillTimer


def make_hills(scenario_name, stops_df, infield, outfield,
               start_analysis, end_analysis,
               catfield=None,
               bin_size_minutes=60,
               percentiles=(0.25, 0.5, 0.75, 0.95, 0.99),
               cat_to_exclude=None,
               occ_weight_field=None,
               totals=1,
               nonstationary_stats=True,
               stationary_stats=True,
               export_bydatetime_csv=True,
               export_summaries_csv=True,
               export_path='.',
               edge_bins=1,
               verbose=0):

    """
    Compute occupancy, arrival, and departure statistics by time bin of day and day of week.

    Main function that first calls `bydatetime.make_bydatetime` to calculate occupancy, arrival
    and departure values by date by time bin and then calls `summarize.summarize`
    to compute the summary statistics.

    Parameters
    ----------

    scenario_name : string
        Used in output filenames
    stops_df : DataFrame
        Base data containing one row per visit
    infield : string
        Column name corresponding to the arrival times
    outfield : string
        Column name corresponding to the departure times
    start_analysis : datetime-like, str
        Starting datetime for the analysis (must be convertible to pandas Timestamp)
    end_analysis : datetime-like, str
        Ending datetime for the analysis (must be convertible to pandas Timestamp)
    catfield : string or List of strings, optional
        Column name(s) corresponding to the categories. If none is specified, then
        only overall occupancy is analyzed.
        Default is None
    bin_size_minutes : int, optional
        Number of minutes in each time bin of the day, default is 60
    percentiles : list or tuple of floats (e.g. [0.5, 0.75, 0.95]), optional
        Which percentiles to compute. Default is (0.25, 0.5, 0.75, 0.95, 0.99)
    cat_to_exclude : list, optional
        Categories to ignore, default is None
    occ_weight_field : string, optional
        Column name corresponding to the weights to use for occupancy incrementing.
    edge_bins: int, default 1
        Occupancy contribution method for arrival and departure bins. 1=fractional, 2=whole bin
    totals: int, default 1
        0=no totals, 1=totals by datetime, 2=totals bydatetime as well as totals for each field in the
        catfields (only relevant for > 1 category field)
    nonstationary_stats : bool, optional
       If True, datetime bin stats are computed. Else, they aren't computed. Default is True
    stationary_stats : bool, optional
       If True, overall, non time bin dependent, stats are computed. Else, they aren't computed. Default is True
    export_bydatetime_csv : bool, optional
       If True, bydatetime DataFrames are exported to csv files. Default is True.
    export_summaries_csv : bool, optional
       If True, summary DataFrames are exported to csv files. Default is True.
    export_path : string, optional
        Destination path for exported csv files, default is current directory
    verbose : int, optional
        The verbosity level. The default, zero, means silent mode. Higher numbers mean more output messages.

    Returns
    -------
    dict of DataFrames
       The bydatetime DataFrames and all summary DataFrames.
    """
    # Create the bydatetime DataFrame
    with HillTimer() as t:
        starttime = t.start
        bydt_dfs = make_bydatetime(stops_df,
                                   infield,
                                   outfield,
                                   start_analysis,
                                   end_analysis,
                                   catfield,
                                   bin_size_minutes,
                                   cat_to_exclude=cat_to_exclude,
                                   occ_weight_field=occ_weight_field,
                                   edge_bins=edge_bins,
                                   totals=totals,
                                   verbose=verbose)

    if verbose:
        print("Datetime DataFrame created (seconds): {:.4f}".format(t.interval))

    # Create the summary stats DataFrames
    summary_dfs = {}
    if nonstationary_stats or stationary_stats:
        with HillTimer() as t:

            summary_dfs = summarize(bydt_dfs,
                                    nonstationary_stats=nonstationary_stats,
                                    stationary_stats=stationary_stats,
                                    percentiles=percentiles,
                                    totals=totals,
                                    verbose=verbose)

        if verbose:
            print("Summaries by datetime created (seconds): {:.4f}".format(t.interval))

    # Export results to csv if requested
    if export_bydatetime_csv:
        with HillTimer() as t:

            export_bydatetimes(bydt_dfs, scenario_name, export_path)

        if verbose:
            print("By datetime exported to csv (seconds): {:.4f}".format(t.interval))

    if export_summaries_csv:
        with HillTimer() as t:

            if nonstationary_stats:
                export_summaries(summary_dfs, scenario_name, export_path, 'nonstationary')

            if stationary_stats:
                export_summaries(summary_dfs, scenario_name, export_path, 'stationary')

        if verbose:
            print("Summaries exported to csv (seconds): {:.4f}".format(t.interval))

    # All done

    hills = {'bydatetime': bydt_dfs, 'summaries': summary_dfs}

    endtime = t.end

    if verbose:
        print("Total time (seconds): {:.4f}".format(endtime - starttime))

    return hills


def export_bydatetimes(bydt_dfs, scenario_name, export_path):

    """
    Export bydatetime DataFrames to csv files.


    Parameters
    ----------
    bydt_dfs: dict of DataFrames
        Output from make_hills to be exported

    scenario_name: string
        Used in output filenames

    export_path: string
        Destination path for exported csv files
    """

    for d in bydt_dfs:
        file_bydt_csv = scenario_name + '_bydatetime_' + d + '.csv'
        csv_wpath = os.path.normpath(os.path.join(export_path, file_bydt_csv))

        dt_cols = ['arrivals', 'departures', 'occupancy',
                   'day_of_week', 'dow_name', 'bin_of_day', 'bin_of_week']
        bydt_dfs[d].to_csv(csv_wpath, index=True, float_format='%.6f', columns=dt_cols)


def export_summaries(summary_all_dfs, scenario_name, export_path, temporal_key):

    """
    Export occupancy, arrival, and departure summary DataFrames to csv files.


    Parameters
    ----------
    summary_all_dfs: dict of DataFrames
        Output from make_hills to be exported

    scenario_name: string
        Used in output filenames

    export_path: string
        Destination path for exported csv files

    temporal_key: string
        'nonstationary' or 'stationary'

    """

    summary_dfs = summary_all_dfs[temporal_key]
    for d in summary_dfs:
        dfdict = summary_dfs[d]
        for metric in ['occupancy', 'arrivals', 'departures']:

            df = dfdict[metric]
            file_summary_csv = scenario_name + '_' + metric
            if len(d) > 0:
                file_summary_csv = file_summary_csv + '_' + d + '.csv'
            else:
                file_summary_csv = file_summary_csv + '.csv'

            csv_wpath = os.path.normpath(os.path.join(export_path, file_summary_csv))

            catfield = df.index.names

            if temporal_key == 'nonstationary' or catfield[0] is not None:
                df.to_csv(csv_wpath, index=True, float_format='%.6f')
            else:
                df.to_csv(csv_wpath, index=False, float_format='%.6f')


if __name__ == '__main__':

    pass
