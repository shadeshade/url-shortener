from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, RedirectView

from .forms import LinkCreate
from .models import Link
from .tools import get_session, create_rule, client


class Home(ListView):
    model = Link
    form = LinkCreate
    paginate_by = 10

    def get_queryset(self):
        session = get_session(self.request)
        queryset = Link.objects.filter(session=session).order_by('-id')
        return queryset

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        context['form'] = self.form
        return context

    def post(self, request, **kwargs):
        form = LinkCreate(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            self.object_list = self.get_queryset()
            main_part = data.get('main_part')
            subpart = data.get('subpart')
            create_rule(request, main_part, subpart)
            context = self.get_context_data()
            return super(Home, self).render_to_response(context)
        else:
            messages.error(request=request, message='Input unique subpart, please')
            return redirect(reverse('home_page'))


class LinkRedirectView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        if client.get(kwargs['short_link']):
            link = client.get(kwargs['short_link'])
        else:
            link = get_object_or_404(Link, subpart=kwargs['short_link'])
            link = link.main_part
        return link
