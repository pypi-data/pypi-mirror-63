import pathlib
import re
import csv
import datetime as dt
from astropy.constants import R_earth
import numpy as np
from . import mrmms_sdc_api as sdc
from cdflib import cdfread, epochs
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

tai_1958 = epochs.CDFepoch.compute_tt2000([1958, 1, 1, 0, 0, 0, 0, 0, 0])

class BurstSegment:
    def __init__(self, tstart, tstop, fom, discussion,
                 sourceid=None, createtime=None):
        '''
        Create an object representing a burst data segment.

        Parameters
        ----------
        fom : int, float
            Figure of merit given to the selection
        tstart : int, str, `datetime.datetime`
            The start time of the burst segment, given as a `datetime` object,
            a TAI time in seconds since 1 Jan. 1958, or as a string formatted
            as `yyyy-MM-dd hh:mm:SS`. Times are converted to `datetimes`.
        tstop : int, str, `datetime.datetime`
            The stop time of the burst segment, similar to `tstart`.
        discussion : str
            Description of the segment provided by the SITL
        sourceid : str
            Username of the SITL that made the selection
        file : str
            Name of the file containing the selection
        '''

        # Convert tstart to datetime
        if isinstance(tstart, str):
            tstart = dt.datetime.strptime(tstart, '%Y-%m-%d %H:%M:%S')
        elif isinstance(tstart, int):
            tstart = self.__class__.tai_to_datetime(tstart)

        # Convert tstop to datetime
        if isinstance(tstop, str):
            tstop = dt.datetime.strptime(tstop, '%Y-%m-%d %H:%M:%S')
        elif isinstance(tstop, int):
            tstop = self.__class__.tai_to_datetime(tstop)

        self.discussion = discussion
        self.createtime = createtime
        self.fom = fom
        self.sourceid = sourceid
        self.tstart = tstart
        self.tstop = tstop

    def __str__(self):
        return ('{0}   {1}   {2:3.0f}   {3}'
                .format(self.tstart, self.tstop, self.fom, self.discussion)
                )

    def __repr__(self):
        return ('selections.BurstSegment({0}, {1}, {2:3.0f}, {3})'
                .format(self.tstart, self.tstop, self.fom, self.discussion)
                )

    @staticmethod
    def datetime_to_list(t):
        return [t.year, t.month, t.day,
                t.hour, t.minute, t.second,
                t.microsecond // 1000, t.microsecond % 1000, 0
                ]

    @classmethod
    def datetime_to_tai(cls, t):
        t_list = cls.datetime_to_list(t)
        return int((epochs.CDFepoch.compute_tt2000(t_list) - tai_1958) // 1e9)

    @classmethod
    def tai_to_datetime(cls, t):
        tepoch  = epochs.CDFepoch()
        return tepoch.to_datetime(t * int(1e9) + tai_1958)

    @property
    def start_time(self):
        return self.tstart.strftime('%Y-%m-%d %H:%M:%S')

    @property
    def stop_time(self):
        return self.tstop.strftime('%Y-%m-%d %H:%M:%S')

    @property
    def taistarttime(self):
        return self.__class__.datetime_to_tai(self.tstart)

    @property
    def taiendtime(self):
        return self.__class__.datetime_to_tai(self.tstop)


def _burst_data_segments_to_burst_segment(data):
    '''
    Turn selections created by `MrMMS_SDC_API.burst_data_segements` and turn
    them into `BurstSegment` instances.
    
    Parameters
    ----------
    data : dict
        Data associated with each burst segment
    
    Returns
    -------
    result : list of `BurstSegment`
        Data converted to `BurstSegment` instances
    '''
    # Look at createtime and finishtime keys to see if either can
    # substitute for a file name time stamp
    result = []
    for tstart, tend, fom, discussion, sourceid, createtime in \
        zip(data['tstart'], data['tstop'], data['fom'],
            data['discussion'], data['sourceid'], data['createtime']
            ):
        result.append(BurstSegment(tstart, tend, fom, discussion,
                                   sourceid=sourceid,
                                   createtime=createtime)
                      )
    return result


def _get_selections(type, start, stop,
                    sort=True, combine=True, unique=True,
                    filter=None):
    '''
    Creator function for burst selections. See `selections`.
    '''
    
    # Get the selections
    data = sdc.burst_selections(type, start, stop)
    
    # Turn the data into BurstSegments. Adjacent segments returned
    # by `sdc.sitl_selections have a 0 second gap between stop and
    # start times. Those returned by `sdc.burst_data_segments` are
    # separated by 10 seconds.
    if type in ('abs-all', 'sitl', 'gls', 'mp-dl-unh'):
        delta_t = 0.0
        converter = _sitl_selections_to_burst_segment
    elif type in ('abs', 'sitl+back'):
        delta_t = 10.0
        converter = _burst_data_segments_to_burst_segment
    else:
        raise ValueError('Invalid selections type {}'.format(type))
    
    # Convert data into BurstSegments
    data = converter(data)
    
    # Curate the data
    if combine:
        combine_segments(data, delta_t=delta_t)
    if sort:
        data = sort_segments(data)
    if unique:
        data = remove_duplicate_segments(data)
    if filter is not None:
        data = filter_segments(data, filter)
    
    return data


def _mission_events_to_burst_segment(data):
    '''
    Turn selections created by `MrMMS_SDC_API.mission_events` and turn
    them into `BurstSegment` instances.
    
    Parameters
    ----------
    data : dict
        Data associated with each burst segment
    
    Returns
    -------
    result : list of `BurstSegment`
        Data converted to `BurstSegment` instances
    '''
    raise NotImplementedError


def _sitl_selections_to_burst_segment(data):
    '''
    Turn selections created by `MrMMS_SDC_API.sitl_selections` and turn
    them into `BurstSegment` instances.
    
    Parameters
    ----------
    data : dict
        Data associated with each burst segment
    
    Returns
    -------
    result : list of `BurstSegment`
        Data converted to `BurstSegment` instances
    '''
    result = []
    for tstart, tend, fom, discussion, sourceid, createtime in \
        zip(data['tstart'], data['tstop'], data['fom'],
            data['discussion'], data['sourceid'], data['createtime']):
        result.append(BurstSegment(tstart, tend, fom, discussion,
                                   sourceid=sourceid,
                                   createtime=createtime)
                      )
    return result


def combine_segments(data, delta_t=0):
    '''
    Combine contiguous burst selections into single selections.

    Parameters
    ----------
    data : list of `BurstSegment`
        Selections to be combined.
    delta_t : int
        Time interval between adjacent selections. For selections
        returned by `pymms.sitl_selections()`, this is 0. For selections
        returned by `pymms.burst_data_segment()`, this is 10.
    '''
    # Any time delta > delta_t sec indicates the end of a contiguous interval
    t_deltas = [(seg1.tstart - seg0.tstop).total_seconds()
                for seg1, seg0 in zip(data[1:], data[:-1])
                ]
    t_deltas.append(1000)
    icontig = 0  # Current contiguous interval
    result = []

    # Check if adjacent elements are continuous in time
    #   - Use itertools.islice to select start index without copying array
    for idx, t_delta in enumerate(t_deltas):
        # Contiguous segments are separated by delta_t seconds
        if t_delta == delta_t:
            # And unique segments have the same fom and discussion
            if (data[icontig].fom == data[idx+1].fom) and \
                    (data[icontig].discussion == data[idx+1].discussion):
                continue

        # End of a contiguous interval
        data[icontig].tstop = data[idx].tstop

        # Next interval
        icontig = icontig + 1

        # Move data for new contiguous segments to beginning of array
        try:
            data[icontig] = data[idx+1]
        except IndexError:
            pass

    # Truncate data beyond last contiguous interval
    del data[icontig:]


def filter_segments(data, filter):
    '''
    Filter burst selections by their discussion string.

    Parameters
    ----------
    data : dict
        Selections to be combined. Must have key 'discussion'.
    '''
    return [seg for seg in data if re.search(filter, seg.discussion)]


def metric(figtype=None):
    starttime = dt.datetime(2019, 10, 17)

    # Find SROI
    #start_date, end_date = gls_get_sroi(starttime)
    start_date = dt.datetime(2019, 10, 19)
    #end_date = start_date + dt.timedelta(days=5)
    end_date = dt.datetime.now()

    # Grab selections
    abs_files = sdc.sitl_selections('abs_selections',
                                    start_date=start_date, end_date=end_date)
    gls_files = sdc.sitl_selections('gls_selections', gls_type='mp-dl-unh',
                                    start_date=start_date, end_date=end_date)

    # Read the files
    abs_data = sdc.read_selections(abs_files)
    sitl_data = sdc.burst_data_segments(start_date, end_date)
    gls_data = sdc.read_selections(gls_files)

    # ABS, SITL, and GLS files/data are often duplicated,
    # out of order, and/or split into smaller chunks. We
    # want to take only unique, aggregate selections.
    abs_data = sort(abs_data)
    abs_data = remove_duplicates(abs_data)
    combine(abs_data)

    sitl_data = sort(sitl_data)
    combine(sitl_data, delta_t=10)
    mp_data = re_filter(sitl_data, '(MP|Magnetopause)')

    gls_data = sort(gls_data)
    gls_data = remove_duplicates(gls_data)
    combine(gls_data)

    # Find overlap between GLS and SITL
    gls_sitl = []
    for segment in gls_data:
        if (segment.tstart <= sitl_data[-1].tstop) & \
                (segment.tstop >= sitl_data[0].tstart):
            gls_sitl.append(selection_overlap(segment, sitl_data))

    # Find overlap between SITL MP Crossings and GLS
    sitl_mp_gls = []
    for segment in mp_data:
        if (segment.tstart <= gls_data[-1].tstop) & \
                (segment.tstop >= gls_data[0].tstart):
            sitl_mp_gls.append(selection_overlap(segment, gls_data))

    # Find overlap between GLS and SITL MP
    gls_sitl_mp = []
    for segment in gls_data:
        if (segment.tstart <= mp_data[-1].tstop) & \
                (segment.tstop >= mp_data[0].tstart):
            gls_sitl_mp.append(selection_overlap(segment, mp_data))

    # Find overlap between ABS and SITL
    abs_sitl = []
    for segment in abs_data:
        if (segment.tstart <= sitl_data[-1].tstop) & \
                (segment.tstop >= sitl_data[0].tstart):
            abs_sitl.append(selection_overlap(segment, sitl_data))

    # Find overlap between SITL MP and ABS
    sitl_mp_abs = []
    for segment in mp_data:
        if (segment.tstart <= abs_data[-1].tstop) & \
                (segment.tstop >= abs_data[0].tstart):
            sitl_mp_abs.append(selection_overlap(segment, abs_data))

    # Find overlap between SITL and ABS
    sitl_abs = []
    for segment in sitl_data:
        if (segment.tstart <= abs_data[-1].tstop) & \
                (segment.tstop >= abs_data[0].tstart):
            sitl_abs.append(selection_overlap(segment, abs_data))

    # Aggregate results
    gls_sitl_selected = sum(selection['n_selections'] > 0 for selection in gls_sitl)
    sitl_mp_gls_selected = sum(selection['n_selections'] > 0 for selection in sitl_mp_gls)
    gls_sitl_mp_selected = sum(selection['n_selections'] > 0 for selection in gls_sitl_mp)
    abs_sitl_selected = sum(selection['n_selections'] > 0 for selection in abs_sitl)
    sitl_mp_abs_selected = sum(selection['n_selections'] > 0 for selection in sitl_mp_abs)
    sitl_abs_selected = sum(selection['n_selections'] > 0 for selection in sitl_abs)

    gls_sitl_pct_selected = gls_sitl_selected / len(gls_sitl) * 100.0
    sitl_mp_gls_pct_selected = sitl_mp_gls_selected / len(sitl_mp_gls) * 100.0
    gls_sitl_mp_pct_selected = gls_sitl_mp_selected / len(gls_sitl_mp) * 100.0
    abs_sitl_pct_selected = abs_sitl_selected / len(abs_sitl) * 100.0
    sitl_mp_abs_pct_selected = sitl_mp_abs_selected / len(sitl_mp_abs) * 100.0
    sitl_abs_pct_selected = sitl_abs_selected / len(sitl_abs) * 100.0

    gls_sitl_pct_overlap = [selection['pct_overlap'] for selection in gls_sitl]
    sitl_mp_gls_pct_overlap = [selection['pct_overlap'] for selection in sitl_mp_gls]
    gls_sitl_mp_pct_overlap = [selection['pct_overlap'] for selection in gls_sitl_mp]
    abs_sitl_pct_overlap = [selection['pct_overlap'] for selection in abs_sitl]
    sitl_mp_abs_pct_overlap = [selection['pct_overlap'] for selection in sitl_mp_abs]
    sitl_abs_pct_overlap = [selection['pct_overlap'] for selection in sitl_abs]

    # Create a figure
    fig = plt.figure(figsize=(8.5,7))
    fig.subplots_adjust(hspace=0.65, wspace=0.4)

    # GLS-SITL selections
    ax = fig.add_subplot(3, 2, 1)
    hh = ax.hist(gls_sitl_pct_overlap, bins=20, range=(0, 100))
    ax.set_xlabel('% Overlap Between GLS and SITL Segment')
    ax.set_ylabel('Occurrence')
    ax.text(0.5, 0.98, '{0:4.1f}% of {1:d}'
              .format(gls_sitl_pct_selected, len(gls_sitl)),
              verticalalignment='top', horizontalalignment='center',
              transform=ax.transAxes)
    ax.set_title('GLS Segments Selected by SITL')

    # SITL MP-GSL selections
    ax = fig.add_subplot(3, 2, 3)
    hh = ax.hist(sitl_mp_gls_pct_overlap, bins=20, range=(0, 100))
    ax.set_xlabel('% Overlap Between SITL and GLS Segment')
    ax.set_ylabel('Occurrence')
    ax.text(0.5, 0.98, '{0:4.1f}% of {1:d}'
              .format(sitl_mp_gls_pct_selected, len(sitl_mp_gls)),
              verticalalignment='top', horizontalalignment='center',
              transform=ax.transAxes)
    ax.set_title('SITL MP Segments Selected by GLS')

    # GLS-SITL MP selections
    ax = fig.add_subplot(3, 2, 5)
    hh = ax.hist(gls_sitl_mp_pct_overlap, bins=20, range=(0, 100))
    ax.set_xlabel('% Overlap Between GLS and SITL Segment')
    ax.set_ylabel('Occurrence')
    ax.text(0.5, 0.98, '{0:4.1f}% of {1:d}'
            .format(gls_sitl_mp_pct_selected, len(gls_sitl_mp)),
            verticalalignment='top', horizontalalignment='center',
            transform=ax.transAxes)
    ax.set_title('GLS Segments Selected by SITL MP')

    # ABS-SITL selections
    ax = fig.add_subplot(3, 2, 2)
    hh = ax.hist(abs_sitl_pct_overlap, bins=20, range=(0, 100))
    ax.set_xlabel('% Overlap Between ABS and SITL Segment')
    ax.set_ylabel('Occurrence')
    ax.text(0.5, 0.98, '{0:4.1f}% of {1:d}'
            .format(abs_sitl_pct_selected, len(abs_sitl)),
            verticalalignment='top', horizontalalignment='center',
            transform=ax.transAxes)
    ax.set_title('ABS Segments Selected by SITL')

    # SITL MP-ABS selections
    ax = fig.add_subplot(3, 2, 4)
    hh = ax.hist(sitl_mp_abs_pct_overlap, bins=20, range=(0, 100))
    ax.set_xlabel('% Overlap Between SITL and ABS Segment')
    ax.set_ylabel('Occurrence')
    ax.text(0.5, 0.98, '{0:4.1f}% of {1:d}'
            .format(sitl_mp_abs_pct_selected, len(sitl_mp_abs)),
            verticalalignment='top', horizontalalignment='center',
            transform=ax.transAxes)
    ax.set_title('SITL MP Segments Selected by ABS')

    # SITL-ABS selections
    ax = fig.add_subplot(3, 2, 6)
    hh = ax.hist(sitl_abs_pct_overlap, bins=20, range=(0, 100))
    ax.set_xlabel('% Overlap Between SITL and ABS Segment')
    ax.set_ylabel('Occurrence')
    ax.text(0.5, 0.98, '{0:4.1f}% of {1:d}'
            .format(sitl_abs_pct_selected, len(sitl_abs)),
            verticalalignment='top', horizontalalignment='center',
            transform=ax.transAxes)
    ax.set_title('SITL Segments Selected by ABS')
    
    # Save the figure
    if figtype is not None:
        filename = (output_dir
                    / '_'.join(('selections_metric',
                                start_date.strftime('%Y%m%d%H%M%S'),
                                end_date.strftime('%Y%m%d%H%M%S')
                                )))
        filename = filename.with_suffix('.' + figtype)
        plt.savefig(filename.expanduser())
    
    plt.show()


def print_selections(data, full=False):
    '''
    Print details of the burst selections.

    Parameters
    ----------
    data : `BurstSegment` or list of `BurstSegment`
        Selections to be printed. Must have keys 'tstart', 'tstop',
        'fom', 'sourceid', and 'discussion'
    '''
    if full:
        source_len = max(len(s.sourceid) for s in data)
        source_len = max(source_len, 8)
        fmt_str = '{0:>19}   {1:>19}   {2:>19}   {3:>5}   ' \
                  '{4:>'+str(source_len)+'}   {5}'
        print(fmt_str.format('TSTART', 'TSTOP', 'CREATETIME', 'FOM',
                             'SOURCEID', 'DISCUSSION')
              )
        for s in data:
            createtime = dt.datetime.strftime(s.createtime,
                                              '%Y-%m-%d %H:%M:%S')
            print(fmt_str.format(s.start_time, s.stop_time, createtime,
                                 s.fom, s.sourceid, s.discussion)
                  )
        return
    
    
    print('{0:>19}   {1:>19}   {2}   {3}'
          .format('TSTART', 'TSTOP', 'FOM', 'DISCUSSION')
          )

    if isinstance(data, list):
        for selection in data:
            print(selection)
    else:
        print(data)


def read_csv(filename, start_time=None, stop_time=None, header=True):
    '''
    Read a CSV file with burst segment selections.
    
    Parameters
    ----------
    filename : str
        The name of the file to which `data` is to be read
    start_time : str or `datetime.datetime`
        Filter results to contain segments selected on or
        after this time. Possible only if `header` is True
        and if a column is named `'start_time'`
    stop_time : str or `datetime.datetime`
        Filter results to contain segments selected on or
        before this time. Possible only if `header` is True
        and if a column is named `'stop_time'`
    header : bool
        If `True`, the csv file has a header indicating the
        names of each column. If `header` is `False`, the
        assumed column names are 'start_time', 'stop_time',
        'fom', 'sourceid', 'discussion', 'createtime'.
    
    Returns
    -------
    data : list of `BurstSegment`
        Burst segments read from the csv file
    '''
    # Convert time itnerval to datetimes if needed
    if isinstance(start_time, str):
        start_time = dt.datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
    if isinstance(stop_time, str):
        stop_time = dt.datetime.strptime(stop_time, '%Y-%m-%d %H:%M:%S')
    
    file = pathlib.Path(filename)
    data = []
            
    # Read the file
    with open(file.expanduser(), 'r', newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        
        # Take column names from file header
        if header:
            keys = next(csvreader)
            
        # Read the rows
        for row in csvreader:
            # Select the data within the time interval
            if start_time is not None:
                tstart = dt.datetime.strptime(row[0],
                                              '%Y-%m-%d %H:%M:%S')
                if tstart < start_time:
                    continue
            if stop_time is not None:
                tstop = dt.datetime.strptime(row[1],
                                             '%Y-%m-%d %H:%M:%S')
                if tstop > stop_time:
                    continue  # BREAK if sorted!!
            
            # Initialize segment with required fields then add
            # additional fields after
            data.append(BurstSegment(row[0], row[1], float(row[2]), row[4],
                                     sourceid=row[3], createtime=row[5]
                                     )
                        )
    
    return data


def remove_duplicate_segments(data):
    '''
    If SITL or GLS selections are submitted multiple times,
    there can be multiple copies of the same selection, or
    altered selections that overlap with what was selected
    previously. Find overlapping segments and select those
    from the most recent file, as indicated by the file name.

    Parameters
    ----------
    data : list of `BurstSegment`
        Selections from which to prude duplicates. Segments
        must be sorted by `tstart`.
    
    Returns
    -------
    results : list of `BurstSegments`
        Unique burst segments.
    '''
    results = data.copy()
    overwrite_times = set()
    for idx, segment in enumerate(data):
        iahead = idx + 1
        
        # Segments should already be sorted. Future segments
        # overlap with current segment if the future segement
        # start time is closer to the current segment start
        # time than is the current segment's end time.
        while ((iahead < len(data)) and 
               ((data[iahead].tstart - segment.tstart) <
                (segment.tstop - segment.tstart))
               ):
            
            # Remove the segment with the earlier create time
            if segment.createtime < data[iahead].createtime:
                remove_segment = segment
                overwrite_time = segment.createtime
            else:
                remove_segment = data[iahead]
                overwrite_time = data[iahead].createtime
            
            # The segment may have already been removed if
            # there are more than one other segments that
            # overlap with it.
            try:
                results.remove(remove_segment)
                overwrite_times.add(overwrite_time)
            except ValueError:
                pass
            
            iahead += 1
    
    # Remove all segments with create times in the overwrite set
    # Note that the model results do not appear to be reproducible
    # so that every time the model is run, a different set of
    # selections are created. Using the filter below, data from
    # whole days can be removed if two processes create overlapping
    # segments at the edges of their time intervals.
#     results = [segment
#                for segment in results
#                if segment.createtime not in overwrite_times
#                ]
    
    print('# Segments Removed: {}'.format(len(data) - len(results)))
    return results


def remove_duplicate_segments_v1(data):
    idx = 0  # current index
    i = idx  # look-ahead index
    noverlap = 0
    result = []
    for idx in range(len(data)):
        if idx < i:
            continue
        print(idx)

        # Reference segment is the current segment
        ref_seg = data[idx]
        t0_ref = ref_seg.taistarttime
        t1_ref = ref_seg.taiendtime
        dt_ref = t1_ref - t0_ref
        
        if idx == len(data) - 2:
            import pdb
            pdb.set_trace()

        try:
            # Test segment are after the reference segment. The
            # test segment overlaps with the reference segment
            # if its start time is closer to the reference start
            # time than is the reference end time. If there is
            # overlap, keep the segment that was created more
            # recently.
            i = idx + 1
            while ((data[i].taistarttime - t0_ref) < dt_ref):
                noverlap += 1
                test_seg = data[i]
                if data[i].createtime > data[idx].createtime:
                    ref_seg = test_seg
                i += 1
        except IndexError:
            pass

        result.append(ref_seg)

    print('# Overlapping Segments: {}'.format(noverlap))
    return result


def selection_overlap(ref, tests):
    out = {'dt': ref.tstop - ref.tstart,
           'dt_next': dt.timedelta(days=7000),
           'n_selections': 0,
           't_overlap': dt.timedelta(seconds=0.0),
           't_overselect': dt.timedelta(seconds=0.0),
           'pct_overlap': 0.0,
           'pct_overselect': 0.0
           }

    # Find which selections overlap with the given entry and by how much
    tdelta = dt.timedelta(days=7000)
    for test in tests:

        if ((test.tstart <= ref.tstop) and
            (test.tstop >= ref.tstart)
            ):
            out['n_selections'] += 1
            out['t_overlap'] += (min(test.tstop, ref.tstop)
                                 - max(test.tstart, ref.tstart)
                                 )

        # Time to nearest interval
        out['dt_next'] = min(out['dt_next'], abs(test.tstart - ref.tstart))

    # Overlap and over-selection statistics
    if out['n_selections'] > 0:
        out['t_overselect'] = out['dt'] - out['t_overlap']
        out['pct_overlap'] = out['t_overlap'] / out['dt'] * 100.0
        out['pct_overselect'] = out['t_overselect'] / out['dt'] * 100.0
    else:
        out['t_overselect'] = out['dt']
        out['pct_overselect'] = 100.0

    return out


def selections(type, start, stop,
               sort=True, combine=True, unique=True,
               filter=None):
    '''
    Factory function for burst data selections.
    
    Parameters
    ----------
    type : str
        Type of burst data selections to retrieve. Options are 'abs',
        'abs-all', 'sitl', 'sitl+back', 'gls', 'mp-dl-unh'.
    start, stop : `datetime.datetime`
        Interval over which to retrieve data
    sort : bool
        Sort burst segments by time. Submissions to the back structure and
        multiple submissions or process executions in one SITL window can
        cause multiples of the same selection or out-of-order selections.
    combine : bool
        Combine adjacent selection into one selection. Due to downlink
        limitations, long time duration burst segments must be broken into
        smaller chunks.
    unique : bool
        Return only unique segments. See `sort`. Also, a SITL may adjust
        the time interval of their selections, so different submissions will
        have duplicates selections but with different time stamps. This is
        accounted for.
    filter : str
        Filter the burst segments by applying the regular expression to
        the segment's discussions string.
    
    Returns
    -------
    results : list of `BurstSegment`
        Each burst segment.
    '''
    return _get_selections(type, start, stop,
                           sort=sort, combine=combine, unique=unique,
                           filter=filter)


def sort_segments(data, createtime=False):
    '''
    Sort abs, sitl, or gls selections into ascending order.

    Parameters
    ----------
    data : list of `BurstSegement`
        Selections to be sorted. Must have keys 'start_time', 'end_time',
        'fom', 'discussion', 'tstart', and 'tstop'.
    createtime: bool
        Sort by time created instead of by selection start time.
    
    Returns
    -------
    results : list of `BurstSegement`
        Inputs sorted by time
    '''
    if createtime:
        return sorted(data, key=lambda x: x.createtime)
    return sorted(data, key=lambda x: x.tstart)


def write_csv(filename, data, append=False):
    '''
    Write a CSV file with burst data segment selections.

    Parameters
    ----------
    filename : str
        The name of the file to which `data` is to be written
    data : list of `BurstSegment`
        Burst segments to be written to the csv file
    append : bool
        If True, `data` will be appended to the end of the file.
    '''
    header = ('start_time', 'stop_time', 'fom', 'sourceid',
              'discussion', 'createtime')
    
    mode = 'w'
    if append:
        mode = 'a'
    
    file = pathlib.Path(filename)
    with open(file.expanduser(), mode, newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        
        if not append:
            csvwriter.writerow(header)
        
        for segment in data:
            csvwriter.writerow([segment.start_time,
                                segment.stop_time,
                                segment.fom,
                                segment.sourceid,
                                segment.discussion,
                                segment.createtime
                                ]
                               )


if __name__ == 'main':
    from heliopy import config
    import pathlib

    # Inputs
    sc = sys.argv[0]
    start_date = sys.argv[1]
    if len(sys.argv) == 3:
        dir = sys.argv[2]
    else:
        dir = pathlib.Path(config['download_dir']) / 'figures' / 'mms'

    start_date = dt.datetime.strptime(start_date, '%Y-%m-%dT%H:%M:%S')

    # Plot the data
    fig = plot_context(sc, start_date, dir=dir)