from django import forms
from django.contrib.auth.models import User


class RegisterForm(forms.ModelForm):

    # ================================================================
    # ❌ VULNERABILITY #1: Password stored in plaintext
    #
    # Problem:
    #   This field collects the password as plain text and the view
    #   (register_view in views.py) saves it directly into the database
    #   WITHOUT hashing it.
    #
    # Impact:
    #   If db.sqlite3 is leaked or accessed by an attacker,
    #   ALL user passwords become visible immediately.
    #
    # Why this is dangerous:
    #   - Users often reuse passwords across websites.
    #   - A plaintext password leak results in instant account takeover.
    #
    # What the secure version will do later:
    #   - Use user.set_password(form.cleaned_data['password'])
    #     to hash the password properly.
    #
    # This comment is required for the “vulnerability commit”.
    # ================================================================

    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        # You included email, so we keep it here
        fields = ['username', 'email', 'password']
