from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile  # Asegúrate de tener un modelo para el perfil si necesitas almacenar más datos

class CustomUserCreationForm(UserCreationForm):
    full_name = forms.CharField(max_length=100, required=True, label='Nombre Completo')
    phone_number = forms.CharField(max_length=15, required=True, label='Número de Teléfono')
    email = forms.EmailField(required=True, label='Correo Electrónico')
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=True, label='Fecha de Nacimiento')

    class Meta:
        model = User
        fields = ('username', 'full_name', 'phone_number', 'email', 'birth_date', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            # Si tienes un modelo Profile, crea una instancia
            profile = Profile.objects.create(user=user, phone_number=self.cleaned_data['phone_number'], birth_date=self.cleaned_data['birth_date'])
            profile.save()
        return user
