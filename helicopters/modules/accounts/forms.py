from django.forms.models import ModelForm
from flight_log.models import Employee

class EmployeeForm(ModelForm):
    class Meta:
        model = Employee
        fields = ['id_employee', 'name', 'email', 'phone']
        