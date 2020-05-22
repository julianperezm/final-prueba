#!/usr/bin/python3

from xml.sax.handler import ContentHandler

class FlickrHandler(ContentHandler):

    def __init__(self):
        self.inEntry = False  # Para saber si estamos dentro de entry
        self.inTitle = False
        self.inLink = False
        self.inContent = False  # Si tenemos contenido que queremos leer
        self.content = ""
        self.alimentador= ""
        self.tituloAlimentador = ""
        self.enlaceAlimentador = ""
        self.alimentadorId = ""
        self.tituloItem = ""
        self.enlaceItem =""
        self.itemId = ""
        self.fotoItem = ""

    def startElement(self, name, attrs):
        if name == 'entry':
            self.inEntry = True

        elif self.inEntry:
            if name == 'title':
                self.inContent = True

            if name == 'link':
                a = attrs.get('rel')
                if a == 'alternate':
                    self.enlaceItem = attrs.get('href')
                    print(self.enlaceItem)
                elif a == 'enclosure':
                    self.fotoItem = attrs.get('href')
                    print(self.fotoItem)

            if name == 'id':
                self.inContent = True

        elif self.inEntry == False:
            if name == 'link':
                a = attrs.get('rel')
                if a == 'self':
                    self.tituloAlimentador = attrs.get('href')
                    self.tituloAlimentador = self.tituloAlimentador.split('=')[-1]
                    print(self.tituloAlimentador)
                if a == 'alternate':
                    self.enlaceAlimentador = attrs.get('href')
                    print(self.enlaceAlimentador)


    def endElement(self, name):
        if name == 'entry':
            from .models import Item, Alimentador
            self.inEntry = False

            if self.alimentador == "":
                try:
                    a = Alimentador.objects.get(alimentadorId=self.tituloAlimentador, nombre=self.tituloAlimentador,
                                                enlace=self.enlaceAlimentador, type="flickr")
                    print("Alimentador que ya teniamos")
                    print(a.nombre)
                except Alimentador.DoesNotExist:
                    a = Alimentador(alimentadorId=self.tituloAlimentador, nombre=self.tituloAlimentador,
                                    enlace=self.enlaceAlimentador, type="flickr")
                    print("alimentador nuevo")
                    a.save()

                self.alimentador = a

            try:
                i = Item.objects.get(nombre=self.tituloItem, enlace=self.enlaceItem, itemId=self.itemId,
                                     fotoItem=self.fotoItem, alimentador=self.alimentador)
                print("item que ya teniamos")
                print(i.nombre)
            except Item.DoesNotExist:
                newItem = Item(nombre=self.tituloItem, enlace=self.enlaceItem, itemId=self.itemId,
                               fotoItem=self.fotoItem, alimentador=self.alimentador)
                print("item nuevo")
                newItem.save()

        elif self.inEntry:
            if name == 'title':
                self.tituloItem =  self.content
                self.content = ""
                self.inContent = False
                print(self.tituloItem)

            if name == 'id':
                self.itemId = self.content
                print(self.itemId)
                self.itemId = self.itemId.split("/")[-1]
                print(self.itemId)
                self.content = ""
                self.inContent = False

    def characters(self, chars):
        if self.inContent:
            self.content = self.content + chars
