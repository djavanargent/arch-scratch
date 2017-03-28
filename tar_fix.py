#!/usr/bin/env python

import tarfile
import os

class Tarball:
    def __init__(self, infile, outfile):
        self.infile = infile
        self.outfile = outfile
    def drop_lead_comp(self):
        """Removes leading path component (top-level dir) from input tar file."""
        with tarfile.open(self.infile) as tarin, tarfile.open(self.outfile, 'w:gz') as tarout:
            lead_comp_name = os.path.commonpath(tarin.getnames())
            if lead_comp_name:
                prefix_len = len(lead_comp_name + '/')
                tarin.members.remove(tarin.getmember(lead_comp_name))
                for m in tarin.members:
                    m.path = m.path[prefix_len:]
                    if m.linkname:
                        if m.islnk():
                            m.linkname = m.linkname[prefix_len:]
                        tarout.addfile(m)
                    else:
                        tarout.addfile(m, tarin.extractfile(m))

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="Remove leading path component from input tarball contents and save "
                                                 "the result in output tarball.", add_help=False)
    group = parser.add_argument_group("Arguments")
    group.add_argument("--help", action='store_true', help="Show this help message and exit.")
    args = parser.parse_known_args()
    group.add_argument("--input", metavar='PATH', dest='infile', type=str, help="Input tar[.gz/xz/bz2] file path.",
                       required=True)
    group.add_argument("--output", metavar='PATH', dest='outfile', type=str, help="Output tar.gz file path.",
                       required=True)
    if args[0].help:
        parser.exit(parser.print_help())
    else:
        args = parser.parse_args()
        tarball = Tarball(args.infile, args.outfile)
        tarball.drop_lead_comp()
