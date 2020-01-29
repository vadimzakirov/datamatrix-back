from .models import Datamatrix, Session
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
import uuid

WEBHOOK_KEY = 'test_key'

class ImageWorker(APIView):

    def get(self, request):
        r = request.GET
        text = r.get('text')
        session_uuid = r.get('session_id')
        last = r.get('last')
        print(str(request))

        if text and session_uuid and (not last):
            s = Session.objects.get(uuid=session_uuid)
            DM = Datamatrix(text=text,session_id=s)
            DM.make_datamatrix()
            return Response({"ok": 'ok'})
        if last:
            s = Session.objects.get(uuid=session_uuid)
            DM = Datamatrix(text=text,session_id=s)
            DM.make_datamatrix()
            DM.make_zipfile()
            return Response({"data": {'session':s.uuid, 'zip': DM.zip_path}})


class SessionGenerator(APIView):

    def get(self,request):
        r = request.GET
        if (r.get('new_session') and (r.get('token') == WEBHOOK_KEY)):
            s = Session()
            s.uuid = str(uuid.uuid4())
            s.save()
            return Response({"session_id": s.uuid})
        else:
            return Response({"error": 'invalid_request'})
