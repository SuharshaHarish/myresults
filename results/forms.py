from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from .models import StudentDetails,StudentResults,UserAdmin
from django.forms import inlineformset_factory,modelformset_factory
from django.forms.models import BaseInlineFormSet

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        )

    def save(self,commit=True):
        user = super(RegistrationForm,self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

            return user

class AdminRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        )

    def save(self,commit=True):
        user = super(AdminRegistrationForm,self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        user.is_staff = True
        user.is_superuser = True



        if commit:
            user.save()
            query = UserAdmin(admin_user = user , admin_username = user)
            query.save()

            return user
    # def save_admin()

class EditProfileForm (UserChangeForm):

    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',

            )

class UploadDetailsForm (forms.ModelForm):

    class Meta:
        model = StudentDetails
        fields = (
            'register_number',
            'student_name',
            'student_branch',

            )

class UploadResultsForm (forms.ModelForm):

    class Meta:
        model = StudentResults
        fields = (
            'subject_name',
            'grade'

            )

class ViewResultsForm(forms.Form):

    your_register_number = forms.CharField(max_length=20)



    # def clean(self):
    #     cleaned_data = super(ViewResultsForm, self).clean()
    #     your_register_number = cleaned_data.get('your_register_number')



    # def save(self,commit=True):
    #     register_number = super(UploadResultsForm,self).save(commit=False)
    #     register_number.student_name = self.cleaned_data['student_name']
    #     register_number.student_branch = self.cleaned_data['student_branch']
    #
    #     if commit:
    #         register_number.save()
    #
    #         return register_number
    #
    #     result = super(UploadResultsFormset, self).save(commit=commit)
    #
    #     for form in self.forms:
    #
    #             if not self._should_delete_form(form):
    #                 form.save(commit=commit)



# data = {
#      'form-TOTAL_FORMS': '2',
#      'form-INITIAL_FORMS': '0',
#      'form-MAX_NUM_FORMS': '',
#      # 'form-0-title': 'Test',
#      # 'form-0-pub_date': '1904-06-16',
#      # 'form-1-title': 'Test',
#      # 'form-1-pub_date': '1912-06-23',
#  }


#
# class BaseUploadResultsFormset ():
#
#     class Meta:
#         model = StudentResults
#         fields = (
#             'register_number',
#             'student_name',
#             'student_branch',
#
#
#             )

    # def add_fields(self, form, index):
    #     super(BaseUploadResultsFormset, self).add_fields(form, index)
    #
    #     # save the formset in the 'nested' property
    #     form.nested = UploadResultsFormset(
    #                     instance=form.instance,
    #                     data=form.data if form.is_bound else None,
    #                     files=form.files if form.is_bound else None,
    #                     prefix='address-%s-%s' % (
    #                         form.prefix,
    #                         UploadResultsFormset.get_default_prefix()),
    #                     extra=1)



    # def __init__(self,  *args, **kwargs):
    #     super(UploadResultsForm, self).__init__(*args, **kwargs)
    #
    #     for i in range(0, 11):
    #         self.fields["subject %d" % i] = forms.CharField()
    #         self.fields["grade "] = forms.CharField()
