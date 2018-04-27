import argparse
import datetime
import os
import sys

from typing import Dict, Any, List, Tuple, Optional
from xml.dom import minidom  # type: ignore

from chart import Chart, XML

def main() -> int:
    parser = argparse.ArgumentParser(description="A utility to convert StepMania-like charts to Museca format.")
    parser.add_argument(
        "file",
        metavar="FILE",
        help=".mu file to convert to Museca format.",
        type=str,
    )
    parser.add_argument(
        "id",
        metavar="ID",
        help="ID to assign this song.",
        type=int,
    )
    parser.add_argument(
        "-d",
        "--directory",
        help="Directory to place files in. Defaults to current directory.",
        default='.',
    )

    args = parser.parse_args()
    root = args.directory
    if root[-1] != '/':
        root = root + '/'
    root = os.path.realpath(root)
    os.makedirs(root, exist_ok=True)

    fp = open(args.file, 'rb')
    data = fp.read()
    fp.close()

    # First, parse out the chart and get the XML writer ready.
    chart = Chart(data)
    xml = XML(chart, args.id)

    # First, write out a metadata file, that can be copied into music-info.xml
    fp = open(os.path.join(root, 'music-info.xml'), 'wb')
    fp.write(xml.get_metadata())
    fp.close()

    # Now, write out the chart data
    fp = open(os.path.join(root, '01_{num:04d}_nov.xml'.format(num=args.id)), 'wb')
    fp.write(xml.get_notes('novice'))
    fp.close()

    # Now, write out the chart data
    fp = open(os.path.join(root, '01_{num:04d}_adv.xml'.format(num=args.id)), 'wb')
    fp.write(xml.get_notes('advanced'))
    fp.close()

    # Now, write out the chart data
    fp = open(os.path.join(root, '01_{num:04d}_exh.xml'.format(num=args.id)), 'wb')
    fp.write(xml.get_notes('exhaust'))
    fp.close()

    # Write out miscelaneous files
    fp = open(os.path.join(root, '01_{num:04d}.def'.format(num=args.id)), 'wb')
    fp.write('#define 01_{num:04d}   0\n'.format(num=args.id).encode('ascii'))
    fp.close()
    fp = open(os.path.join(root, '01_{num:04d}_prv.def'.format(num=args.id)), 'wb')
    fp.write('#define 01_{num:04d}_prv   0\n'.format(num=args.id).encode('ascii'))
    fp.close()

    return 0

if __name__ == '__main__':
    sys.exit(main())