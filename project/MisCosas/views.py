from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login,logout
from django.utils import timezone

from .forms import LoginForm, RegisterForm, changePhoto
from django.contrib.auth.models import User
from .models import Item,Alimentador, Comentario, Users, Voto
import urllib.request
from xml.sax import make_parser
from xml.sax.handler import ContentHandler
from .ytchannel import YTHandler
from .flickrtag import FlickrHandler

# Create your views here.s
def index(request):
    paginaPrincipal = True
    form = LoginForm()
    print(Users.objects.all())
    print(User.objects.all())
    print(Comentario.objects.all())



    alimentadoresYT = Alimentador.objects.filter(pagPrincipal=True,type="youtube")
    alimentadoresFR = Alimentador.objects.filter(pagPrincipal=True,type="flickr")

    print(alimentadoresYT)
    print(alimentadoresFR)
    print("---------------------ITEMS ORDENADOS-----------------------")
    itemsOrdenados = Item.objects.all().order_by('-votosTotales')[:10]
    print(itemsOrdenados)
    for item in itemsOrdenados:
        print(item.nombre +  ":" + str(item.votosTotales))

    context = {'paginaPrincipal': paginaPrincipal,
                'form': form,
               'alimentadoresYT': alimentadoresYT,
               'alimentadoresFR': alimentadoresFR,
               'top10': itemsOrdenados}

    user = request.user.username
    if user:
        try:
            user = Users.objects.get(username=user)
        except Users.DoesNotExist:
            user = Users(username=user)
            user.save()
        votos = Voto.objects.filter(usuario=user).order_by('-id')[:5]

        print(votos)
        print("--------ITEMS VOTADO POR EL USUARIO-------------")
        context['itemsvotados'] = votos

    if request.method == "POST":
        action = request.POST['action']
        print(action)
        if action == "youtube":
            idchannel = request.POST['idyoutube']
            print(idchannel)
            redireccion = "/MisCosas/youtube/" + idchannel
            return HttpResponseRedirect(redireccion)

        elif action == "flickr":
            idtag = request.POST['idflickr']
            print(idtag)
            redireccion = "/MisCosas/flickr/" + idtag
            return redirect(redireccion)


    if request.method == "GET":
        format = request.GET.get('format')
        if format == 'xml':
            return render(request, 'MisCosas/index.xml', context, content_type='text/xml')
        if format == 'json':
            return render(request, 'MisCosas/index.json', context, content_type='text/json')

    return render(request, 'MisCosas/index.html', context)

def alimentadores(request):
    form=LoginForm
    paginaAlimentadores = True
    try:
        alimentadoresYT = Alimentador.objects.filter(type="youtube")
        alimentadoresFR = Alimentador.objects.filter(type="flickr")
        print("-----------ALIMENTADORES DE YOUTUBE--------------")
        print(alimentadoresYT)
        print("-----------ALIMENTADORES DE FLICKR--------------")
        print(alimentadoresFR)
        for alimentadores in alimentadoresYT:
            print(alimentadores.item_set.count())
        context = {'alimentadoryoutube': alimentadoresYT,
                   'alimentadoresflickr':alimentadoresFR,
                   'paginaAlimentadores':paginaAlimentadores,
                   'form': form}
                   #'items': totItems}

    except Alimentador.DoesNotExist:
        print("no alimentadores")
        context = {}

    return render(request,'MisCosas/alimentadores.html',context)

def borrarprincipal(request, llave, llave1,llave2 ):
    a = Alimentador.objects.get(alimentadorId=llave1)
    a.pagPrincipal = not a.pagPrincipal
    a.save()
    if llave2 == "paginaPrincipal":
        redireccion = "/MisCosas/"
    elif llave2  == "paginaAlimentador":
        redireccion = "/MisCosas/"+ llave + "/" +llave1

    return redirect(redireccion)

def processalimentador(request, llave1, llave2):
    if llave1 == 'youtube':
        Parser = make_parser()
        Parser.setContentHandler(YTHandler())
        url = 'https://www.youtube.com/feeds/videos.xml?channel_id=' \
              + llave2

    if llave1 == 'flickr':
        Parser = make_parser()
        Parser.setContentHandler(FlickrHandler())
        url = 'https://www.flickr.com/services/feeds/photos_public.gne?tags=' \
              + llave2

    xmlStream = urllib.request.urlopen(url)
    Parser.parse(xmlStream)
    a = Alimentador.objects.get(alimentadorId=llave2)
    items = Item.objects.filter(alimentador__alimentadorId=llave2)

    for item in items:
        item.votosTotales = item.votosPositivos - item.votosNegativos
        print(item.votosTotales)
        item.save()

    form= LoginForm();
    context = {'contentList': items,
               'alimentador': a,
               'form':form}

    return render(request, 'MisCosas/alimentador.html', context)

def processitem(request, llave,llave1, llave2):
    a = Alimentador.objects.get(alimentadorId=llave1)
    i= Item.objects.get(itemId=llave2)
    ##items = Item.objects.filter(alimentador__alimentadorId = llave1)
    items = Item.objects.filter(alimentador=a)
    form = LoginForm()

    context = {'alimentador': a,
               'item': i,
               'form': form}

    user = request.user.username
    if user:
        user = Users.objects.get(username=user)
        context['users'] = user
        if request.method == "POST":
            action = request.POST['action']
            if action == 'comment':
                newComment = request.POST['commentsection']
                c = Comentario(usuario=user, fecha=timezone.now(), cuerpo=newComment, item=i)
                c.save()
        try:
            voto = Voto.objects.get(usuario=user, item=i)
            context['voto'] = voto
            print(voto.estado)
        except Voto.DoesNotExist:
            print("no votes")

    print(items)
    print(a)
    print(i)

    try:
        comments = Comentario.objects.filter(item__itemId=llave2)
        context['comment'] = comments
    except Comentario.DoesNotExist:
        print("No Comments")

    return render(request, 'MisCosas/item.html',context)

def gestionvotos(request,llave, llave1,llave2,llave3):

    i = Item.objects.get(itemId=llave2)
    print(i)
    name = request.user.username
    if name:
        action = request.POST.get('action', None)
        u = Users.objects.get(username=name)
        itemuser = u.itemsvotados.filter(itemId=i.itemId)

        print("HAS VOTADO ESTA PAGINA ANTES :")
        print(itemuser.exists())
        if itemuser.exists() == False:
            print("HE ENTRAAAAAAADOOOOOOO")
            u.estadoVoto = ""
            u.save()
        print("HE HECHO UN VOTO" + action)
        print("MI ESTADO DEL VOTO AL EMPEZAR" + u.estadoVoto)
        if action == "votopositivo":
            if itemuser.exists():
                if u.estadoVoto == "estadonegativo":
                    i.votosPositivos = i.votosPositivos +1
                    i.votosNegativos = i.votosNegativos - 1
                    i.save()
                v = Voto.objects.get(usuario=u, item=i)
                v.estado = "estadopositivo"
                v.save()
            else:
                i.votosPositivos = i.votosPositivos + 1
                i.save()
                u.itemsvotados.add(i)
                v = Voto(usuario=u, item=i, estado="estadopositivo")
                v.save()
            u.estadoVoto = "estadopositivo"
            u.save()

        elif action =="votonegativo":
            if itemuser.exists():
                print("USUARIO EXISTE")
                print("EL ESTADO DEL VOTO en ESte " + u.estadoVoto)
                if u.estadoVoto == "estadopositivo":
                    print("USUARIO HABIA VOTADO POSITIVAMENTE")
                    i.votosPositivos = i.votosPositivos - 1
                    i.votosNegativos = i.votosNegativos + 1
                    i.save()
                print("USUARIO EXISTENTE HA VOTADO NEGATIVO")
                v = Voto.objects.get(usuario=u, item=i)
                v.estado = "estadonegativo"
                v.save()
            else:
                print("USUARIO NO EXISTE")
                i.votosNegativos = i.votosNegativos + 1
                i.save()
                u.itemsvotados.add(i)
                v = Voto(usuario=u, item=i, estado="estadonegativo")
                v.save()

            u.estadoVoto = "estadonegativo"
            u.save()
            v.estado = u.estadoVoto
            v.save()

        print("VOTO CREADO PARA ESTE USUARIO")
        voto = Voto.objects.get(usuario=u, item=i)
        print(voto.estado)

        print("EL ESTADO DEL VOTO AL TERMINAR ES " + u.estadoVoto)
        print("Videos votados por" + u.username)
        print(u.itemsvotados.all())

        a = Alimentador.objects.get(alimentadorId=llave1)
        items = Item.objects.filter(alimentador=a)
        votospos = 0
        votosne = 0
        for votos in items:
            print(votos.nombre +  ":" + str(votos.votosPositivos))
            votospos = votos.votosPositivos + votospos
            votosne = votos.votosNegativos + votosne

        print(votospos)
        print(votosne)

        puntuacionAlimentador = votospos - votosne
        a.puntuacion = puntuacionAlimentador
        a.save()
    #AQUI NO METO HTTP_REFERER POR QUE ME DA FALLO AL HACER LOS TEST
    if llave3 == 'paginaPrincipal':
        redireccion = "/MisCosas/"
    elif llave3 == 'paginaItem':
        redireccion  = "/MisCosas" + "/" + llave + "/" + llave1 + "/" + llave2

    return redirect(redireccion)

def users(request):
    paginaUsuarios = True
    form = LoginForm()
    users = Users.objects.all()

    context = {'users':users,
               'paginaUsuarios':paginaUsuarios,
               'form': form}
    return render(request,'MisCosas/users.html', context)


def user(request, llave):
    users = Users.objects.get(username = llave)
    ##No se si esto habra que arreglarlo cuando borre base de datos
    itemsComentados = Comentario.objects.filter(usuario = users)
    itemsVotados = Voto.objects.filter(usuario=users)
    for item in itemsComentados:
        print(item.item)
    form = LoginForm()
    form2 = changePhoto()
    context = {'users': users,
               'form': form,
               'itemscomentados': itemsComentados,
                'itemsvotados': itemsVotados,
               'form2':form2}
    print(users)
    print(request.user.username)
    if users.username == request.user.username:
        sameuser = True
        context['sameuser'] = sameuser

    if request.method == "POST":
        if 'tamañoletra' in request.POST:
            tamañoletra= request.POST['tamañoletra']

            if tamañoletra == "grande":
                letra = "2rem";
            elif tamañoletra == "mediana":
                letra = "1rem";
            elif  tamañoletra == "pequeña":
                letra = "0.5rem"

            users.tamañoletra = letra

        elif 'estilo' in request.POST:
            estilo = request.POST['estilo']
            print(estilo)
            if estilo == "Oscuro":
                fondo = "black"
            elif estilo == "Ligero":
                fondo = "white"

            users.estilo = fondo

        else:
            print("entro en cambiar foto")
            form2 = changePhoto(request.POST, request.FILES)
            if form2.is_valid():
                image = form2.cleaned_data['image']
                users.image = image

        users.save()

    print(users.tamañoletra)
    return render(request, 'MisCosas/perfil.html', context)


def register(request):
    form = RegisterForm()
    context = {'form': form}
    if request.method == "POST":
        print("entro al post")
        form = RegisterForm(request.POST,request.FILES)
        if form.is_valid():
            print("entro en formulario")
            nombre = form.cleaned_data['Username']
            email = form.cleaned_data['Email']
            contraseña = form.cleaned_data['Password']
            image = form.cleaned_data['image']
            try:
                superUser = User.objects.get(username=nombre)
                context['error'] = 'Usuario existente, pruebe otro'
                return render(request, 'MisCosas/register.html', context)
            except User.DoesNotExist:
                try:
                    user = Users.objects.get(username=nombre)
                    context['error'] = 'Usuario existente, pruebe otro'
                    return render(request, 'MisCosas/register.html', context)
                except Users.DoesNotExist:
                    u = Users(username=nombre, email=email, password=contraseña,image = image)
                    u.save()
                    user = User.objects.create_user(username=nombre, email=email, password=contraseña)
                    user.save()
                    if user is not None:
                        login(request,user)
                    return redirect('index')

    return render(request, 'MisCosas/register.html', context)

def login_view(request):
    if request.method == "POST":
        print("entro en post login")
        form = LoginForm(request.POST)
        if form.is_valid():
            print("entro en form valid")
            nombre = form.cleaned_data['Username']
            contraseña = form.cleaned_data['Password']
            user = authenticate(request, username=nombre, password=contraseña)
            if user is not None:
                """u = Users.objects.get(username=nombre)
                context = {'user' : u}"""
                login(request, user)
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return  HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def logout_view(request):
    logout(request)
    return redirect(request.META.get('HTTP_REFERER'))

def css(request):
    context = {}
    try:
        users = Users.objects.get(username=request.user.username)
        context['users'] = users
    except Users.DoesNotExist:
        print("")

    return render(request, 'MisCosas/base.css', context, content_type='text/css')


