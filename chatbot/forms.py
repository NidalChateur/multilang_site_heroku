from django import forms


class ChatbotForm(forms.Form):
    message = forms.CharField(required=True)
