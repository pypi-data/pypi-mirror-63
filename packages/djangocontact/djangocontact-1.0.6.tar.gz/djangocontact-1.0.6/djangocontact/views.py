from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages
from django.template.loader import get_template
from django.core.mail import send_mail
""" Import from the local app. """
from .forms import EmailForm


# Create your views here.
def ConfirmationEmailView(request):
    template_name = "djangoadmin/djangocontact/confirmation_email_form.html"

    if request.method == "POST":
        # contact forms prefrences here.
        subject = settings.DEFAULT_EMAIL_SUBJECT
        sys_email = settings.DEFAULT_FROM_EMAIL
        email = [request.POST.get('email')]
        full_name = request.POST.get('full_name')
        message = settings.DEFAULT_EMAIL_CONTENT

        # Let's import the email form.
        emailform = EmailForm(request.POST or None)
        if emailform.is_valid():
            emailform.save()

            # context for email.
            context = {"email": email, "sys_email": sys_email, "full_name": full_name, "message": message}
            # get_template for mail.
            mail_template = get_template("djangoadmin/djangocontact/contact_us.html").render(context)
            # send mail here.
            send_mail(subject, mail_template, sys_email, email, fail_silently=True)

            # send message here.
            messages.success(request, 'Contact form submitted successfully.', extra_tags='success')
            return redirect('djangocontact:confirmation_email_view')
        else:
             messages.error(request, 'Contact form not submitted.', extra_tags='warning')
             return redirect('djangocontact:confirmation_email_view')
    else:
        emailform = EmailForm()
        context = {'emailform': emailform}
        return render(request, template_name, context)