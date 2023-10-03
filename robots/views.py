import json

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
                return HttpResponse("Your data has been saved!")

            else:
                return HttpResponse(form.errors.as_json(), 500)

        except Exception as e:
            return HttpResponse('Incorrect input data', 500)
