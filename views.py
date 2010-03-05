# -*- coding: UTF8 -*-

from django.contrib.auth.models import User
from django.shortcuts import render_to_response, get_list_or_404
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth import login, authenticate, get_backends

from django.conf import settings

from core.decorators import publish
from django.contrib.auth.decorators import login_required
from apps.django_extjs import utils

@publish
def default(request):
    if request.user.is_authenticated() and request.GET.get('next'):
        return HttpResponseRedirect(request.GET['next'])
    from django.template import RequestContext
    if request.method == 'POST':
        user = request.POST['login']
        apass = request.POST['password']
        user = authenticate(username=user, password=apass)
        if user is not None:
            if user.is_active:
                login(request, user)
                resp = utils.JsonSuccess({'redirect':request.GET.get('next', '/')  })
                resp = utils.set_cookie(resp, 'username', user.username)
                return resp
            else:
                # Return a 'disabled account' error message
                return utils.JsonError(u"Cet utilisateur est desactiv&eacute;")    
        else:
            # Return an 'invalid login' error message.
            return utils.JsonError("Mauvais utilisateur ou mot de passe")  
    params = {}
    params['username'] = utils.get_cookie(request, 'username') or ''
    response = render_to_response('login.html', params, context_instance=RequestContext(request))
    return response


@publish
def logout(request):
    from django.contrib.auth import logout as dlogout
    dlogout(request)
    return HttpResponseRedirect('/')


def user_token(user):
    import hashlib
    salt = settings.SECRET_KEY
    hash = hashlib.md5(user.email + salt).hexdigest()
    return hash
    
@publish
@login_required
def changepassword(request):
    newpass1 = request.POST['new1']
    newpass2 = request.POST['new2']
    current = request.POST['current']
    if request.user.check_password(current):
        if newpass1==newpass2:
            request.user.set_password(newpass1)
            request.user.save()
            if request.user.email:
                try:
                    message = u'Votre mot de passe a été réinitialisé : %s \n\n%s' % (newpass1, settings.HOST) 
                    request.user.email_user('Nouveau mot de passe', message)
                except:
                    pass
            return utils.JsonSuccess()
    return utils.JsonError('Les mots de passe ne correspondent pas')
    
   
   
@publish
def resetpassword(request):
    if request.GET.get('a') and request.GET.get('t'):
        u = User.objects.get(pk = request.GET['a'])
        token = user_token(u)
        if request.GET['t'] == token:
            newpass =  User.objects.make_random_password(length=8)
            u.set_password(newpass)
            u.save()
            message = u'Votre mot de passe LFAweb a été réinitialisé : %s \n\n%s' % (newpass, settings.HOST) 
            u.email_user('Nouveau mot de passe LFAweb', message)
            # auto log user
            backend = get_backends()[0]
            u.backend = "%s.%s" % (backend.__module__, backend.__class__.__name__)
            authenticate(user = u)
            login(request, u)
    return HttpResponseRedirect('/')
    
@publish
def lostpassword(request):
    if request.POST.get('email'):
        try:
            u = User.objects.get(email = request.POST['email'])
            token = user_token(u)
            link = '%s/apps/login/resetpassword?a=%s&t=%s' % (settings.HOST, u.pk, token)
            message = u'Vous avez demandé à réinitialiser votre mot de passe LFAweb.\n\nCliquez ici pour le réinitialiser : %s\n\n%s\n\nOrigine de la demande : %s' % (link, settings.HOST, request.META.get('REMOTE_ADDR', '?'))
            u.email_user('Mot de passe LFAweb', message)
            return utils.JsonSuccess()  
        except:
            return utils.JsonError("Email inconnu")  
    
    return HttpResponseRedirect('/')
