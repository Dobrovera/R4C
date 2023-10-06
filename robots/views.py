import json
import pandas as pd

from io import BytesIO
from datetime import datetime, timedelta
from django.db.models import Count
from django.views import View
from django.http import HttpResponse

from .models import Robot
from .forms import RobotForm


class RobotView(View):
    model = Robot

    def post(self, request):

        try:
            robot_data = json.loads(request.body)
            form = RobotForm(robot_data)
            if form.is_valid():
                model = robot_data['model']
                version = robot_data['version']
                created = robot_data['created']
                serial = f"{model}-{version}"
                robot = Robot(
                    serial=serial,
                    model=model,
                    version=version,
                    created=created)
                robot.save()
                return HttpResponse('Данные успешно сохранены!!')

            else:
                return HttpResponse(form.errors.as_json(), 500)

        except Exception as e:
            return HttpResponse(f'Ошибка: {e}', 500)


class RobotLastWeekDataView(View):
    model = Robot

    def get(self, request):
        try:
            six_days_ago = datetime.now() - timedelta(days=6)
            robots = (Robot.objects
                      .filter(created__range=(six_days_ago, datetime.now()))
                      .values('model', 'version')
                      .annotate(total_created=Count('created'))
                      .order_by('model', 'total_created'))

            filename = 'robots_last_week.xlsx'

            data = []
            current_model = None

            with BytesIO() as b:
                with pd.ExcelWriter(b, engine="xlsxwriter") as wr:
                    for robot in robots:
                        if current_model == robot['model']:
                            data.append({
                                "Модель": robot['model'],
                                "Версия": robot['version'],
                                "Количество за неделю": robot['total_created']
                            })
                            sheet = pd.DataFrame(data)
                            sheet.to_excel(wr, sheet_name=f"{robot['model']}", index=False)

                        else:
                            data = []
                            data.append({
                                "Модель": robot['model'],
                                "Версия": robot['version'],
                                "Количество за неделю": robot['total_created']
                            })
                            sheet = pd.DataFrame(data)
                            sheet.to_excel(wr, sheet_name=f"{robot['model']}", index=False)
                            current_model = robot['model']

                response = HttpResponse(b.getvalue(), content_type='application/force-download')
                response['Content-Disposition'] = f'attachment; filename="{filename}"'

            return response

        except Exception as e:
            return HttpResponse(f'Ошибка: [{e}]', 500)
