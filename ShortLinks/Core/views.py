from django.views.generic import ListView
from django.contrib.sessions.models import Session

from .forms import LinkCreate
from .models import Link


class Home(ListView):
    model = Link
    queryset = Link.objects.all()
    form = LinkCreate

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.object_list = self.get_queryset()

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        context['form'] = self.form
        return context

    def post(self, request, **kwargs):
        form = LinkCreate(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            context = self.get_context_data()

            context['main_part'] = data.get('main_part')

            context['subpart'] = data.get('subpart')
            session = get_session(request)
            new_link = Link.objects.create(main_part=context['main_part'], subpart=context['subpart'],
                                           session=session)
            new_link.save()
            return super(Home, self).render_to_response(context)



def get_session(request):
    if request.session.session_key is None:
        request.session.save()
    session_key = request.session.session_key
    return Session.objects.get(session_key=session_key)
