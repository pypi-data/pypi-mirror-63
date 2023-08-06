from django.urls import reverse_lazy
from django.views.generic import CreateView
from djangosubscribe.forms import SubscriberEmailOnlyForm
from django.contrib.messages.views import SuccessMessageMixin


# Create your views here.
class SubscriberView(SuccessMessageMixin, CreateView):
    template_name = "djangoadmin/djangosubscribe/create_subscriber_formview.html"
    form_class = SubscriberEmailOnlyForm
    success_url = reverse_lazy("djangosubscribe:subscriber")
    success_message = "You are successfully subscribed us."

    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)

    def get_success_message(self, cleaned_data):
        return self.success_message

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subscriberform'] = SubscriberEmailOnlyForm()
        return context
