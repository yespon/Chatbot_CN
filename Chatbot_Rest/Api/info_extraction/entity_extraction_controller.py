#-*- coding:utf-8 _*-  
""" 
@author:charlesXu
@file: entity_extraction_controller.py 
@desc: 实体抽取控制器
@time: 2019/05/15 
"""

import json
import logging
import datetime

from django.http import JsonResponse
from Chatbot_Model.Entity_extraction.NER_main import NER
from Chatbot_Rest.Api.util import LogUtils2

logger = logging.getLogger(__name__)

ner = NER()

def entity_ext_controller(request):
    '''
    实体抽取接口
    :param request:
    :return:
    '''
    if request.method == 'POST':
        jsonData = json.loads(request.body.decode('utf-8'))
        try:
            msg = jsonData["msg"]

            # res = ner.evaluate_line(msg)
            res = ner.interface(msg)
            localtime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            dic = {
                "desc": "Success",
                "ques": msg,
                "res": res,
                "time": localtime,
            }
            log_res = json.dumps(dic, ensure_ascii=False)
            logger.info(log_res)
            return JsonResponse(dic)
        except Exception as e:
            logger.info(e)
            print(e)
    else:
        return JsonResponse({"desc": "Bad request"}, status=400)


