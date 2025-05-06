 # Copyright 2025 Beijing Volcano Engine Technology Ltd.
 # SPDX-License-Identifier: Apache-2.0
import os
from volcengine.vod.VodService import VodService

if __name__ == '__main__':
    vod_service = VodService(region='cn-north-1')

    # call below method if you dont set ak and sk in $HOME/.vcloud/config
    vod_service.set_ak(os.getenv("VOLCENGINE_ACCESS_KEY"))
    vod_service.set_sk(os.getenv("VOLCENGINE_SECRET_KEY"))
    # then call specific action
