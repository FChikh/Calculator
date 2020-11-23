from django import forms


class CalcForm(forms.Form):
    first = forms.IntegerField(label="Первое число",
                               max_value=10000,
                               min_value=0,
                               required=True)
    second = forms.IntegerField(label="Второе число",
                                max_value=10000,
                                min_value=0,
                                required=True)


