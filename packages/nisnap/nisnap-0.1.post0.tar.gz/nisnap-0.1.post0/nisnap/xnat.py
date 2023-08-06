import tempfile
import os

def __is_valid_scan__(xnat_instance, scan) :
    ''' Checks if a scan is valid according to a set of rules '''
    valid = False
    import fnmatch
    prefix = [i.split('/')[0] for i in scan.keys() if fnmatch.fnmatch(i,'*scandata/id')][0]
    if not prefix :
            raise Exception
    if scan['%s/id' % prefix].isdigit() \
            and not scan['%s/id' % prefix].startswith('0') \
            and scan['%s/quality' % prefix] == 'usable' \
            and xnat_instance.select.experiment(scan['ID']).scan(scan['%s/id' % prefix]).datatype() in\
                                        ['xnat:mrScanData',
                                         'xnat:petScanData',
                                         'xnat:ctScanData'] :
        valid = True
    return valid

def download_resources(config, experiment_id, resource_name,  destination,
    raw=True, cache=False):
    """Download a given experiment/resource from an XNAT instance in a local
    destination folder.

    Parameters
    ----------
    config: string
        Configuration file to the XNAT instance.
        See http://xgrg.github.io/first-steps-with-pyxnat/ for more details.

    experiment_id : string
        ID of the experiment from which to download the segmentation maps and
        raw anatomical image.

    resource_name: string
        Name of the resource where the segmentation maps are stored in the XNAT
        instance.

    destination: string
        Destination folder where to store the downloaded resources.

    raw: boolean, optional
        If True, a raw anatomical image will be downloaded along with the
        target resources. If False, only the resources referred to by
        `resource_name` will be downloaded. Default: True

    cache: boolean, optional
        If False, resources will be normally downloaded from XNAT. If True,
        download will be skipped and data will be looked up locally.
        Default: False

    Notes
    -----
    Requires an XNAT instance where SPM segmentation maps will be found
    following a certain data organization in experiment resources named
    `resource_name`.

    See Also
    --------
    xnat.plot_segment : To plot segmentation maps directly providing their
        experiment_id on an XNAT instance
    nisnap.plot_segment : To plot segmentation maps directly providing their
        filepaths

    """
    import os.path as op
    import pyxnat
    x = pyxnat.Interface(config=config)
    filepaths = []
    e = x.select.experiment(experiment_id)

    if 'SPM12' in resource_name:

        if raw:
            fp1 = op.join(destination, '%s_T2_T1space.nii.gz'%experiment_id)
            filepaths.append(fp1)
            if not cache:
                t2_lut_names = ['T2_ALFA1']
                t2_scans = []
                scans = x.array.mrscans(experiment_id=experiment_id,\
                        columns=['xnat:mrScanData/quality',
                                 'xnat:mrScanData/type',
                                 'xsiType']).data
                for s in scans:
                    scan = e.scan(s['xnat:mrscandata/id'])

                    if scan.attrs.get('type') in t2_lut_names and \
                        __is_valid_scan__(x, s):
                            t2_scans.append(scan.id())
                assert(len(t2_lut_names) == 1)

                t2_t1space = list(e.resource('ANTS').files('*%s*T1space.nii.gz'%t2_scans[0]))[0]
                t2_t1space.get(fp1)
        else:
            filepaths.append(None)

        r = e.resource(resource_name)
        for each in ['c1', 'c2', 'c3']:
            c = list(r.files('%s*.nii.gz'%each))[0]
            fp = op.join(destination, '%s_%s_%s.nii.gz'\
                %(experiment_id, resource_name, each))
            if not cache:
                c.get(fp)
            filepaths.append(fp)

    elif 'FREESURFER6' in resource_name:
        r = e.resource(resource_name)

        for each in ['orig.mgz', 'aparc+aseg.mgz']:
            c = list(r.files('*%s'%each))[0]
            fp = op.join(destination, '%s_%s'%(experiment_id, each))
            if not cache:
                c.get(fp)
            filepaths.append(fp)
    return filepaths


def plot_segment(config, experiment_id, savefig=None, cut_coords=None,
    resource_name='SPM12_SEGMENT_T2T1_COREG',
    axes=('A', 'C', 'S'), raw=True, opacity=10, animated=False, figsize=None,
    cache=False):
    """Download a given experiment/resource from an XNAT instance and create
    snapshots of this resource along a selected set of slices.

    Parameters
    ----------
    config: string
        Configuration file to the XNAT instance.

    experiment_id : string
        ID of the experiment from which to download the segmentation maps and
        raw anatomical image.

    savefig: string, optional
        Filepath where the resulting snapshot will be created. If None is given,
        a temporary file will be created and/or the result will be displayed
        inline in a Jupyter Notebook.

    cut_coords: None, or a tuple of floats
        The indexes of the slices that will be rendered. If None is given, the
        slices are selected automatically.

    resource_name: string, optional
        Name of the resource where the segmentation maps are stored in the XNAT
        instance. Default: SPM12_SEGMENT_T2T1_COREG

    axes: string, or a tuple of strings
        Choose the direction of the cuts (among 'A', 'S', 'C', 'AXIAL',
        'SAGITTAL' or 'CORONAL', or lowercase)

    raw: boolean, optional
        If True, the segmentation maps will be plotted over a background image
        (e.g. anatomical T1 or T2, as in xnat.download_resources). If False,
        the segmentation maps will be rendered only. Default: True

    opacity: integer, optional
        The opacity (in %) of the segmentation maps when plotted over a background
        image. Only used if a background image is provided. Default: 10

    animated: boolean, optional
        If True, the snapshot will be rendered as an animated GIF.
        If False, the snapshot will be rendered as a static PNG image. Default:
        False

    figsize: None, or a 2-uple of floats
        Sets the figure size. Default: {'A': (37, 3), 'C': (40, 3), 'S': (18, 3)}

    bg: None or str
        Path to the background image that the masks will be plotted on top of.
        If nothing is specified, the segmentation maps/masks will be plotted only.

    cache: boolean, optional
        If False, resources will be normally downloaded from XNAT. If True,
        download will be skipped and data will be looked up locally.
        Default: False

    Notes
    -----
    Requires an XNAT instance where SPM segmentation maps will be found
    following a certain data organization in experiment resources named
    `resource_name`.

    See Also
    --------
    xnat.download_resources : To download resources (e.g. segmentation maps +
        raw images) from an XNAT instance (e.g. prior to snapshot creation)
    nisnap.plot_segment : To plot segmentation maps directly providing their
        filepaths

    """


    fp = savefig
    if savefig is None:
        if animated:
            f, fp = tempfile.mkstemp(suffix='.gif')
        else:
            f, fp = tempfile.mkstemp(suffix='.png')
        os.close(f)

    dest = tempfile.gettempdir()
    # Downloading resources
    filepaths = download_resources(config, experiment_id, resource_name, dest,
        raw=raw, cache=cache)
    bg = filepaths[0]

    if animated and not raw:
        msg = 'animated cannot be True with raw set to False. Switching raw to True.'
        log.warning(msg)
        raw = True

    from . import spm
    spm.plot_segment(filepaths[1:], axes=axes, bg=bg, opacity=opacity,
        animated=animated, savefig=fp, figsize=figsize, cut_coords=cut_coords)

    if savefig is None:
        # Return image
        from IPython.display import Image
        return Image(filename=fp)
