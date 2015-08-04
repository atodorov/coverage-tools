# The MIT License (MIT)
#
# Copyright (c) 2015 Alexander Todorov <atodorov@nospam.otb.bg>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import difflib
from math import log10
from fnmatch import fnmatch
from coverage.backward import iitems
from coverage.data import CoverageData
from coverage.files import PathAliases
from coverage.annotate import AnnotateReporter

def do_diff(cov1, cov2, show_lines=False, include=[], exclude=[]):
    result = []

    src1 = annotate_sources(cov1, show_lines, include, exclude)
    src2 = annotate_sources(cov2, show_lines, include, exclude)
    fnames = sorted(set(src1.keys() + src2.keys()))

    for fname in fnames:
        if src1.has_key(fname):
            s1 = src1[fname]
        else:
            s1 = []

        if src2.has_key(fname):
            s2 = src2[fname]
        else:
            s2 = []

        for line in difflib.unified_diff(s1, s2,
                                        fromfile="a/"+fname.lstrip('/'),
                                        tofile="b/"+fname.lstrip('/'),
                                        lineterm=""):
            result.append(line)

    return result

class MyAnnotateReporter(AnnotateReporter):
    def __init__(self, coverage, config):
        super(MyAnnotateReporter, self).__init__(coverage, config)
        self.show_lines = False
        self.report_result = {}

    def report(self, morfs, directory=None):
        self.report_result = {}
        super(MyAnnotateReporter, self).report(morfs, directory)

    def annotate_file(self, cu, analysis):
        """
            Copied from the parent but returns a list
            instead of writing to a file and doesn't return on
            relative files.
        """
        source = cu.source_file()
        dest = []

        statements = analysis.statements
        missing = analysis.missing
        excluded = analysis.excluded

        lineno = 0
        i = 0
        j = 0
        covered = True
        prefix = ""
        while True:
            line = source.readline()
            if line == '':
                break
            lineno += 1
            while i < len(statements) and statements[i] < lineno:
                i += 1
            while j < len(missing) and missing[j] < lineno:
                j += 1
            if i < len(statements) and statements[i] == lineno:
                covered = j >= len(missing) or missing[j] > lineno
            if self.blank_re.match(line):
                prefix = '  '
            elif self.else_re.match(line):
                # Special logic for lines containing only 'else:'.
                if i >= len(statements) and j >= len(missing):
                    prefix = '! '
                elif i >= len(statements) or j >= len(missing):
                    prefix = '> '
                elif statements[i] == missing[j]:
                    prefix = '! '
                else:
                    prefix = '> '
            elif lineno in excluded:
                prefix = '- '
            elif covered:
                prefix = '> '
            else:
                prefix = '! '
            if self.show_lines:
                prefix = '{n: 6} {p}'.format(n=lineno, p=prefix)
            dest.append(prefix + line.rstrip("\n"))
        source.close()
        self.report_result[cu.filename] = dest


def annotate_sources(cov, show_lines=False, include=[], exclude=[]):
    """
        Returns a map of source files where
        missing lines are annotated with
    """
    cov.config.from_args(omit=exclude, include=include, ignore_errors=True)

    reporter = MyAnnotateReporter(cov, cov.config)
    reporter.show_lines = show_lines
    reporter.report(None)
    return reporter.report_result

def annotated_src_as_string(src):
    result = ""
    for fname in sorted(src.keys()):
        result += '!!! missing/%s\n' % fname.lstrip('/')
        result += '>>> covered/%s\n' % fname.lstrip('/')
        for line in src[fname]:
            result += "%s\n" % line

    return result

def combine(data_paths, output_file):
    try:
        if CoverageData.combine_parallel_data:
            # use the old API, version 3.6 and 3.7.X
            data = CoverageData(output_file)
            data = coverage3x_combine(data_paths, data)
            data.write()
    except AttributeError:
        # new versions have better support for combining files
        # and the method combine_parallel_data() has been moved
        # to teh new CoverageDataFiles class.
        # see https://bitbucket.org/ned/coveragepy/pull-requests/62
        from coverage.data import CoverageDataFiles

        data = CoverageData()

        dataf = CoverageDataFiles()
        dataf.combine_parallel_data(data, data_paths=data_paths)

        data.write_file(output_file)

def coverage3x_combine(files, data):
    """
        Combine all coverage files from @files
        into @data.

        Note: this works with coverage 3.6 (and possibly older) versions.
    """

    aliases = PathAliases()

    for f in files:
        new_lines, new_arcs = data._read_file(f)

        for filename, file_data in iitems(new_lines):
            filename = aliases.map(filename)
            data.lines.setdefault(filename, {}).update(file_data)
        for filename, file_data in iitems(new_arcs):
            filename = aliases.map(filename)
            data.arcs.setdefault(filename, {}).update(file_data)

    return data
