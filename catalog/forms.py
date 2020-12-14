from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import datetime

class FormaZaemaKnigi(forms.Form):
    data_zaema = forms.DateField(label=('Дата заема'),help_text="Введите дату в промежутке нынешнего дня и последующих 3 недель")

    def clean_data_zaema(self): # созздаем функцию которая будет проверять правильность введенных данных(дату)
         # Определяем условия которые будут учитываться при введении даты
        data = self.cleaned_data['data_zaema'] # задаем переменную которая будет в дальнейшем возвращать правильные данные
        if data < datetime.date.today():
            raise ValidationError('Ошибка, неверная дата') # должно перевести фразу
        if data > datetime.date.today()+datetime.timedelta(weeks=3):
            raise ValidationError('Ошибка, неверная дата') # должно перевести фразу

        #Возвращаем очищенные данные
        return data
