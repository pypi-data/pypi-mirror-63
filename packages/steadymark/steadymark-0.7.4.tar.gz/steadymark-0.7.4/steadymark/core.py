#!/usr/bin/env python
# -*- coding: utf-8 -*-
# <steadymark - markdown-based test runner for python>
# Copyright (C) <2012-2020>  Gabriel Falcão <gabriel@nacaolivre.org>
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.


import re
import sys

from doctest import DocTestParser, DocTest, DebugRunner, DocTestFailure
from datetime import datetime
from misaka import BaseRenderer, Markdown, EXT_FENCED_CODE, EXT_NO_INTRA_EMPHASIS


class SteadyMarkDoctestRunner(DebugRunner):
    def report_unexpected_exception(self, out, test, example, exc_info):
        exc_type, exc_val, tb = exc_info
        exc_val.example = example

        if exc_type is DocTestFailure:
            raise exc_info
        raise exc_val


class MarkdownTest(object):
    def __init__(self, title, raw_code, globs, locs):
        self.title = title
        self.raw_code = raw_code

        self.globs = globs
        self.locs = locs
        dt_parser = DocTestParser()
        doctests = dt_parser.get_examples(raw_code)

        if any(doctests):
            self.code = DocTest(
                examples=doctests,
                globs=self.globs,
                name=title,
                filename=None,
                lineno=None,
                docstring=None,
            )
        else:
            self.code = compile(raw_code, title, "exec")

    def _run_raw(self):
        return eval(self.code, self.globs)

    def _run_doctest(self):
        if not isinstance(self.code, DocTest):
            raise TypeError("Attempt to run a non-doctest as doctest: %r" % self.code)

        runner = SteadyMarkDoctestRunner(verbose=False)
        return runner.run(self.code)

    def run(self):
        before = datetime.now()
        failure = None
        result = None

        is_doctest = isinstance(self.code, DocTest)
        try:
            import sure

            if is_doctest:
                result = self._run_doctest()
            else:
                result = self._run_raw()
            sure

        except:
            failure = sys.exc_info()

        after = datetime.now()

        return result, failure, before, after


class SteadyMark(BaseRenderer):
    title_regex = re.compile(r"(?P<title>[^#]+)(?:[#]+(?P<index>\d+))?")

    def preprocess(self, text):
        self._tests = [{}]
        self.globs = globals()
        self.locs = locals()
        return str(text)

    def blockcode(self, code, language):
        if language != "python":
            return

        if re.match(r"^#\s*steadymark:\s*ignore", code):
            return

        item = self._tests[-1]
        if "code" in item:  # the same title has more than 1 code
            found = self.title_regex.search(item["title"])
            title = found.group("title").rstrip()
            index = int(found.group("index") or 0)

            if not index:
                index = 1
                item["title"] = "{0} #{1}".format(title, index)

            new_item = {
                "title": "{0} #{1}".format(title, index + 1),
                "level": item["level"],
                "code": code,
            }

            self._tests.append(new_item)
            item = self._tests[-1]

        else:
            item["code"] = str(code).strip()

        if "title" not in item:
            item["title"] = "Test #{0}".format(len(self._tests))
            self._tests.append({})

    def header(self, title, level):
        t = str(title)
        t = re.sub(r"^[# ]*(.*)", r"\g<1>", t)
        t = re.sub(r"`([^`]*)`", r"\033[1;33m\g<1>\033[0m", t)
        self._tests.append({"title": t, "level": int(level)})

    def postprocess(self, full_document):
        tests = []

        globs = self.globs
        locs = self.locs
        for test in [x for x in self._tests if "code" in x]:
            raw_code = test["code"]
            title = test["title"]
            tests.append(MarkdownTest(title, raw_code, globs=globs, locs=locs))

        self.tests = tests

    @classmethod
    def inspect(cls, raw):
        renderer = cls()
        markdown = renderer.preprocess(raw)
        extensions = EXT_FENCED_CODE | EXT_NO_INTRA_EMPHASIS
        md = Markdown(renderer, extensions=extensions)
        full = md(markdown)
        renderer.postprocess(full)
        return renderer
