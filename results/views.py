from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse, Http404
from django.template import loader
from .models import StudentDetails,StudentResults
from results.forms import RegistrationForm,EditProfileForm,AdminRegistrationForm
from django.contrib.auth.forms import UserChangeForm,PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from .forms import UploadResultsForm, UploadDetailsForm,ViewResultsForm
from django.urls import reverse
from django.forms import modelformset_factory,inlineformset_factory
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings
# from django.views.decorators.cache import cache_control


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('results:login'))
    else:
        form = RegistrationForm()

    args = {'form':form}
    return render(request,'results/reg_form.html',args)


def admin_register(request):
    if request.method == 'POST' and request.user.is_superuser:
        form = AdminRegistrationForm(request.POST)
        if form.is_valid():
            form.save()

            return redirect(reverse('results:login'))
    elif request.user.is_superuser:
        form = AdminRegistrationForm()
        args = {'form':form}

        return render(request,'results/admin_reg_form.html',args)
    return redirect(reverse('results:login'))
# @cache_control(no_cache=True, must_revalidate=True, no_store=True)
# @login_required(login_url= settings.LOGIN_URL)
def view_profile(request):
    args = {'user': request.user}

    return render(request,'results/profile.html',args)


def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect(reverse('results:view_profile'))
    else:
        form = EditProfileForm(instance= request.user)
        args = {'form' : form}

        return render(request, 'results/edit_profile.html', args)


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user = request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect(reverse('results:view_profile'))
        else:
            return redirect(reverse('results:change_password'))
    else:
        form = PasswordChangeForm(user = request.user)
    args = {'form':form}

    return render(request,'results/change_password.html', args)


def view_results(request):

    # reg_no = StudentDetails.objects.only('register_number')
    your_register_number=""
    if request.method == 'POST':
       form = ViewResultsForm(request.POST)
       if form.is_valid():
           your_register_number = form.cleaned_data['your_register_number']

           if StudentDetails.objects.filter(register_number=your_register_number).exists():
               request.session['your_register_number'] = your_register_number
               return redirect(reverse('results:display_results'))

           elif not StudentDetails.objects.filter(register_number=your_register_number).exists():
               return redirect(reverse('results:invalid_register_number'))

    else:
       form = ViewResultsForm()

    args = {'form':form,
            'your_register_number':your_register_number}
    return render(request,'results/view_results.html',args)


def display_results(request):

    if request.session.has_key('your_register_number'):
        your_register_number = request.session['your_register_number']
        details = StudentDetails.objects.get(register_number = your_register_number)
        results = StudentResults.objects.filter(subject_id = your_register_number)

        #subjects = StudentResults.objects.all().filter(register_number = your_register_number)
        args = {'your_register_number' : your_register_number,
                'details' : details,
                'results' : results
                }
        return render(request,'results/display_results.html',args)

    else:
        return redirect(reverse('results:view_results'))


@staff_member_required(login_url = settings.PERMISSION_REQUIRED_URL)
def upload_results(request):

    UploadResultsFormset = inlineformset_factory(StudentDetails,
        StudentResults, form = UploadResultsForm,
        fields=('subject_name', 'grade'),
        extra=6,
        can_delete=True
    )

    if request.method == 'POST':
        details_form = UploadDetailsForm(request.POST)

        if details_form.is_valid():
            form = details_form.save()
            uploadresultsFormset = UploadResultsFormset(request.POST, request.FILES, instance=form)

            if uploadresultsFormset.is_valid():
                uploadresultsFormset.save()
                return redirect(reverse('results:save_results'))

    else:
        details_form = UploadDetailsForm()
        uploadresultsFormset = UploadResultsFormset()
        args = {'form':details_form,
                'formset' : uploadresultsFormset }
        return render(request, 'results/upload_results.html', args)

@staff_member_required(login_url = settings.PERMISSION_REQUIRED_URL)
def save_results(request):

    if request.method == 'POST':
        return redirect(reverse('results:upload_results'))


    return render(request,'results/save_results.html')

def permission_required(request):

    # if request.method == 'POST':
    #     return redirect(reverse('results:logout'))


    return render(request, 'results/permission_required.html')

def invalid_register_number(request):

    if request.method == 'POST':
        return redirect(reverse('results:view_results'))
    # if request.method == 'GET' and request.session.has_key('your_register_number'):
    #     # your_register_number = request.session['your_register_number']
    #     # details = StudentDetails.objects.get(register_number = your_register_number)
    #     return render(request,'results/invalid_register_number.html')
    # else:
    return render(request,'results/invalid_register_number.html')

def csrf_failure(request,reason=""):
    return redirect(reverse('results:logout'))
