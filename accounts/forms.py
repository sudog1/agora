from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth import get_user_model

TRACK_CHOICES = [
    ("", "----"),
    ("AI", "AI"),
    ("Unity", "Unity"),
]


class CustomUserCreationForm(UserCreationForm):
    track = forms.ChoiceField(
        choices=TRACK_CHOICES,
        initial="",
    )

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ("username", "track", "email", "password1", "password2")

    def save(self, commit=True):
        username = self.cleaned_data.get("username")
        track = self.cleaned_data.get("track")
        new_username = f"{username}_{track}"

        if get_user_model().objects.filter(username=new_username).exists():
            return None

        user = super().save(commit=False)
        user.username = new_username
        if commit:
            user.save()
        return user
