import datetime
from django.shortcuts import redirect, render
from django.views import generic
from .forms import BS4ScheduleForm, SimpleScheduleForm,OptionsForm
from .models import Schedule, Options
from . import mixins
import json
from django.views import View

class MonthCalendar(mixins.MonthCalendarMixin, generic.TemplateView):
    """月間カレンダーを表示するビュー"""
    template_name = 'wakeup/month.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        calendar_context = self.get_month_calendar()
        context.update(calendar_context)
        return context


class WeekCalendar(mixins.WeekCalendarMixin, generic.TemplateView):
    """週間カレンダーを表示するビュー"""
    template_name = 'wakeup/week.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        calendar_context = self.get_week_calendar()
        context.update(calendar_context)
        return context


class WeekWithScheduleCalendar(mixins.WeekWithScheduleMixin, generic.TemplateView):
    """スケジュール付きの週間カレンダーを表示するビュー"""
    template_name = 'wakeup/week_with_schedule.html'
    model = Schedule
    date_field = 'date'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        calendar_context = self.get_week_calendar()
        context.update(calendar_context)
        return context


class MonthWithScheduleCalendar(mixins.MonthWithScheduleMixin, generic.TemplateView):
    """スケジュール付きの月間カレンダーを表示するビュー"""
    template_name = 'wakeup/month_with_schedule.html'
    model = Schedule
    date_field = 'date'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        calendar_context = self.get_month_calendar()
        context.update(calendar_context)
        return context


class MyCalendar(mixins.MonthCalendarMixin, mixins.WeekWithScheduleMixin, generic.CreateView):
    """月間カレンダー、週間カレンダー、スケジュール登録画面のある欲張りビュー"""
    template_name = 'wakeup/mycalendar.html'
    model = Schedule
    date_field = 'date'
    form_class = BS4ScheduleForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        week_calendar_context = self.get_week_calendar()
        month_calendar_context = self.get_month_calendar()
        context.update(week_calendar_context)
        context.update(month_calendar_context)
        return context

    def form_valid(self, form):
        month = self.kwargs.get('month')
        year = self.kwargs.get('year')
        day = self.kwargs.get('day')
        if month and year and day:
            date = datetime.date(year=int(year), month=int(month), day=int(day))
        else:
            date = datetime.date.today()
        schedule = form.save(commit=False)
        schedule.date = date
        schedule.save()
        return redirect('wakeup:mycalendar', year=date.year, month=date.month, day=date.day)


class MonthWithFormsCalendar(mixins.MonthWithFormsMixin, generic.View):
    """フォーム付きの月間カレンダーを表示するビュー"""
    template_name = 'wakeup/month_with_forms.html'
    model = Schedule
    date_field = 'date'
    form_class = SimpleScheduleForm

    def get(self, request, **kwargs):
        context = self.get_month_calendar()
        return render(request, self.template_name, context)

    def post(self, request, **kwargs):
        context = self.get_month_calendar()
        formset = context['month_formset']
        if formset.is_valid():
            formset.save()
            data = [[x.start_time,x.date] for x in Schedule.objects.all()]
            return redirect('wakeup:month_with_forms')

        return render(request, self.template_name, context)

# Create your views here.
def top(request):
    json_open = open('wakeup/options.json', 'r')
    json_load = json.load(json_open)
    if json_load['day_week_year']=='day':
        xlabel_name = []
        if json_load['absolute_or_relative'] == 'absolute':
            y_data = []
        else:
            y_data = []
    elif json_load['day_week_year']=='week':
        xlabel_name = []
        if json_load['absolute_or_relative'] == 'absolute':
            y_data = []
        else:
            y_data = []
    else:
        xlabel_name = []
        if json_load['absolute_or_relative'] == 'absolute':
            y_data = []
        else:
            y_data = []

    idea_times = []

    context = {
            'xlabels': xlabel_name,
            'data':y_data,
            'idea_time':idea_times,
    }
    return render(request, 'wakeup/top.html', context)



class HowToView(View):
    def get(self, request, *args, **kwargs):
        json_open = open('wakeup/how_to_options.json', 'r')
        json_load = json.load(json_open)
        context = {
            'default_alarm': 'on',
            'all_switch':'on' ,
            'all_time':'07:00:00',
            'holiday_switch':'off',
            'holiday_time':'07:00:00',
            'weekdays_switch':'off',
            'weekdays_time':'07:00:00',
            'day_of_the_week':'off',
            'sunday_switch':'off',
            'sunday_time':'07:00:00',
            'monday_switch':'off',
            'monday_time':'07:00:00',
            'tuesday_switch':'off',
            'tuesday_time':'07:00:00',
            'wednesday_switch':'off',
            'wednesday_time':'07:00:00',
            'thursday_switch':'off',
            'thursday_time':'07:00:00',
            'friday_switch':'off',
            'friday_time':'07:00:00',
            'saturday_switch':'off',
            'saturday_time':'07:00:00',
            'use_servo':'on',
            'use_sound':'on',
        }
        return render(request, 'wakeup/howto.html/', context)

    def post(self, request, *args, **kwargs):
        print("dhahdahafhfiahih")
        print(request.POST.get('use_servo',None))
        context = {
            'default_alarm': request.POST['default_alarm'],
            'all_switch':'on' ,
            'all_time':'07:00:00',
            'holiday_switch':'off',
            'holiday_time':'07:00:00',
            'weekdays_switch':'off',
            'weekdays_time':'07:00:00',
            'day_of_the_week':'off',
            'sunday_switch':'off',
            'sunday_time':'07:00:00',
            'monday_switch':'off',
            'monday_time':'07:00:00',
            'tuesday_switch':'off',
            'tuesday_time':'07:00:00',
            'wednesday_switch':'off',
            'wednesday_time':'07:00:00',
            'thursday_switch':'off',
            'thursday_time':'07:00:00',
            'friday_switch':'off',
            'friday_time':'07:00:00',
            'saturday_switch':'off',
            'saturday_time':'07:00:00',
            'use_servo':'on',
            'use_sound':'on',
        }
        return render(request, 'wakeup/howto.html/', context)


howto = HowToView.as_view()
