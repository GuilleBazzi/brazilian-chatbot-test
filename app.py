# -*- coding:utf8 -*-
# !/usr/bin/env python
# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = makeWebhookResult(req)

    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def makeWebhookResult(req):
    if req.get("result").get("action") != "shipping.cost":
        return {}
    result = req.get("result")
    parameters = result.get("parameters")
    zone = parameters.get("pf-product")

    cost = {'Europe':100, 'North America':200, 'South America':300, 'Asia':400, 'Africa':500}
    #products = {'Benefix':2022, 'Carduran':309.29, 'Viagra':141, 'Vibramicina ':94}
    products = {'Aldactone':50.38, 'Aldazida':41.33, 'Aromasin':1025.58, 'Benefix':2022.29, 'Carduran':309.49, 'Cartrax Creme':70.06, 'Caverject':102.88, 'Celebra':158.18, 'Champix':983.54, 'Citalor':199.82, 'Dalacin':126.60, 'Depo Provera':12.83, 'Depo-Medrol':18.62, 'Detrusitol':377.06, 'Diabinese':54.84, 'Dostinex':356.28, 'Ecalta':556.90, 'Eliquis':283.52, 'Farlutal':30.04, 'Feldene':28.66, 'Frademicina':20.54, 'Fragmin':211.91, 'Frontal':130.54, 'Genotropin':1702.91, 'Geodon':717.65, 'Inlyta':22327.77, 'Lipitor':343.95, 'Loniten':52.86, 'Lopid':85.34, 'Lyrica':212.22, 'Minidiab':39.19, 'Minipress':53.69, 'Motrin':18.62, 'Neurontin':225.68, 'NIMENRIX':260.31, 'Norvasc':231.53, 'Olmetec':147.44, 'Pletil':23.42, 'Ponstan':29.64, 'Prolift':151.49, 'Propil':26.53, 'Provera':30.84, 'Revatio':3304.13, 'Sermion':124.61, 'Somavert':15646.40, 'Terra-Cortril':18.23, 'Terramicina':35.36, 'Tralen':40.64, 'Trofodermin':56.90, 'Unasyn':2641.26, 'Vfend':1743.55, 'Viagra':141.47, 'Vibramicina':94.10, 'Vyndaqel':25783.42, 'Xalacom':185.16, 'Xalatan':164.81, 'Xalkori':28089.92, 'Xeljanz':4730.77, 'Zitromax':30.97, 'Zoloft':212.14, 'Zoltec':139.07, 'Zyvox':3767.04}
    speech = "O custo do " + zone + " é de " + str(products[zone]) + " reais."

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        #"data": {},
        # "contextOut": [],
        "source": "apiai-brazilian-chatbot"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
