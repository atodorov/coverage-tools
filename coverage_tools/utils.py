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
from coverage.misc import CoverageException
from coverage.summary import SummaryReporter

def do_diff(cov1, cov2):
    result = []

    src1 = annotate_sources(cov1)
    src2 = annotate_sources(cov2)
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

        for line in difflib.unified_diff(s1, s2, fromfile=fname, tofile=fname, lineterm=""):
            result.append(line)

    return result

def annotate_sources(cov):
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
            source = cu.source_file().read().split('\n')
            analysis = cov._analyze(cu)

            executed = cov.data.executed_lines(cu.filename)
            missing = sorted(set(analysis.statements) - set(executed))

            i = 1
            for line in source:
#todo: for some reason in my coverage data the line for if statements and
# function definitions are reported as missing
                if i in missing:
                    src.append("- %s" % line)
                    rng = analysis.parser.multiline.get(i)
                    if rng:
                        missing += range(rng[0], rng[1]+1)
                else:
                    src.append("+ %s" % line)
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
