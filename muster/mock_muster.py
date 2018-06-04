from datetime import datetime, timedelta
from requests import post, codes
from time import sleep
from random import randint
from mock_data import MOCKDATA, MOCKUSERS

STEPDELAY = 2
PERSDELAY = 0.25
MOCKTIMEDELAY = 300

GATEWAYURL = "http://startupsges.bd.esri.com:6280/geoevent/rest/receiver/gateway-person-in"
SECTORURL = "http://startupsges.bd.esri.com:6280/geoevent/rest/receiver/sector-person-in"

STRENGTHRANGE = [1,3]

def post_update(json, url):
    req = post(url, json=json)
    if req.status_code < 200 or req.status_code > 299:
        print("Error posting `{0}`".format(json))
        print(req.text)
        return False
    return True

def get_timestamp(step):
    ctime = datetime.utcnow()
    mocktime = ctime + timedelta(seconds=MOCKTIMEDELAY)
    return mocktime.isoformat()

def get_gateway_data(userid, username, deviceid, step, signalstrength=None):
    timestamp = get_timestamp(step)
    signalstrength = signalstrength if signalstrength else randint(STRENGTHRANGE[0], STRENGTHRANGE[1])

    data = {
        "eventtime": timestamp,
        "userid": userid,
        "username": username,
        "deviceid": deviceid,
        "signalstrength": signalstrength
    }
    return data

def get_sector_data(userid, username, sectorid, step):
    timestamp = get_timestamp(step)

    data = {
        "eventtime": timestamp,
        "userid": userid,
        "username": username,
        "sectorid": sectorid
    }
    return data

if __name__ == "__main__":
    print("Streaming")
    count = 0

    uids = list(MOCKUSERS.keys())
    max_iters = max([len(MOCKDATA[uid]) for uid in MOCKDATA.keys()])
    
    for i in range(0, max_iters):
        try:
            for uid in uids:
                if uid not in MOCKDATA or i >= len(MOCKDATA[uid]):
                    continue
                step = MOCKDATA[uid][i]
                username = MOCKUSERS[uid]
                if "sector" in step:
                    sector = step["sector"]
                    data = get_sector_data(uid, username, sector, i)
                    post_update(data, SECTORURL)
                if "device" in step:
                    deviceid = step["device"]
                    data = get_gateway_data(uid, username, deviceid, i)
                    post_update(data, GATEWAYURL)
                sleep(PERSDELAY)
            print(i)
            sleep(STEPDELAY)
        except KeyboardInterrupt:
            break
    
    print("\nSo Long!")

    # while True:
    #     try:


    #         # sector = str(randint(1, 3))
    #         # sector = 2
    #         # data = get_sector_data("1", "Beau Ryck", sector)
    #         # deviceid = str(randint(1, 5))
    #         deviceid = 5
    #         data = get_gateway_data('1', 'Max', deviceid)
    #         post_update(data, GATEWAYURL)
    #         count += 1
    #         print(count)
    #         # sleep(DELAY)
    #     except KeyboardInterrupt:
    #         break
    # print("\nSo Long!")