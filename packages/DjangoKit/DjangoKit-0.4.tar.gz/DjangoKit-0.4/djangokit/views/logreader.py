#
# Copyright (c) 2020, Grigoriy Kramarenko
# All rights reserved.
# This file is distributed under the BSD 3-Clause License.
#
from os import listdir
from os.path import basename, join, exists
from django.views.generic import View
from djangokit.utils.responses import JsonResponse


class LogReaderView(View):
    """
    AJAX-представление, считывающее построчно log-файлы из определённого
    каталога. Для ограничения доступа
    """
    logdir = None
    maxlines = 500

    def _readfile(self, filename: str, start: int):
        exists(filename)
        f = open(filename, 'rb')
        f.seek(start)
        lines = []
        i = 0
        maxlines = self.maxlines
        for line in f:
            lines.append(line.encode('utf-8').rstrip('\n'))
            i += 1
            if i >= maxlines:
                break
        end = f.tell()
        f.close()
        return {
            'lines': lines,
            'end': end,
        }

    def _listdir(self, logdir: str):
        files = [f for f in listdir(logdir) if f.endswith('.log')]
        return {'files': files}

    def get(self, request, logfile=None, start=0):
        logdir = self.logdir
        data = {}
        if logfile:
            filename = join(logdir, basename(logfile))
            if exists(filename):
                data = self._readfile(filename, start)
        elif logdir and exists(logdir):
            data = self._listdir(logdir)
        return JsonResponse(data)
