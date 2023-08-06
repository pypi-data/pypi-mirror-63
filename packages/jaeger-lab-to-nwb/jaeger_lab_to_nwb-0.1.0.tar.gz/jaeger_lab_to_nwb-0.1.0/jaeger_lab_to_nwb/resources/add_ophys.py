from pynwb.ophys import OpticalChannel
from pynwb.device import Device
from ndx_fret import FRET, FRETSeries
from hdmf.data_utils import DataChunkIterator
from jaeger_lab_to_nwb.resources.create_nwbfile import create_nwbfile

from datetime import datetime
from pathlib import Path
import numpy as np
import struct
import copy
import os


def read_trial_meta(trial_meta):
    """Opens trial_meta file and read line by line."""
    files_raw = []
    addftolist = False
    with open(trial_meta, "r") as f:
        line = f.readline()
        while line:
            if 'acquisition_date' in line:
                acquisition_date = line.replace('acquisition_date', '').replace('=', '').strip()
            if 'sample_time' in line:
                aux = line.replace('sample_time', '').replace('=', '').replace('msec', '').strip()
                sample_time = float(aux) / 1000.
                sample_rate = 1 / sample_time
            if 'page_frames' in line:
                aux = line.replace('page_frames', '').replace('=', '').strip()
                n_frames = int(aux)
            if addftolist:
                files_raw.append(line.strip())
            if 'Data-File-List' in line:
                addftolist = True   # indicates that next lines are file names to be added
            line = f.readline()

    # Separate .rsm file (bitmap of monitor) from .rsd files (raw data)
    file_rsm = files_raw[0]
    files_raw = files_raw[1:]
    return file_rsm, files_raw, acquisition_date, sample_rate, n_frames


def add_ophys_rsd(nwbfile, metadata, dir_cortical_imaging):
    """
    Reads optophysiology raw data from .rsd files and adds it to nwbfile.
    XXXXXXX_A.rsd - Raw data from donor
    XXXXXXX_B.rsd - Raw data from acceptor
    XXXXXXXXX.rsh - Header data
    """
    def data_gen(channel, trial):
        """channel = 'A' or 'B'"""
        # Read trial-specific metadata file .rsh
        trial_meta = os.path.join(dir_cortical_imaging, "VSFP_01A0801-" + trial + "_" + channel + ".rsh")
        file_rsm, files_raw, acquisition_date, sample_rate, n_frames = read_trial_meta(trial_meta=trial_meta)

        # Iterates over all files within the same trial
        for fn, fraw in enumerate(files_raw):
            print('adding channel ' + channel + ', trial: ', trial, ': ', 100 * fn / len(files_raw), '%')
            fpath = os.path.join(dir_cortical_imaging, fraw)

            # Open file as a byte array
            with open(fpath, "rb") as f:
                byte = f.read(1000000000)
            # Data as word array: 'h' signed, 'H' unsigned
            words = np.array(struct.unpack('h' * (len(byte) // 2), byte))

            # Iterates over frames within the same file (n_frames, 100, 100)
            n_frames = int(len(words) / 12800)
            words_reshaped = words.reshape(12800, n_frames, order='F')
            frames = np.zeros((n_frames, 100, 100))
            excess_frames = np.zeros((n_frames, 20, 100))
            for ifr in range(n_frames):
                iframe = -words_reshaped[:, ifr].reshape(128, 100, order='F').astype('int16')
                frames[ifr, :, :] = iframe[20:120, :]
                excess_frames[ifr, :, :] = iframe[0:20, :]

                yield iframe[20:120, :]

            #     # Analog signals are taken from excess data variable
            #     analog_1 = np.squeeze(np.squeeze(excess_frames[:, 12, 0:80:4]).reshape(20*256, 1))
            #     analog_2 = np.squeeze(np.squeeze(excess_frames[:, 14, 0:80:4]).reshape(20*256, 1))
            #     stim_trg = np.squeeze(np.squeeze(excess_frames[:, 8, 0:80:4]).reshape(20*256, 1))

    # Get session_start_time from first header file
    all_files = os.listdir(dir_cortical_imaging)
    all_headers = [f for f in all_files if ('.rsh' in f) and ('_A' not in f) and ('_B' not in f)]
    all_headers.sort()
    _, _, acquisition_date, _, _ = read_trial_meta(trial_meta=Path(dir_cortical_imaging) / all_headers[0])
    session_start_time = datetime.strptime(acquisition_date, '%Y/%m/%d %H:%M:%S')
    print(session_start_time)

    # Get initial metadata
    meta_init = copy.deepcopy(metadata)
    if nwbfile is None:
        meta_init['NWBFile']['session_start_time'] = session_start_time
        nwbfile = create_nwbfile(meta_init)
    else:
        if session_start_time != nwbfile.session_start_time:
            print("Session start time in current nwbfile does not match the start time from rsd files.")
            print("Ophys data conversion aborted.")
            return nwbfile

    # Create and add device
    device = Device(name=metadata['Ophys']['Device'][0]['name'])
    nwbfile.add_device(device)

    # Get FRETSeries metadata
    meta_donor = metadata['Ophys']['FRET'][0]['donor'][0]
    meta_acceptor = metadata['Ophys']['FRET'][0]['acceptor'][0]

    # OpticalChannels
    opt_ch_donor = OpticalChannel(
        name=meta_donor['optical_channel'][0]['name'],
        description=meta_donor['optical_channel'][0]['description'],
        emission_lambda=meta_donor['optical_channel'][0]['emission_lambda']
    )
    opt_ch_acceptor = OpticalChannel(
        name=meta_acceptor['optical_channel'][0]['name'],
        description=meta_acceptor['optical_channel'][0]['description'],
        emission_lambda=meta_acceptor['optical_channel'][0]['emission_lambda']
    )

    # Add trials intervals values only if no trials data exists in nwbfile
    if nwbfile.trials is not None:
        add_trials = False
        print('Trials already exist in current nwb file. Ophys trials intervals not added.')
    else:
        add_trials = True

    # Iterate over trials, creates a FRET group per trial
    trials_numbers = [f.split('-')[1].replace('.rsh', '') for f in all_headers]
    for tr in trials_numbers:
        # Read trial-specific metadata file .rsh
        trial_meta_A = os.path.join(dir_cortical_imaging, "VSFP_01A0801-" + tr + "_A.rsh")
        trial_meta_B = os.path.join(dir_cortical_imaging, "VSFP_01A0801-" + tr + "_B.rsh")
        file_rsm_A, files_raw_A, acquisition_date_A, sample_rate_A, n_frames_A = read_trial_meta(trial_meta=trial_meta_A)
        file_rsm_B, files_raw_B, acquisition_date_B, sample_rate_B, n_frames_B = read_trial_meta(trial_meta=trial_meta_B)

        absolute_start_time = datetime.strptime(acquisition_date_A, '%Y/%m/%d %H:%M:%S')
        relative_start_time = float((absolute_start_time - nwbfile.session_start_time.replace(tzinfo=None)).seconds)

        # Checks if Acceptor and Donor channels have the same basic parameters
        assert acquisition_date_A == acquisition_date_B, \
            "Acquisition date of channels do not match. Trial=" + str(tr)
        assert sample_rate_A == sample_rate_B, \
            "Sample rate of channels do not match. Trial=" + str(tr)
        assert n_frames_A == n_frames_B, \
            "Number of frames of channels do not match. Trial=" + str(tr)
        assert relative_start_time >= 0., \
            "Starting time is negative. Trial=" + str(tr)

        # Create iterator
        data_donor = DataChunkIterator(
            data=data_gen(channel='A', trial=tr),
            iter_axis=0,
            buffer_size=10000,
            maxshape=(None, 100, 100)
        )
        data_acceptor = DataChunkIterator(
            data=data_gen(channel='B', trial=tr),
            iter_axis=0,
            buffer_size=10000,
            maxshape=(None, 100, 100)
        )

        # FRETSeries
        frets_donor = FRETSeries(
            name='donor',
            fluorophore=meta_donor['fluorophore'],
            optical_channel=opt_ch_donor,
            device=device,
            description=meta_donor['description'],
            data=data_donor,
            starting_time=relative_start_time,
            rate=sample_rate_A,
            unit=meta_donor['unit'],
        )
        frets_acceptor = FRETSeries(
            name='acceptor',
            fluorophore=meta_acceptor['fluorophore'],
            optical_channel=opt_ch_acceptor,
            device=device,
            description=meta_acceptor['description'],
            data=data_acceptor,
            starting_time=relative_start_time,
            rate=sample_rate_B,
            unit=meta_acceptor['unit']
        )

        # Adds FRET to acquisition
        meta_fret = metadata['Ophys']['FRET'][0]
        fret = FRET(
            name=meta_fret['name'] + '_' + str(tr),
            excitation_lambda=meta_fret['excitation_lambda'],
            donor=frets_donor,
            acceptor=frets_acceptor
        )
        nwbfile.add_acquisition(fret)

        # Adds trial
        if add_trials:
            tr_stop = relative_start_time + n_frames_A / sample_rate_A
            nwbfile.add_trial(
                start_time=relative_start_time,
                stop_time=tr_stop
            )

    return nwbfile
