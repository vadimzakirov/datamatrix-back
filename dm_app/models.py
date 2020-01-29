# coding utf-8
from bs4 import BeautifulSoup
from django.db import models
import subprocess as sp
import shutil
import requests
import uuid
import os


class Datamatrix(models.Model):
    text = models.CharField(max_length=100, default='unknown')
    image_path = models.CharField(max_length=100, default='data/images/')
    zip_path = models.CharField(max_length=100, default='data/zips/')
    session_id = models.ForeignKey('Session', on_delete=models.CASCADE)

    def make_datamatrix(self):
        payload = {
        'barcode_text':self.text,
        'barcode_type':'dmtx',
        'barcode_size':1 ,
        'barcode_module':'s',
        'barcode_density':0.8
        }
        post_response = requests.post('https://ecoprint.spb.ru/barcode/make-datamatrix.php',data=payload)
        soup = BeautifulSoup(post_response.text, 'lxml')
        img_tag = soup.find_all('img')
        src = str(img_tag[0]['src'])
        all_dm = Datamatrix.objects.count()
        self.image_path += f'{self.session_id}_{all_dm+1}.gif'
        with open(self.image_path,'wb') as target:
            a = requests.get('https://ecoprint.spb.ru/barcode/' + src )
            target.write(a.content)
        self.save()

    def make_zipfile(self):
        session_dms = Datamatrix.objects.filter(session_id = self.session_id)
        self.zip_path += f'{self.session_id}.zip'
        for dm in session_dms:
            call = ['zip', self.zip_path, dm.image_path]
            sp.call(call)
        self.save()
        shutil.rmtree('data/images')
        os.makedirs('data/images')

class Session(models.Model):
    uuid = models.CharField(max_length=100, default='unknown')

    def __str__(self):
        return self.uuid
