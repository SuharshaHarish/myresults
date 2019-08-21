from django.shortcuts import redirect

#redirect from default url to login page.
def login_redirect(request):
    return redirect('/login/')
