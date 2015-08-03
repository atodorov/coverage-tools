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
from coverage.files import PathAliases
from coverage.misc import CoverageException
from coverage.summary import SummaryReporter

try:
    from pip.commands.search import compare_versions
except ImportError:
    from distutils.version import StrictVersion, LooseVersion

    def compare_versions(version1, version2):
        """ Copied from pip """
        try:
            return cmp(StrictVersion(version1), StrictVersion(version2))
        # in case of abnormal version number, fall back to LooseVersion
        except ValueError:
            pass
        try:
            return cmp(LooseVersion(version1), LooseVersion(version2))
        except TypeError:
        # certain LooseVersion comparions raise due to unorderable types,
        # fallback to string comparison
            return cmp([str(v) for v in LooseVersion(version1).version],
                       [str(v) for v in LooseVersion(version2).version])

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

def annotate_sources(cov, show_lines=False, include=[], exclude=[]):
    """
        Returns a map of source files where
        where missing lines are annotated with
        - if missing and
        + if executed.
    """
    result = {}
    reporter = SummaryReporter(cov, cov.config)
    reporter.find_code_units(None)
    for cu in reporter.code_units:
        try:
            src = []
            source = cu.source_file().read().strip().split('\n')

            # skip all files which are not marked for inclusion
            skip_file = False
            for pattern in include:
                if fnmatch(cu.filename, pattern):
                    skip_file = False
                    break
                else:
                    skip_file = True
                    # don't break b/c there can be multiple patterns and the
                    # next one may include the file

            # exclude all files which are marked for exclusion
            for pattern in exclude:
                if fnmatch(cu.filename, pattern):
                    skip_file = True
                    break

            if skip_file:
                continue

            analysis = cov._analyze(cu)

            executed = cov.data.executed_lines(cu.filename)
            missing = sorted(set(analysis.statements) - set(executed))

            i = 1
            for line in source:
#todo: for some reason in my coverage data the line for if statements and
# function definitions are reported as missing
                if i in missing:
                    line = "- %s" % line
                    rng = analysis.parser.multiline.get(i)
                    if rng:
                        missing += range(rng[0], rng[1]+1)
                else:
                    line = "+ %s" % line

                # +1 b/c of log10, +1 leading space
                width = int(log10(len(source))) + 2
                if show_lines:
                    line = '{n: {w}} {l}'.format(n=i, w=width, l=line)

                src.append(line)
                i += 1

            result[cu.filename] = src
        except CoverageException:
#todo: if a source is missing locally it will not be included in the report
            pass

    return result

def annotated_src_as_string(src):
    result = ""
    for fname in sorted(src.keys()):
        result += '--- missing/%s\n' % fname.lstrip('/')
        result += '+++ covered/%s\n' % fname.lstrip('/')
        for line in src[fname]:
            result += "%s\n" % line

    return result


def coverage36_combine(files, data):
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
