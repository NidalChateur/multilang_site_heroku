from django.http import JsonResponse
from django.shortcuts import render
from django.utils.translation import gettext as _
from django.views import View
from openai import OpenAI

from .forms import ChatbotForm

client = OpenAI()


def ask_openai(message: str) -> str:
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant.",
            },
            {
                "role": "user",
                "content": message,
            },
        ],
    )

    return completion.choices[0].message


class Chatbot(View):
    def get(self, request):
        return render(request, "chatbot.html", {})

    def post(self, request):
        form = ChatbotForm(request.POST)
        if form.is_valid():
            try:
                message = ask_openai(form.cleaned_data.get("message"))

                return JsonResponse({"response": message})

            except Exception as e:
                print("openai error :", e)

                return JsonResponse(
                    {"response": _("I am here but it is not free. (^_^)")}
                )
