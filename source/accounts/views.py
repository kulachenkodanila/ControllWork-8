

from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.views import PasswordChangeView

from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import CreateView, DetailView, UpdateView

from accounts.forms import MyUserCreationForm, UserChangeForm, ProfileChangeForm, ChangeForm

User = get_user_model()


class RegisterView(CreateView):
    model = User
    template_name = 'registration.html'
    form_class = MyUserCreationForm

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(self.get_success_url())

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if not next_url:
            next_url = self.request.POST.get('next')
        if not next_url:
            next_url = reverse('webapp:index')
        return next_url


def login_view(request):
    context = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('webapp:index')
        else:
            context['has_error'] = True
    return render(request, 'login.html', context=context)


def logout_view(request):
    logout(request)
    return redirect('webapp:index')


class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "profile.html"
    paginate_by = 5
    paginate_orphans = 0
    context_object_name = "user_obj"



class ChangeProfileView(PermissionRequiredMixin, UpdateView):
    model = User
    form_class = ChangeForm
    template_name = "change_user.html"
    profile_form_class = ProfileChangeForm
    context_object_name = "user_obj"

    def has_permission(self):
        return self.request.user.is_superuser or self.request.user == self.get_object()

    def get_form_class(self):
        if self.request.GET.get("is_admin"):
            return ChangeForm
        return UserChangeForm

    def get_success_url(self):
        return reverse("accounts:profile", kwargs={"pk": self.object.pk})





class ChangePasswordView(PasswordChangeView):
    template_name = "change_password.html"

    def get_success_url(self):
        return reverse("accounts:profile", kwargs={"pk": self.request.user.pk})