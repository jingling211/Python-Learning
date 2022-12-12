import requests
import json

from requests.packages import urllib3
urllib3.disable_warnings()

class GPS_API:
    #---baidu---
    def addressToLocationbyBaidu(self, address):
        """
        将地址转换为经纬度
        :param address: 地址
        :return: 经度和维度
        """
        parameters = {
                        'ak': 'xxxx',
                        'address': address,
                        'output' : 'json',
                        'callback' : 'showLocation'
                     }
        try:
            base = 'http://api.map.baidu.com/geocoding/v3/?'
            contest = requests.get(base,parameters)
            data1 = json.loads(contest.text[27:-1])
            location = str(data1['result']['location']['lng']) + ',' + str(data1['result']['location']['lat'])
        except KeyError:
            location = "地址错误，无法查询"
        finally:
            return location
    
    def locationToAddressbyBaidu(self, location):
        return "功能开发中"
        
    #---amap---
    def addressToLocationbyAmap(self, address):
        """
        将地址转换为经纬度
        :param address: 地址
        :return: 经度和维度
        """
        # 在高德地图开发者平台（https://lbs.amap.com/）申请的key，需要替换为自己的key
        parameters = {
                        'key': 'xxxx',
                        'address': address,
                     }
        try:
            base = 'http://restapi.amap.com/v3/geocode/geo?'
            contest = requests.get(base,parameters).json()
            location = contest['geocodes'][0]['location']
        except IndexError:
            location = "地址错误，无法查询"
        finally:
            return location
        
    def locationToAddressbyAmap(self, location):
        """
        将经纬度转换为地址
        所以选用的是逆地理编码的接口
        :param location: 经纬度，格式为 经度+','+维度，例如:location='116.323294,39.893874'
        :return:返回地址所在区，以及详细地址
        """
        parameters = {
                        'location': location,
                        'key': 'xxxx'
                     }
        try:
            base = 'http://restapi.amap.com/v3/geocode/regeo?'
            response = requests.get(base, parameters)
            answer = response.json()  #.encode('gbk','replace')
            address = answer['regeocode']['formatted_address']
        except KeyError:
            return  "坐标错误，无法查询"
        finally:
            #return answer['regeocode']['addressComponent']['district'],answer['regeocode']['formatted_address']
            return address

    #---tencent---
    def addressToLocationbyTENCENT(self, address):
        """
        将地址转换为经纬度
        :param address: 地址
        :return: 经度和维度
        """
        parameters = {
                    'address': address,
                    'key': 'xxxx',
                     }
        try:
            base = 'https://apis.map.qq.com/ws/geocoder/v1/?'
            contest = requests.get(base,parameters,verify=False)
            data1 = json.loads(contest.text)
            locationTENCENT = str(data1['result']['location']['lng'])+','+str(data1['result']['location']['lat'])
            #time.sleep(0.4)
        except KeyError:
            locationTENCENT = "地址错误，无法查询"
        finally:
            return locationTENCENT
        
    def locationToAddressbyTENCENT(self, location):
        return "功能开发中"
