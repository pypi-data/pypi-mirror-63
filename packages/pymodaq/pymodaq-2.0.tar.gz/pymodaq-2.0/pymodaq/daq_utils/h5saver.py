
from PyQt5 import QtWidgets
from PyQt5.QtCore import QDateTime, QTime, QDate, QObject, pyqtSignal
from pyqtgraph.parametertree import Parameter, ParameterTree
import pymodaq.daq_utils.custom_parameter_tree as custom_tree
from pymodaq.daq_utils.h5browser import H5Browser
from pymodaq.daq_utils import daq_utils as utils
from pymodaq.version import get_version
import datetime
from dateutil import parser
import os
import tables
import numpy as np
from pathlib import Path
import copy

version = '0.0.1'
save_types = ['scan', 'detector', 'logger', 'custom']
group_types = ['raw_datas', 'scan', 'detector', 'move', 'data', 'ch', '', 'external_h5']
group_data_types = ['data0D', 'data1D', 'data2D', 'dataND']
data_types = ['data', 'axis', 'live_scan', 'navigation_axis', 'external_h5', 'strings']
data_dimensions = ['0D', '1D', '2D', 'ND']
scan_types = ['', 'scan1D', 'scan2D']


class H5Saver(QObject):
    """QObject containing all methods in order to save datas in a *hdf5 file* with a hierachy compatible with
    the H5Browser. The saving parameters are contained within a **Parameter** object: self.settings that can be displayed
    on a UI (see :numref:`other_settings`) using the widget self.settings_tree. At the creation of a new file, a node
    group named **Raw_datas** and represented by the attribute ``raw_group`` is created and set with a metadata attribute:

    * 'type' given by the **save_type** class parameter

    The root group of the file is then set with a few metadata:

    * 'pymodaq_version' the current pymodaq version, e.g. 1.6.2
    * 'file' the file name
    * 'date' the current date
    * 'time' the current time

    All datas will then be saved under this node in various groups

    See Also
    --------
    H5Browser

    Parameters
    ----------
    h5_file: pytables hdf5 file
             object used to save all datas and metadas

    h5_file_path: str or Path
                  pyqtSignal signal represented by a float. Is emitted each time the hardware reached the target
                  position within the epsilon precision (see comon_parameters variable)

    save_type: str
               an element of the list module attribute save_types = ['scan', 'detector', 'custom']
               * 'scan' is used for DAQ_Scan module and should be used for similar application
               * 'detector' is used for DAQ_Viewer module and should be used for similar application
               * 'custom' should be used for customized applications

    Attributes
    ----------
    status_sig: pyqtSignal
                emits a signal of type Threadcommand in order to senf log information to a main UI
    new_file_sig: pyqtSignal
                  emits a boolean signal to let the program know when the user pressed the new file button on the UI

    settings: Parameter
               Parameter instance (pyqtgraph) containing all settings (could be represented using the settings_tree widget)

    settings_tree: ParameterTree
                   Widget representing as a Tree structure, all the settings defined in the class preamble variable ``params``

    """
    status_sig = pyqtSignal(utils.ThreadCommand)
    new_file_sig = pyqtSignal(bool)

    params = [  {'title': 'Save type:', 'name': 'save_type', 'type': 'list', 'values': save_types, 'readonly': True},
                {'title': 'Save 2D datas and above:', 'name': 'save_2D', 'type': 'bool', 'value': True},
                {'title': 'Save raw datas only:', 'name': 'save_raw_only', 'type': 'bool', 'value': True, 'tooltip':
                        'if True, will not save extracted ROIs used to do live plotting, only raw datas and the scan \
                        result will be saved'},
                {'title': 'Do Save:', 'name': 'do_save', 'type': 'bool', 'default': False, 'value': False},
                {'title': 'N saved:', 'name': 'N_saved', 'type': 'int', 'default': 0, 'value': 0, 'visible': False},
                {'title': 'custom_name?:', 'name': 'custom_name', 'type': 'bool', 'default': False, 'value': False},
                {'title': 'show file content?:', 'name': 'show_file', 'type': 'bool', 'default': False, 'value': False},
                {'title': 'Base path:', 'name': 'base_path', 'type': 'browsepath', 'value': 'C:\Data', 'filetype': False, 'readonly': True,},
                {'title': 'Base name:', 'name': 'base_name', 'type': 'str', 'value': 'Scan', 'readonly': True},
                {'title': 'Current scan:', 'name': 'current_scan_name', 'type': 'str', 'value': '', 'readonly': True},
                {'title': 'Current path:', 'name': 'current_scan_path', 'type': 'text', 'value': 'C:\Data',
                 'readonly': True, 'visible': False},
                {'title': 'h5file:', 'name': 'current_h5_file', 'type': 'text_pb', 'value': '', 'readonly': True},
                {'title': 'Compression options:', 'name': 'compression_options', 'type': 'group', 'children': [
                    {'title': 'Compression library:', 'name': 'h5comp_library', 'type': 'list', 'value': 'zlib',
                     'values': ['zlib', 'lzo', 'bzip2', 'blosc']},
                    {'title': 'Compression level:', 'name': 'h5comp_level', 'type': 'int', 'value': 5, 'min': 0, 'max': 9},
                ]},
                ]

    def __init__(self, h5_file_path=None, h5_file=None, save_type='scan'):
        """Initialize the H5Saver object

        Creates the ``setting`` and ``settings_tree`` object



        """
        super().__init__()

        if save_type not in save_types:
            raise Exception('Invalid saving type')

        self.h5_file = h5_file
        self.h5_file_path = h5_file_path
        self.h5_file_name = None
        self.logger_array = None
        self.file_loaded = False

        self.current_group = None
        self.current_scan_group = None
        self.current_scan_name = None
        self.raw_group = None

        self.settings=Parameter.create(title='Saving settings', name='save_settings', type='group', children=self.params)
        self.settings_tree = ParameterTree()
        self.settings_tree.setMinimumHeight(310)
        self.settings_tree.setParameters(self.settings, showTop=False)
        self.settings.child(('current_h5_file')).sigActivated.connect(lambda: self.emit_new_file(True))

        self.settings.child(('save_type')).setValue(save_type)

        self.filters = tables.Filters(
            complevel=self.settings.child('compression_options', 'h5comp_level').value(),
            complib=self.settings.child('compression_options', 'h5comp_library').value())
        # self.settings.child('saving_options', 'save_independent').show(save_type == 'scan')
        # self.settings.child('saving_options', 'do_save').show(not save_type == 'scan')
        # self.settings.child('saving_options', 'current_scan_name').show(save_type == 'scan')


        self.settings.sigTreeStateChanged.connect(self.parameter_tree_changed)  # any changes on the settings will update accordingly the detector

    def flush(self):
        self.h5_file.flush()

    def emit_new_file(self, status):
        """Emits the new_file_sig

        Parameters
        ----------
        status: bool
                emits True if a new file has been asked by the user pressing the new file button on the UI
        """
        self.new_file_sig.emit(status)

    def init_file(self, update_h5=False, custom_naming=False, addhoc_file_path=None, metadata=dict([])):
        """Initializes a new h5 file.
        Could set the h5_file attributes as:

        * a file with a name following a template if ``custom_naming`` is ``False`` and ``addhoc_file_path`` is ``None``
        * a file within a name set using a file dialog popup if ``custom_naming`` is ``True``
        * a file with a custom name if ``addhoc_file_path`` is a ``Path`` object or a path string

        Parameters
        ----------
        update_h5: bool
                   create a new h5 file with name specified by other parameters
                   if false try to open an existing file and will append new data to it
        custom_naming: bool
                       if True, a selection file dialog opens to set a new file name
        addhoc_file_path: Path or str
                          supplied name by the user for the new file
        metadata: dict
                    dictionnary with pair of key, value that should be saved as attributes of the root group
        Returns
        -------
        update_h5: bool
                   True if new file has been created, False otherwise
        """
        datetime_now = datetime.datetime.now()

        if addhoc_file_path is None:
            if not os.path.isdir(self.settings.child(('base_path')).value()):
                os.mkdir(self.settings.child(('base_path')).value())

            # set the filename and path
            base_name = self.settings.child(('base_name')).value()

            if not custom_naming:
                custom_naming = self.settings.child(('custom_name')).value()

            if not custom_naming:
                scan_type = self.settings.child(('save_type')).value() == 'scan'
                scan_path, current_scan_name, save_path = self.update_file_paths(update_h5)
                self.current_scan_name = current_scan_name
                self.settings.child(('current_scan_name')).setValue(current_scan_name)
                self.settings.child(('current_scan_path')).setValue(str(scan_path))

                if not scan_type:
                    self.h5_file_path = save_path #will remove the dataset part used for DAQ_scan datas
                    self.h5_file_name = base_name+datetime_now.strftime('_%Y%m%d_%H_%M_%S.h5')
                else:
                    self.h5_file_path = save_path
                    self.h5_file_name = save_path.name+".h5"
            else:
                self.h5_file_name = utils.select_file(start_path=base_name, save=True, ext='h5')
                self.h5_file_path = self.h5_file_name.parent

        else:
            if isinstance(addhoc_file_path, str):
                addhoc_file_path = Path(addhoc_file_path)
            self.h5_file_path = addhoc_file_path.parent
            self.h5_file_name = addhoc_file_path.name

        fullpathname = str(self.h5_file_path.joinpath(self.h5_file_name))
        self.settings.child(('current_h5_file')).setValue(fullpathname)

        if update_h5:
            self.current_scan_group = None

        scan_group = None
        if self.current_scan_group is not None:
            scan_group = self.current_scan_group._v_name

        if update_h5:
            self.close_file()
            self.h5_file = tables.open_file(fullpathname,'w', title='PyMoDAQ file')
            self.h5_file.root._v_attrs['pymodaq_version'] = get_version()
        else:
            self.close_file()
            self.h5_file = tables.open_file(fullpathname, 'a', title='PyMoDAQ file')

        self.raw_group = self.get_set_group(self.h5_file.root, 'Raw_datas', title='Data from PyMoDAQ modules')
        self.get_set_logger(self.raw_group)
        if scan_group is not None:
            self.current_scan_group = self.get_set_group(self.raw_group, scan_group)
        else:
            self.current_scan_group = self.get_last_scan()

        self.raw_group._v_attrs['type'] = self.settings.child(('save_type')).value()
        self.h5_file.root._v_attrs['file'] = self.h5_file_name
        if update_h5:
            self.h5_file.root._v_attrs['date'] = datetime_now.date().isoformat()
            self.h5_file.root._v_attrs['time'] = datetime_now.time().isoformat()
            for metadat in metadata:
                self.raw_group._v_attrs[metadat] = metadata[metadat]


        return update_h5

    def update_file_paths(self, update_h5=False):
        """

        Parameters
        ----------
        update_h5: bool
                   if True, will increment the file name and eventually the current scan index
                   if False, get the current scan index in the h5 file

        Returns
        -------
        scan_path: Path
        current_filename: str
        dataset_path: Path

        """

        try:
            # set the filename and path
            base_path = self.settings.child(('base_path')).value()
            base_name = self.settings.child(('base_name')).value()
            current_scan = self.settings.child(('current_scan_name')).value()
            scan_type = self.settings.child(('save_type')).value() == 'scan'
            ind_dataset = None
            if current_scan == '' or update_h5:
                next_scan_index = 0
                update_h5 = True #just started the main program so one should create a new h5
                self.file_loaded = False
            else:
                next_scan_index = self.get_scan_index()
            if self.file_loaded:
                ind_dataset = int(os.path.splitext(self.h5_file_name)[0][-3:])
                try:
                    curr_date = datetime.date.fromisoformat(self.h5_file.root._v_attrs['date'])
                except ValueError:
                    curr_date = parser.parse(self.h5_file.root._v_attrs['date']).date()
            else:
                curr_date = datetime.date.today()										 

            scan_path, current_filename, dataset_path = self.set_current_scan_path(base_path, base_name, update_h5,
                                next_scan_index, create_dataset_folder=scan_type, curr_date=curr_date,
                                ind_dataset=ind_dataset)
            self.settings.child(('current_scan_path')).setValue(str(scan_path))

            return scan_path, current_filename, dataset_path


        except Exception as e:
            print(e)

    def set_current_scan_path(self, base_dir, base_name='Scan', update_h5=False, next_scan_index=0, create_scan_folder=False,
                              create_dataset_folder=True, curr_date=None, ind_dataset=None):
        """

        Parameters
        ----------
        base_dir
        base_name
        update_h5
        next_scan_index
        create_scan_folder
        create_dataset_folder

        Returns
        -------

        """
        base_dir = Path(base_dir)
        if curr_date is None:
            curr_date = datetime.date.today()

        year_path = utils.find_part_in_path_and_subpath(base_dir, part=str(curr_date.year),
                                                  create=True)  # create directory of the year if it doen't exist and return it
        day_path = utils.find_part_in_path_and_subpath(year_path, part=curr_date.strftime('%Y%m%d'),
                                                 create=True)  # create directory of the day if it doen't exist and return it
        dataset_base_name = curr_date.strftime('Dataset_%Y%m%d')
        dataset_paths = sorted([path for path in day_path.glob(dataset_base_name + "*") if path.is_dir()])

        if ind_dataset is None:
            if dataset_paths == []:

                ind_dataset = 0
            else:
                if update_h5:
                    ind_dataset = int(dataset_paths[-1].name.partition(dataset_base_name + "_")[2]) + 1
                else:
                    ind_dataset = int(dataset_paths[-1].name.partition(dataset_base_name + "_")[2])

        dataset_path = utils.find_part_in_path_and_subpath(day_path, part=dataset_base_name + "_{:03d}".format(ind_dataset),
                                                     create=create_dataset_folder)
        scan_paths = sorted([path for path in dataset_path.glob(base_name + '*') if path.is_dir()])
        # if scan_paths==[]:
        #     ind_scan=0
        # else:
        #     if list(scan_paths[-1].iterdir())==[]:
        #         ind_scan=int(scan_paths[-1].name.partition(base_name)[2])
        #     else:
        #         ind_scan=int(scan_paths[-1].name.partition(base_name)[2])+1
        ind_scan = next_scan_index

        scan_path = utils.find_part_in_path_and_subpath(dataset_path, part=base_name + '{:03d}'.format(ind_scan),
                                                  create=create_scan_folder)
        return scan_path, base_name + '{:03d}'.format(ind_scan), dataset_path

    def get_last_scan(self):
        """Gets the last scan node within the h5_file and under the the **raw_group**

        Returns
        -------
        scan_group: pytables group or None


        """
        groups = [group for group in list(self.raw_group._v_groups) if 'Scan' in group]
        groups.sort()
        if len(groups) != 0:
            scan_group = self.get_node(self.raw_group, groups[-1])
        else:
            scan_group = None
        return scan_group


    def get_scan_index(self):
        """ return the scan group index in the "scan templating": Scan000, Scan001 as an integer
        """
        try:
            if self.current_scan_group is None:
                return 0
            else:

                groups = [group for group in list(self.raw_group._v_groups) if 'Scan' in group]
                groups.sort()
                flag = False
                if len(groups) != 0:
                    if 'scan_done' in self.get_node(self.raw_group, groups[-1])._v_attrs:
                        if self.get_node(self.raw_group, groups[-1])._v_attrs['scan_done']:
                            return len(groups)
                        return len(groups)-1

                # for child in list(self.get_node(self.raw_group, groups[-1])._v_groups):
                #     if 'scan' in child: #checks if a group like live_scan has been saved, meaning the previous scan completed
                #         return len(groups)

                return 0

        except Exception as e:
            return 0


    def load_file(self, base_path=None, file_path=None):
        """Opens a file dialog to select a h5file saved on disk to be used

        Parameters
        ----------
        base_path
        file_path

        See Also
        --------
        :py:meth:`init_file`
        :py:meth:`pymodaq.daq_utils.daq_utils.select_file`

        """
        if base_path is None:
            base_path = self.settings.child('base_path').value()
            if not os.path.isdir(base_path):
                base_path = None

        if file_path is None:
            file_path = utils.select_file(base_path, save=False, ext='h5')

        if not isinstance(file_path, Path):
            file_path = Path(file_path)

        if 'h5' not in file_path.suffix:
            raise IOError('Invalid file type, should be a h5 file')

        self.init_file(addhoc_file_path=file_path)
        self.file_loaded = True

    def close_file(self):
        """Flush data and close the h5file

        """
        try:
            if self.h5_file is not None:
                self.h5_file.flush()
                if self.h5_file.isopen:
                    self.h5_file.close()
        except Exception as e:
            print(e) #no big deal


    def is_node_in_group(self,where, name):
        """
        Check if a given node with name is in the group defined by where (comparison on lower case strings)
        Parameters
        ----------
        where: (str or node)
                path or parent node instance
        name: (str)
              group node name

        Returns
        -------
        bool
            True if node exists, False otherwise
        """

        nodes_names = [node._v_name.lower() for node in self.h5_file.list_nodes(where)]
        return name.lower() in nodes_names

    def get_set_logger(self, where):
        """ Retrieve or create (if absent) a logger enlargeable array to store logs
        Get attributed to the class attribute ``logger_array``
        Parameters
        ----------
        where: node
               location within the tree where to save or retrieve the array

        Returns
        -------
        logger_array: vlarray
                      enlargeable array accepting strings as elements
        """
        logger = 'Logger'
        if not logger in list(self.get_node(where)._v_children.keys()):
            # check if logger node exist
            text_atom = tables.atom.ObjectAtom()
            self.logger_array = self.add_string_array(where, logger)
            self.logger_array._v_attrs['type'] = 'log'
        else:
            self.logger_array = self.get_node(where, name=logger)
        return self.logger_array

    def add_string_array(self, where, name, title='', metadata=dict([])):
        text_atom = tables.atom.ObjectAtom()
        array = self.h5_file.create_vlarray(where, name, atom=text_atom, title=title)
        array._v_attrs['shape'] = (1,)

        array._v_attrs['type'] = 'strings'
        array._v_attrs['data_dimension'] = '0D'
        array._v_attrs['scan_type'] = 'scan1D'


        for metadat in metadata:
            array._v_attrs[metadat] = metadata[metadat]
        return array

    def get_set_group(self, where, name, title=''):
        """Retrieve or create (if absent) a node group
        Get attributed to the class attribute ``current_group``

        Parameters
        ----------
        where: str or node
               path or parent node instance
        name: str
              group node name
        title: str
               node title

        Returns
        -------
        group: group node
        """
        if not name in list(self.get_node(where)._v_children.keys()):
            self.current_group = self.h5_file.create_group(where, name, title)
        else:
            self.current_group = self.get_node(where, name)
        return self.current_group

    def get_group_by_title(self, where, title):
        node = self.get_node(where)
        for child_name in node._v_children:
            child = node._f_get_child(child_name)
            if 'TITLE' in child._v_attrs:
                if child._v_attrs['TITLE'] == title:
                    return child
        return None

    def get_node(self, where, name=None):
        return self.h5_file.get_node(where, name)


    def add_data_group(self,where, group_data_type, title='', settings_as_xml='', metadata=dict([])):
        """Creates a group node at given location in the tree

        Parameters
        ----------
        where: group node
               where to create data group
        group_data_type: list of str
                         either ['data0D', 'data1D', 'data2D', 'dataND']
        title: str, optional
               a title for this node, will be saved as metadata
        settings_as_xml: str, optional
                         XML string created from a Parameter object to be saved as metadata
        metadata: dict, optional
                  will be saved as a new metadata attribute with name: key and value: dict value

        Returns
        -------
        group: group node

        See Also
        --------
        :py:meth:`àdd_group`
        """
        if group_data_type not in group_data_types:
            raise Exception('Invalid data group type')
        group = self.add_group(group_data_type, '', where, title, settings_as_xml, metadata)
        return group

    def add_navigation_axis(self, data, parent_group, axis='x_axis', enlargeable=False, title='', metadata=dict([])):
        """
        Create carray or earray for navigation axis within a scan
        Parameters
        ----------
        data: (ndarray) of dimension 1
        parent_group: (str or node) parent node where to save new data
        axis: (str) either x_axis, y_axis, z_axis or time_axis
            'x_axis', 'y_axis', 'z_axis', 'time_axis' are axes containing scalar values (floats or ints)
            'time_axis' can be interpreted as the posix timestamp corresponding to a datetime object, see datetime.timestamp()
        enlargeable: (bool)
            if True the created array is a earray type
            if False the created array is a carray type
        """
        if axis not in ['x_axis', 'y_axis', 'z_axis', 'time_axis']:
            raise Exception('Invalid navigation axis name')

        array = self.add_array(parent_group, f"{self.settings.child(('save_type')).value()}_{axis}", 'navigation_axis', data_shape=data.shape,
                    data_dimension='1D', array_to_save=data, enlargeable=enlargeable, title=title, metadata=metadata)
        return array

    def add_data_live_scan(self,channel_group, data_dict, scan_type='scan1D', title=''):
        shape, dimension, size = utils.get_data_dimension(data_dict['data'], scan_type=scan_type, remove_scan_dimension=True)
        data_array = self.add_array(channel_group, 'Data', 'data', array_type=np.float,
                                    title=title,
                                    data_shape=shape,
                                    data_dimension=dimension, scan_type=scan_type,
                                    array_to_save=data_dict['data'])
        if 'x_axis' in data_dict:
            if not isinstance(data_dict['x_axis'], dict):
                array_to_save = data_dict['x_axis']
                tmp_dict = dict(label='', units='')
            else:
                tmp_dict = copy.deepcopy(data_dict['x_axis'])
                array_to_save = tmp_dict.pop('data')
        if 'x_axis' in data_dict:

            array = self.add_array(channel_group, 'x_axis', 'axis',
                                   array_type=np.float, array_to_save=array_to_save,
                                   enlargeable=False, data_dimension='1D', metadata=tmp_dict)
        if 'y_axis' in data_dict:
            if not isinstance(data_dict['y_axis'], dict):
                array_to_save = data_dict['y_axis']
                tmp_dict = dict(label='', units='')
            else:
                tmp_dict = copy.deepcopy(data_dict['y_axis'])
                array_to_save = tmp_dict.pop('data')
        if 'y_axis' in data_dict:
            array = self.add_array(channel_group, 'y_axis', 'axis',
                                   array_type=np.float, array_to_save=array_to_save,
                                   enlargeable=False, data_dimension='1D', metadata=tmp_dict)
        return data_array

    def add_data(self, channel_group, data_dict, scan_type='scan1D', scan_shape=[], title='', enlargeable=False,
                 init=False, add_scan_dim=False, metadata=dict([])):

        shape, dimension, size = utils.get_data_dimension(data_dict['data'])
        tmp_data_dict = copy.deepcopy(data_dict)

        #save axis
        # this loop covers all type of axis : x_axis, y_axis... nav_x_axis, ...
        axis_keys = [k for k in tmp_data_dict.keys() if 'axis' in k]
        for key in axis_keys:
            if not isinstance(tmp_data_dict[key], dict):
                array_to_save = tmp_data_dict[key]
                tmp_dict = dict(label='', units='')
            else:
                tmp_dict = copy.deepcopy(tmp_data_dict[key])
                array_to_save = tmp_dict.pop('data')
                tmp_data_dict.pop(key)

            array = self.add_array(channel_group, key, 'axis',
                   array_type=np.float, array_to_save=array_to_save,
                            enlargeable=False, data_dimension='1D', metadata=tmp_dict)

        # if 'x_axis' in data_dict:
        #     if not isinstance(data_dict['x_axis'], dict):
        #         array_to_save = data_dict['x_axis']
        #         tmp_dict = dict(label='', units='')
        #     else:
        #         tmp_dict = copy.deepcopy(data_dict['x_axis'])
        #         array_to_save = tmp_dict.pop('data')
        #         data_dict.pop('x_axis')
        #
        #     array = self.add_array(channel_group, 'x_axis', 'axis',
        #            array_type=np.float, array_to_save=array_to_save,
        #                     enlargeable=False, data_dimension='1D', metadata=tmp_dict)
        #
        # if 'y_axis' in data_dict:
        #     if not isinstance(data_dict['y_axis'], dict):
        #         array_to_save = data_dict['y_axis']
        #         tmp_dict = dict(label='', units='')
        #     else:
        #         tmp_dict = copy.deepcopy(data_dict['y_axis'])
        #         array_to_save = tmp_dict.pop('data')
        #         data_dict.pop('y_axis')
        #
        #     array = self.add_array(channel_group, 'y_axis', 'axis',
        #             array_type=np.float, array_to_save=array_to_save,
        #             enlargeable=False, data_dimension='1D', metadata=tmp_dict)

        array_to_save = tmp_data_dict.pop('data')
        if 'type' in tmp_data_dict:
            tmp_data_dict.pop('type') #otherwise this metadata would overide mandatory type for a h5 node
        tmp_data_dict.update(metadata)
        data_array = self.add_array(channel_group, 'Data', 'data', array_type=np.float,
            title=title, data_shape=shape, enlargeable=enlargeable, data_dimension=dimension, scan_type=scan_type,
            scan_shape=scan_shape,
            array_to_save=array_to_save,
            init=init, add_scan_dim=add_scan_dim, metadata=tmp_data_dict)

        self.h5_file.flush()
        return data_array


    def add_array(self, where, name, data_type, data_shape=(1,), data_dimension = '0D', scan_type='', scan_shape=[] ,
                  title='', array_to_save=None, array_type=None, enlargeable=False, metadata=dict([]),
                  init=False, add_scan_dim=False):
        if array_type is None:
            if array_to_save is None:
                array_type = np.float
            else:
                array_type = array_to_save.dtype

        if data_dimension not in data_dimensions:
            raise Exception('Invalid data dimension')
        if data_type not in data_types:
            raise Exception('Invalid data type')
        if scan_type != '':
            scan_type = utils.uncapitalize(scan_type)
        if scan_type not in scan_types:
            raise Exception('Invalid scan type')
        if enlargeable:
            shape = [0]
            if data_shape != (1,):
                shape.extend(data_shape)
            shape = tuple(shape)
            array = self.h5_file.create_earray(where, utils.capitalize(name), tables.Atom.from_dtype(np.dtype(array_type)), shape=shape,
                                               title=title, filters=self.filters)
            array._v_attrs['shape'] = shape
        else:
            if add_scan_dim:  #means it is an array initialization to zero
                shape = scan_shape[:]
                shape.extend(data_shape)
                if init or array_to_save is None:
                    array_to_save = np.zeros(shape)

            array = self.h5_file.create_carray(where, utils.capitalize(name), obj=array_to_save,
                                               title=title,
                                               filters=self.filters)
            array._v_attrs['shape'] = array_to_save.shape

        array._v_attrs['type'] = data_type
        array._v_attrs['data_dimension'] = data_dimension
        array._v_attrs['scan_type'] = scan_type


        for metadat in metadata:
            array._v_attrs[metadat] = metadata[metadat]
        return array

    def append(self, array, data):
        if not (isinstance(array, tables.vlarray.VLArray) or isinstance(array, tables.earray.EArray)):
            raise Exception('This array cannot be appended')
        if isinstance(data, np.ndarray):
            if data.shape != (1,):
                shape = [1]
                shape.extend(data.shape)
                array.append(data.reshape(shape))
            else:
                array.append(data)
        else:
            array.append(data)
        sh = list(array._v_attrs['shape'])
        sh[0] += 1
        array._v_attrs['shape'] = tuple(sh)

    def add_group(self, group_name, group_type, where, title='', settings_as_xml='', metadata=dict([])):
        """
        Add a node in the h5 file tree of the group type
        Parameters
        ----------
        group_name: (str) a custom name for this group
        group_type: (str) one of the possible values of **group_types**
        where: (str or node) parent node where to create the new group
        settings_as_xml: (str) XML string containing Parameters representation (see custom_Tree)
        metadata: (dict) extra metadata to be saved with this new group node

        Returns
        -------
        (node): newly created group node
        """

        if group_type not in group_types:
            raise Exception('Invalid group type')

        try:
            node = self.get_node(where, utils.capitalize(group_name))
        except tables.NoSuchNodeError as e:
            node = None

        if node is None:
            node = self.get_set_group(where, utils.capitalize(group_name), title)
            node._v_attrs['settings'] = settings_as_xml
            node._v_attrs['type'] = group_type.lower()
            for metadat in metadata:
                node._v_attrs[metadat] = metadata[metadat]

        return node

    def add_incremental_group(self, group_type, where, title='', settings_as_xml='', metadata=dict([])):
        """
        Add a node in the h5 file tree of the group type with an increment in the given name
        Parameters
        ----------
        group_type: (str) one of the possible values of **group_types**
        where: (str or node) parent node where to create the new group
        settings_as_xml: (str) XML string containing Parameters representation (see custom_Tree)
        metadata: (dict) extra metadata to be saved with this new group node

        Returns
        -------
        (node): newly created group node
        """
        if group_type not in group_types:
            raise Exception('Invalid group type')
        nodes = list(self.get_node(where)._v_children.keys())
        nodes_tmp = []
        for node in nodes:
            if utils.capitalize(group_type) in node:
                nodes_tmp.append(node)
        nodes_tmp.sort()
        if len(nodes_tmp) ==0:
            ind_group = -1
        else:
            ind_group = int(nodes_tmp[-1][-3:])
        group = self.get_set_group(where, utils.capitalize(group_type)+'{:03d}'.format(ind_group + 1), title)
        group._v_attrs['settings'] = settings_as_xml
        if group_type.lower() != 'ch':
            group._v_attrs['type'] = group_type.lower()
        else:
            group._v_attrs['type'] = ''
        for metadat in metadata:
            group._v_attrs[metadat] = metadata[metadat]
        return group


    def add_det_group(self, where, title='', settings_as_xml='', metadata=dict([])):
        """
        Add a new group of type detector
        See Also
        -------
        add_incremental_group
        """
        group = self.add_incremental_group('detector', where, title, settings_as_xml, metadata)
        return group

    def add_CH_group(self, where, title='', settings_as_xml='', metadata=dict([])):
        """
        Add a new group of type channel
        See Also
        -------
        add_incremental_group
        """
        group = self.add_incremental_group('ch', where, title, settings_as_xml, metadata)
        return group

    def add_live_scan_group(self, where, dimensionality, title='', settings_as_xml='', metadata=dict([])):
        """
        Add a new group of type live scan
        See Also
        -------
        add_incremental_group
        """
        group = self.add_group('Live_scan_{:s}'.format(dimensionality), '', where, title=title,
                               settings_as_xml=settings_as_xml, metadata=metadata)
        return group

    def add_scan_group(self, title='', settings_as_xml='', metadata=dict([])):
        """
        Add a new group of type scan
        See Also
        -------
        add_incremental_group
        """
        if self.current_scan_group is not None:
            if list(self.current_scan_group._v_children) == []:
                new_scan = False
            else:
                new_scan = True
        else:
            new_scan = True
        if new_scan:
            self.current_scan_group = self.add_incremental_group('scan', self.raw_group, title, settings_as_xml, metadata)
            self.current_scan_group._v_attrs['description'] = ''
            self.settings.child(('current_scan_name')).setValue(self.current_scan_group._v_name)


        return self.current_scan_group

    def add_move_group(self, where, title='', settings_as_xml='', metadata=dict([])):
        """
        Add a new group of type move
        See Also
        -------
        add_incremental_group
        """
        group = self.add_incremental_group('move', where, title, settings_as_xml, metadata)
        return group


    def parameter_tree_changed(self,param,changes):
        for param, change, data in changes:
            path = self.settings.childPath(param)

            if change == 'childAdded':
                pass

            elif change == 'value':
                if param.name() == 'show_file':
                    param.setValue(False)
                    self.show_file_content()


                elif param.name() == 'base_path':
                    try:
                        if not os.path.isdir(param.value()):
                            os.mkdir(param.value())
                    except:
                        self.update_status("The base path couldn't be set, please check your options")

                elif param.name() in custom_tree.iter_children(self.settings.child(('compression_options')), []):
                    self.filters = tables.Filters(
                        complevel=self.settings.child('compression_options', 'h5comp_level').value(),
                        complib=self.settings.child('compression_options', 'h5comp_library').value())

            elif change == 'parent':
                pass

    def update_status(self,status):
        self.status_sig.emit(utils.ThreadCommand("Update_Status", [status, 'log']))

    def show_file_content(self):
        form = QtWidgets.QWidget()
        if not self.h5_file.isopen:
            if self.h5_file_path.exists():
                self.analysis_prog = H5Browser(form, h5file=self.h5_file_path)
            else:
                raise FileExistsError('no File presents')
        else:
            self.h5_file.flush()
            self.analysis_prog = H5Browser(form, h5file=self.h5_file)
        form.show()



if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    prog = H5Saver()
    prog.settings_tree.show()

    prog.init_file(True)

    #prog.add_scan_group()

    sys.exit(app.exec_())