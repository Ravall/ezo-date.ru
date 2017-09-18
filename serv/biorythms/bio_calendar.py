# -*- coding: utf-8 -*-
import calendar
from datetime import date
from snct_date.date import today, day_maps, yyyy_mm_dd, date_shift, num_days_in_month


class MyHtmlCalendar(calendar.LocaleHTMLCalendar):
    today = date.today()

    def formatday(self, day, weekday):
        css = [self.cssclasses[weekday]]
        if (
            day == self.today.day and
            self.today.month == self.month and
            self.today.year == self.year
        ):
            css.append('today')

        if self.current_date == [day, self.month, self.year]:
            css.append('selected')

        if day == 0:
            return '<td class="noday">&nbsp;</td>'
        else:
            return (
                '<td class="%s">'
                '<a class="get_bio_data" day="%s" href="#">%d</a>'
                '</td>'
            ) % (
                ' '.join(css),
                yyyy_mm_dd((day, self.month, self.year)),
                day
            )

    def formatmonthname(self, theyear, themonth, withyear=True):
        with calendar.TimeEncoding(self.locale) as encoding:
            s = calendar.month_name[themonth]
            if encoding is not None:
                s = s.decode(encoding)
            if withyear and theyear != self.today.year:
                s = '%s, %s' % (s, theyear)
            prev_month_day = yyyy_mm_dd(
                date_shift(1, themonth, theyear, -1)
            )
            next_month_day = yyyy_mm_dd(
                date_shift(
                    num_days_in_month(themonth,theyear),
                    themonth, theyear, 1
                )
            )
            return (
                '<tr><th colspan="7" class="month">'
                '<a href="#" day="%s" class="get_bio_data">&larr;</a> '
                '%s'
                ' <a href="#" day="%s" class="get_bio_data">&rarr;</a>'
                '</th></tr>'
            )% (prev_month_day, s, next_month_day)

    def formatmonth(self, theyear=today.year, themonth=today.month, withyear=True):
        self.year = theyear
        self.month = themonth
        return super(MyHtmlCalendar, self).formatmonth(theyear, themonth, withyear)