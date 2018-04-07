from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template import RequestContext
from django.template.context_processors import csrf
from reference_books.models import Event
from report.views import logging_event
from sim.forms import get_new_simcard
from sim.models import OpSoS_card, UseTypeSIM
from django.contrib.auth.decorators import login_required


def clean_phone(phone):
    phone_clean = phone.replace(' ', '')
    phone_clean = phone_clean.replace('(', '')
    phone_clean = phone_clean.replace(')', '')
    phone_clean = phone_clean.replace('-', '')
    phone_clean = phone_clean.replace('+7', '')
    return phone_clean

def clean_iccsim(icc_sim):
    return icc_sim.replace(' ', '')


@login_required
def get_simcard_list(request,status='active'):
    args = {}
    if status == 'active':
        args['simcards'] = OpSoS_card.objects.filter(Status=True).order_by('id')
    else:
        args['simcards'] = OpSoS_card.objects.filter(Status=False).order_by('id')

    args['status'] = status
    return render(request, 'simcard_list.html', args)


@login_required
def get_new_simcard_item(request, simcard_id=None):
    args = {}
    args.update(csrf(request))
    form = get_new_simcard(request.POST or None, instance=simcard_id and OpSoS_card.objects.get(id=simcard_id))

    if request.method == 'POST' and form.is_valid():
        status_checkbox = request.POST.get('Status', False)
        usetype_slug = UseTypeSIM.objects.get(id=str(request.POST['Use_type'])).slug

        if simcard_id != None:
            old_data = OpSoS_card.objects.get(id=simcard_id)

            if status_checkbox != 'on':
                logging_event(Event.objects.get(slug='change_status'), request.user, old_data.Status, 'sim')

            if old_data.Notation != request.POST['Notation']:
                logging_event(Event.objects.get(slug='change_notation'), request.user, old_data.Notation, 'sim')

            if usetype_slug=='usesim_object':
                if old_data.Use_nameobject != request.POST['Use_nameobject']:
                    logging_event(Event.objects.get(slug='change_use_nameobject'), request.user, old_data.Use_nameobject, 'sim')
                if old_data.Use_numberobject != request.POST['Use_numberobject']:
                    logging_event(Event.objects.get(slug='change_use_numberobject'), request.user, old_data.Use_numberobject, 'sim')
                if old_data.Use_addressobject != request.POST['Use_addressobject']:
                    logging_event(Event.objects.get(slug='change_use_addressobject'), request.user, old_data.Use_addressobject, 'sim')
            else:
                if old_data.Use_user != request.POST['Use_user']:
                    logging_event(Event.objects.get(slug='change_use_user'), request.user, old_data.Use_user, 'sim')

        else:
            logging_event(Event.objects.get(slug='add_simcard'), request.user, '','sim')

        item = form.save(commit=False)
        if simcard_id==None:
            if request.POST['Number_SIM']:
                item.Number_SIM = clean_phone(request.POST['Number_SIM'])
            if request.POST['ICC_SIM']:
                item.ICC_SIM = clean_iccsim(request.POST['ICC_SIM'])
            item.Create_user = request.user.id
        else:
            item.Update_user = request.user.id
        item.save()
        return HttpResponseRedirect(reverse('simmanage:getlist_simcard', args=['active']))

    else:
        args['form'] = form
        if simcard_id:
            args['simcard_data'] = OpSoS_card.objects.get(id=simcard_id)

        return render(request, 'simcard_item.html', args)