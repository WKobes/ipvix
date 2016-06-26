from django.db import models
from datetime import datetime
from operator import itemgetter


class Visualization(models.Model):
    id = models.AutoField(primary_key=True)
    enterprise_id = models.IntegerField()
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True)
    function = models.CharField(max_length=255, blank=True)

    class Meta:
        unique_together = ("id", "enterprise_id")

    def __str__(self):
        return self.name


class Type(models.Model):
    id = models.AutoField(primary_key=True)
    enterprise_id = models.IntegerField()
    name = models.CharField(max_length=255)
    datatype = models.CharField(max_length=255, blank=True)
    description = models.CharField(max_length=1024, blank=True)
    units = models.CharField(max_length=255, blank=True)

    class Meta:
        unique_together = ("id", "enterprise_id")

    def __str__(self):
        return self.name


class TypeToVisualization(models.Model):
    id = models.AutoField(primary_key=True)
    type_enterprise_id = models.IntegerField()
    type = models.ForeignKey(Type, models.DO_NOTHING)
    visual_enterprise_id = models.IntegerField()
    visual = models.ForeignKey(Visualization, models.DO_NOTHING)
    filename = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return self.visual + " " + self.type

    @staticmethod
    def get_plot_numbers_time(filename=None):
        xdata = []
        ydata = []

        file = open(filename, 'r')

        # TODO count verwijderen
        count = 0
        for line in file:
            line = line[:-1]
            count += 1
            if count == 100000:
                break
            words = line.split('  ')
            words[words.__len__()-1] = "".join(words[words.__len__()-1].split())
            ydata.append(int(words[words.__len__()-1]))
            tmp = words[0].split('.')[1]
            date_object = datetime.strptime(words[0].split('.')[0], '%Y-%m-%d %H:%M:%S')
            xdata.append(int(date_object.strftime("%s")) * 1000 + int(tmp))

        temp = [list(x) for x in zip(*sorted(zip(xdata, ydata), key=itemgetter(0)))]
        xdata = temp[0]
        ydata = temp[1]

        chartdata = {'x': xdata, 'y': ydata, 'name': 'Data', }
        charttype = "lineChart"
        chartcontainer = 'linechart_container'
        data = {
            'charttype': charttype,
            'chartdata': chartdata,
            'chartcontainer': chartcontainer,
            'extra': {
                'x_is_date': True,
                'x_axis_format': '%H:%M:%S',
                'tag_script_js': True,
                'jquery_on_ready': False,
                'key': 'Data',
            }
        }
        return data

    @staticmethod
    def get_count(filename=None):
        xdata = []
        ydata = []

        file = open(filename, 'r')

        for line in file:
            line = line[:-1]
            words = line.split('  ')
            tmp = words[words.__len__() - 1]
            tmp = "".join(tmp.split())
            if tmp not in xdata:
                xdata.append(tmp)
                ydata.append(1)
            else:
                ydata[xdata.index(tmp)] += 1

        chartdata = {'x': xdata, 'y': ydata, 'name': 'Data', }
        charttype = "discreteBarChart"
        chartcontainer = 'discretebarchart_container'
        data = {
            'charttype': charttype,
            'chartdata': chartdata,
            'chartcontainer': chartcontainer,
            'extra': {
                'x_is_date': False,
                'x_axis_format': '',
                'tag_script_js': True,
                'jquery_on_ready': False,
            }
        }
        return data

    @staticmethod
    def get_bar_chart_not_0(filename=None):
        xdata = []
        ydata = []

        file = open(filename, 'r')

        # TODO count verwijderen
        count = 0
        for line in file:
            line = line[:-1]
            count += 1
            if count == 100000:
                break
            words = line.split('  ')
            words[words.__len__()-1] = "".join(words[words.__len__()-1].split())
            if int(words[words.__len__()-1]) != 0:
                ydata.append(int(words[words.__len__()-1]))
                tmp = words[0].split('.')[1]
                date_object = datetime.strptime(words[0].split('.')[0], '%Y-%m-%d %H:%M:%S')
                xdata.append(int(date_object.strftime("%s")) * 1000 + int(tmp))

        temp = [list(x) for x in zip(*sorted(zip(xdata, ydata), key=itemgetter(0)))]
        xdata = temp[0]
        ydata = temp[1]

        chartdata = {'x': xdata, 'y': ydata, 'name': 'Data', }
        charttype = "lineChart"
        chartcontainer = 'linechart_container'
        data = {
            'charttype': charttype,
            'chartdata': chartdata,
            'chartcontainer': chartcontainer,

            'extra': {
                'x_is_date': True,
                'x_axis_format': '%H:%M:%S',
                'tag_script_js': True,
                'jquery_on_ready': False,
            }
        }
        return data

    @staticmethod
    def get_line_chart_sum_second(filename=None):
            xdata = []
            ydata = []
            file = open(filename, 'r')
            for line in file:
                date_object = datetime.strptime(line[:19], '%Y-%m-%d %H:%M:%S')
                tmp = int(date_object.strftime("%s")) * 1000
                tmp2 = int(line[23:-1])
                if tmp not in xdata:
                    xdata.append(tmp)
                    ydata.append(tmp2)
                else:
                    ydata[xdata.index(tmp)] += tmp2

            temp = [list(x) for x in zip(*sorted(zip(xdata, ydata), key=itemgetter(0)))]
            xdata = temp[0]
            ydata = temp[1]

            chartdata = {'x': xdata, 'y': ydata, 'name': 'Data', }
            charttype = "lineChart"
            chartcontainer = 'linechart_container'
            data = {
                'charttype': charttype,
                'chartdata': chartdata,
                'chartcontainer': chartcontainer,
                'extra': {
                    'x_is_date': True,
                    'x_axis_format': '%H:%M:%S',
                    'tag_script_js': True,
                    'jquery_on_ready': False,
                    'key': 'Data',
                }
            }
            return data

    @staticmethod
    def get_cdf(filename=None):

        xdata = []
        file = open(filename, 'r')
        # TODO Delete count
        count = 0
        for line in file:
            count += 1
            if count > 100000:
                break
            tmp = int(line[23:-1])
            xdata.append(tmp)

        import numpy as np
        sorted = np.sort(xdata)
        yvals = np.arange(len(sorted)) / float(len(sorted))

        chartdata = {'x': sorted, 'y': yvals, 'name': 'Data'}
        charttype = "lineChart"
        chartcontainer = 'linechart_container'
        data = {
            'charttype': charttype,
            'chartdata': chartdata,
            'chartcontainer': chartcontainer,
            'extra': {
                'x_is_date': False,
                'x_axis_format': '',
                'tag_script_js': True,
                'jquery_on_ready': False,
            },
        }
        return data

    @staticmethod
    def get_cdf_not_0(filename=None):

        xdata = []
        file = open(filename, 'r')
        # TODO Delete count
        count = 0
        for line in file:
            count += 1
            if count > 100000:
                break
            tmp = int(line[23:-1])
            if tmp != 0:
                xdata.append(tmp)

        import numpy as np
        sorted = np.sort(xdata)
        yvals = np.arange(len(sorted)) / float(len(sorted))

        chartdata = {'x': sorted, 'y': yvals, 'name': 'Data'}
        charttype = "lineChart"
        chartcontainer = 'linechart_container'
        data = {
            'charttype': charttype,
            'chartdata': chartdata,
            'chartcontainer': chartcontainer,
            'extra': {
                'x_is_date': False,
                'x_axis_format': '',
                'tag_script_js': True,
                'jquery_on_ready': False,
            },
        }
        return data
