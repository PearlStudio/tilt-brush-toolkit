#!/usr/bin/env python

# Copyright 2016 Google Inc. All Rights Reserved.
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

import sys
import argparse
import os
import glob
import shutil

# The user documents folder for Tilt Brush application
tb_session_root = os.path.normpath("C:/Users/{0}/Documents/Tilt Brush".format(os.environ['USERNAME']))

# The place where all the Tilt Brush sessions are saved
tb_work_area_base = os.path.normpath("C:/Users/{0}/Desktop/TiltBrushWorkarea".format(os.environ['USERNAME']))

# Data of all sketches in the current session
all_sketches_data = {}

# The name of the session for renaming the session files
session_name_old = None
session_name_new = None


# Dynamically add the tiltbrush package to the PYTHONPATH
try:
    sys.path.append(os.path.join(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))), 'Python'))
    import tiltbrush.unpack
except ImportError:
    print >>sys.stderr, "Please put the 'Python' directory in your PYTHONPATH"


def convert(in_name, compress):
    """
    Converts the sketch file between directories and archived files.

    Archived files can further be compressed to save space
    :param in_name:
    :param compress:
    :return:
    """
    if os.path.isdir(in_name):
        tiltbrush.unpack.convert_dir_to_zip(in_name, compress)
        print "Converted %s to zip format" % in_name
    elif os.path.isfile(in_name):
        tiltbrush.unpack.convert_zip_to_dir(in_name)
        print "Converted %s to directory format" % in_name
    else:
        raise tiltbrush.unpack.ConversionError("%s doesn't exist" % in_name)


def get_snapshots_data(sketch_base):
    """
    Gather all the snapshots generated for this sketch

    Snapshots are saved as .png files with the naming convention
    <sketch_base>_00.png, <sketch_base>_01.png, <sketch_base>_02.png, ...
    :param sketch_base:
    :return:
    """
    snapshots = glob.glob(tb_session_root + "\\Snapshots\\{0}_*".format(sketch_base))
    return snapshots


def get_videos_data(sketch_base):
    """
    Gather all the videos generated for this sketch

    Video data is saved as

        <sketch_base>_00.HQ_Render.bat
        <sketch_base>_00.mp4
        <sketch_base>_00.usda

        <sketch_base>_01.HQ_Render.bat
        <sketch_base>_01.mp4
        <sketch_base>_01.usda

    In the example above, if <sketch_base> was Untitled_0, it means that
    two videos were recorded from that sketch

    :param sketch_base:
    :return:
    """
    video_data= glob.glob(tb_session_root + "\\Videos\\{0}_*".format(sketch_base))
    return video_data


def get_exports_data(sketch_base):
    """
    Gather all the export related data generated for this sketch

    Exported data is saved in the following directory structure

    <sketch_base>
        sketch_base.fbx
        sketch_base.json
        sketch_base.usd

    In the example above, if <sketch_base> was Untitled_0, it means that
    two videos were recorded from that sketch

    :param sketch_base:
    :return:
    """
    exports_data= glob.glob(tb_session_root + "\\Exports\\{0}\\*".format(sketch_base))
    return exports_data


def gather_sketch_data(sketch):
    """
    Accumulates all the sketch specific data for further processing
    """
    global all_sketches_data

    sketch_name = os.path.basename(sketch)
    sketch_base = os.path.splitext(sketch_name)[0]
    sketch_data = all_sketches_data[sketch_base] = {}

    ## Metadata about the sketch
    sketch_session = sketch_data['Session'] = {}
    sketch_session['path'] = sketch
    sketch_session['name'] = sketch_base

    ## Gather snapshots
    snapshots = get_snapshots_data(sketch_base)
    sketch_data['Snapshots'] = snapshots

    ## Gather videos

    videos = get_videos_data(sketch_base)
    sketch_data['Videos'] = videos

    ## Gather exports
    exports = get_exports_data(sketch_base)
    sketch_data['Exports'] = exports


def get_sketch_files(tb_session_root):
    """
    Return a list of Tilt Brush sketches that are files.

    Tilt Brush sketches converted to directories are ignored

    :param tb_session_root:
    :return:
    """
    items = glob.glob(tb_session_root + "\\Sketches\\Untitled_*")
    sketch_files = []

    for item in items:
        if os.path.isfile(item):
            sketch_files.append(item)

    return sketch_files

def main():
    global session_name_old
    global session_name_new

    description = """
        Saves a Tilt Brush session to a destination folder.
        User will be prompted to enter a file name for the session
    """
    parser = argparse.ArgumentParser(description=description)
    # parser.add_argument('tilt_file', type=str,
    #                   help="File to be saved")

    # args = parser.parse_args()
    # print args.tilt_file

    ## Sketches

    untitled_sketches = get_sketch_files(tb_session_root)

    for sketch in untitled_sketches:
        gather_sketch_data(sketch)

    session_name_new = raw_input("Enter session name:")

    sketch_data = all_sketches_data.items()[0][1]

    session_name_old = sketch_data['Session']['name']

    sketch_path = sketch_data['Session']['path']
    sketch_dir = os.path.dirname(sketch_path)
    sketch_path_new = sketch_dir + '\\{0}.tilt'.format(session_name_new)

    os.rename(sketch_path, sketch_path_new)

    sketch_data['Session']['path'] = sketch_path_new
    sketch_data['Session']['name'] = session_name_new

    # Rename Snapshots

    snapshots = sketch_data['Snapshots']

    for index, snapshot_path_old in enumerate(snapshots[:]):
        dir_name = os.path.dirname(snapshot_path_old)
        base = os.path.basename(snapshot_path_old)
        suffix = base.split(session_name_old)[-1]
        snapshot_path_new = '{0}\\{1}{2}'.format(dir_name, session_name_new, suffix)
        os.rename(snapshot_path_old, snapshot_path_new)
        snapshots[index] = snapshot_path_new

    # Rename Videos
    items = sketch_data['Videos']

    for index, path_old in enumerate(items[:]):
        dir_name = os.path.dirname(path_old)
        base = os.path.basename(path_old)
        suffix = base.split(session_name_old)[-1]
        path_new = '{0}\\{1}{2}'.format(dir_name, session_name_new, suffix)
        os.rename(path_old, path_new)
        items[index] = path_new

    # Rename Exports

    try:
        items = sketch_data['Exports']

        for index, path_old in enumerate(items[:]):
            dir_name = os.path.dirname(path_old)
            base = os.path.basename(path_old)
            if not base.startswith(session_name_old):
                continue
            suffix = os.path.splitext(base)[-1]
            path_new = "{0}\\{1}{2}".format(dir_name, session_name_new, suffix)
            os.rename(path_old, path_new)
            items[index] = path_new

        # Rename the exports folder itself
        path_old = tb_session_root + "\\Exports\\" + session_name_old
        path_new = tb_session_root + "\\Exports\\" + session_name_new

        os.rename(path_old, path_new)
    except WindowsError:
        pass
    except Exception:
        raise

    # Convert Tilt File to a Directory

    convert(all_sketches_data[session_name_old]['Session']['path'], False)

    ## Moving session data to a Work Area

    if not os.path.exists(tb_work_area_base):
        os.mkdir(tb_work_area_base)

    # The workarea for the current session
    session_workarea = "{0}\\{1}".format(tb_work_area_base, session_name_new)

    shutil.copytree(tb_session_root, session_workarea)

    # Remove
    try:
        shutil.rmtree(tb_session_root)
    except Exception as e:
        print("Unable to remove Tilt Brush session folder. Delete ")


if __name__ == '__main__':
    main()
