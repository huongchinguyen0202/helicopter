from django import forms
from django.forms import ModelForm
from flight_log.models import Employee,JobTitle
import constant

class RegisterForm (ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput(), max_length = 10)
    employee_number = forms.IntegerField(label = 'Employee Id')
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['job_title'] = forms.ModelChoiceField(queryset=JobTitle.objects.all(), empty_label="Job Title/ Choose One", required=False)
        self.fields['employee_number'] = forms.IntegerField(min_value = 0,max_value = 9999999)
        self.fields['phone'] = forms.IntegerField(min_value = 0,max_value = 999999999999)
    class Meta:
        model = Employee
        widgets = {
            'password': forms.PasswordInput(),
        }
        fields = ['first_name', 'last_name', 'employee_number', 'email', 'phone', 'job_title']