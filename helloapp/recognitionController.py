from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from imageTensorFlow import label_image

from PIL import Image
from io import BytesIO
import json
import base64
import datetime
# Create your views here.
@method_decorator(csrf_exempt, name='dispatch')
class Recogni(TemplateView):

    def post(self, request, **kwargs):
            #Se transforma a guarda el base64 en content           
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)
            content = body['image']

            format, imgstr = content.split(';base64,') 
            ext = format.split('/')[-1] 
            #De otra manera convertir de base64 a imagen
            im = Image.open(BytesIO(base64.b64decode(imgstr))).convert('RGB')
            
            #se guarda el archivo de la imagen
            current_time1 = datetime.datetime.now().strftime("%Y-%m-%d%H-%M-%S")
            im.save("./imageTensorFlow/images/file-"+current_time1+"."+"jpeg", 'JPEG')
            result = label_image.execTensor("./imageTensorFlow/images/file-"+current_time1+"."+"jpeg")
            print(result)

            date_handler = lambda obj: (
                obj.isoformat()
                if isinstance(obj, (datetime.datetime, datetime.date))
                else None
            )

            final_response = {}
            final_response["result"] = result
            return HttpResponse(json.dumps(final_response, default=date_handler, sort_keys=True), "application/json")

            #return JsonResponse(result)