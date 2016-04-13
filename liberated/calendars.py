from calendar import HTMLCalendar

class HTML_Calendar(HTMLCalendar):
    def formatday(self, day, weekday):
        """
        Return a day as a table cell.
        """
        if day == 0:
            return '<td class="noday">&nbsp;</td>' # day outside month
        else:
            return '<td class="%s"><a href="%s">%d</a></td>' % (self.cssclasses[weekday], '/calendar/' + str(day), day)

class AttendanceCalendar(HTMLCalendar):

    def __init__(self, class_times, year, month, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.class_times = class_times
        self.year = year
        self.month = month

    def formatday(self, day, weekday):
        """
        Return a day as a table cell. Render any classes inside the day cell.
        """
        if day == 0:
            return '<td class="noday">&nbsp;</td>' # day outside month
        else:
            ret = '<td class="%s">%s<br>' % (self.cssclasses[weekday], day)
            strrr = '%s-%s-%s' % (self.getYear(), self.getMonth(), self.buffNum(day))
            todays_classes = self.class_times[strrr]

            for cl_t in todays_classes:
                thing = '/attendance/' + strrr + '%20' + cl_t
                ret += '<a href="%s">%s</a>' % (
                    thing,
                    cl_t
                )
                ret += '<br>'
            ret += '</td>'
            return ret

    def getMonth(self):
        return self.buffNum(self.month)
    def getYear(self):
        return self.buffNum(self.year)

    def buffNum(self, num):
        if len(str(num)) < 2:
            return '0' + str(num)
        return str(num)


