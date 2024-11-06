from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type  #را نصب کنیم six باید این pip install six با دستور

#the code below generates our token
class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            text_type(user.pk) + text_type(timestamp) +
            text_type(user.is_active)
        )


account_activation_token = AccountActivationTokenGenerator()
#The default value for password reset token is seven days, so the user will have seven days by default to click on that but this duration can be changed in the settings.py file (password_reset_timeout_days).