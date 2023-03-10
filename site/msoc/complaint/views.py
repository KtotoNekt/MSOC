from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponse
from django.shortcuts import render
from django.views.generic import CreateView

from .forms import ComplaintForm
from main.models import Music
from .models import Complaint


# Create your views here.
def complaints_view(req):
    if req.user.is_staff:
        complaints = Complaint.objects.all()

        data = {
            "complaints": complaints
        }

        return render(req, "complaint/complaints.html", data)

    raise Http404()


def delete_complaint(req, complaint_id):
    if req.user.is_staff:
        try:
            complaint = Complaint.objects.get(id=complaint_id)
            complaint.delete()
            return HttpResponse()
        except:
            pass

    raise Http404()


class CreateComplaintView(LoginRequiredMixin, CreateView):
    form_class = ComplaintForm
    success_url = "/"
    template_name = "complaint/create_complaint.html"

    def get(self, request, *args, **kwargs):
        try:
            self.kwargs["music"] = Music.objects.get(id=kwargs['music_id'])
            return super().get(request, args, kwargs)
        except:
            raise Http404()

    def get_context_data(self, **kwargs):
        obj = super().get_context_data(**kwargs)

        obj["music"] = self.kwargs["music"]

        return obj

    def form_valid(self, form):
        form.instance.music = Music.objects.get(id=self.kwargs['music_id'])
        form.instance.user = self.request.user
        return super().form_valid(form)

