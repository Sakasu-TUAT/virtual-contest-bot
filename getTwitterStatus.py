#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Twitter Rate Limit 情報取得サンプル"""

import os
import sys
import json
from base64 import b64encode
import datetime
import time
import re
import argparse

#!pip install requests
import requests
#!pip install requests_oauthlib
from requests_oauthlib import OAuth1Session


USER_AGENT = "Get Twitter Staus Application/1.0"
TOKEN_ENDPOINT = 'https://api.twitter.com/oauth2/token'
STATUS_ENDPOINT = 'https://api.twitter.com/1.1/application/rate_limit_status.json'


def epoch2datetime(epoch):
    """エポックタイム (UNIX タイム) を datetime (localtime) へ変換"""
    return datetime.datetime(*(time.localtime(epoch)[:6]))


def datetime2epoch(d_utc):
    """datetime (UTC) をエポックタイム (UNIX タイム)へ変換"""
    #UTC を localtime へ変換
    date_localtime = \
        d_utc.replace(tzinfo=datetime.tzinfo.tz.tzutc()).astimezone(datetime.tzinfo.tz.tzlocal())
    return int(time.mktime(date_localtime.timetuple()))


def get_delta(target_epoch_time):
    """target_epoch_time と現在時刻の差分を返す"""
    return target_epoch_time - int(round(time.time(), 0))


class GetTweetStatus:
    """Twitter API の limit status を取得するクラス"""
    def __init__(self, apikey, apisec, access_token="", access_secret=""):
        self._apikey = apikey
        self._apisec = apisec
        self._access_token = access_token
        self._access_secret = access_secret
        self._access_token_mask = re.compile(r'(?P<access_token>"access_token":)\s*".*"')

    def _get_bearer(self):
        """Bearer を取得"""
        cred = self._get_credential()
        headers = {
            'Authorization': 'Basic ' + cred,
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
            'User-Agent': USER_AGENT
            }
        data = {
            'grant_type': 'client_credentials',
            }

        try:
            res = requests.post(TOKEN_ENDPOINT, data=data, headers=headers, timeout=5.0)
            res.raise_for_status()
        except (TimeoutError, requests.ConnectionError):
            raise Exception("Cannot get Bearer")
        except requests.exceptions.HTTPError:
            if res.status_code == 403:
                raise requests.exceptions.HTTPError("Auth Error")
            raise requests.exceptions.HTTPError("Other Exception")
        except Exception:
            raise Exception("Cannot get Bearer")
        rjson = res.json()
        return rjson['access_token']

    def _get_credential(self):
        """Credential の生成"""
        pair = self._apikey + ':' + self._apisec
        bcred = b64encode(pair.encode('utf-8'))
        return bcred.decode()


    def get_limit_status_v2(self, resource_family="search"):
        """OAuth v2.0 (Bearer) を使用したステータスの取得"""
        bearer = self._get_bearer() # Bearer の取得

        headers = {
            'Authorization':'Bearer {}'.format(bearer),
            'User-Agent': USER_AGENT
        }
        params = {
            'resources': resource_family  # help, users, search, statuses etc.
        }

        try:
            res = requests.get(STATUS_ENDPOINT, headers=headers, params=params, timeout=5.0)
            res.raise_for_status()
        except (TimeoutError, requests.ConnectionError):
            raise requests.ConnectionError("Cannot get Limit Status")
        except Exception:
            raise Exception("Cannot get Limit Status")
        return res.json()

    def get_limit_status_v1(self, resource_family="search"):
        """OAuth v1.1 を使用したステータスの取得"""

        # OAuth は複雑なので OAuth1Session を利用する
        oauth1 = OAuth1Session(self._apikey, self._apisec, self._access_token, self._access_secret)

        params = {
            'resources': resource_family  # help, users, search, statuses etc.
        }

        try:
            res = oauth1.get(STATUS_ENDPOINT, params=params, timeout=5.0)
            res.raise_for_status()
        except (TimeoutError, requests.ConnectionError):
            raise requests.ConnectionError("Cannot get Limit Status")
        except Exception:
            raise Exception("Cannot get Limit Status")
        return res.json()


    def disp_limit_status(self, version=2, resource_family="search"):
        """バージョンに分けて Rate Limit を表示する"""
        if version == 2:
            resj = self.get_limit_status_v2(resource_family=resource_family)
        elif version == 1:
            resj = self.get_limit_status_v1(resource_family=resource_family)
        else:
            raise Exception("Version error: {version}")

        # JSON の表示
        print(self._access_token_mask.sub(r'\g<access_token> "*******************"',
                                          json.dumps(resj, indent=2, ensure_ascii=False)))
        # 分解表示(remain/reset の取得例)
        print("resources:")
        if 'resources' in resj:
            resources = resj['resources']
            for family in resources:
                print(f"  family: {family}")
                endpoints = resources[family]
                for endpoint in endpoints:
                    items = endpoints[endpoint]
                    print(f"    endpoint: {endpoint}")
                    limit = items['limit']
                    remaining = items['remaining']
                    reset = items['reset']
                    e2d = epoch2datetime(reset)
                    duration = get_delta(reset)
                    print(f"      limit: {limit}")
                    print(f"      remaining: {remaining}")
                    print(f"      reset: {reset}")
                    print(f"      reset(epoch2datetime): {e2d}")
                    print(f"      duration: {duration} sec")
        else:
            print("  Not Available")


def main():
    """main()"""
    # API_KEY, API_SEC 等環境変数の確認
    apikey = os.getenv('TWITTER_API_KEY', default="")
    apisec = os.getenv('TWITTER_API_SECRET', default="")
    access_token = os.getenv('ACCESS_TOKEN', default="")
    access_secret = os.getenv('ACCESS_TOKEN_SECRET', default="")

    if apikey == "" or apisec == "":    # 環境変数が取得できない場合
        print("環境変数 API_KEY と API_SEC を設定してください。", file=sys.stderr)
        print("OAuth v1.1 を使用する場合には環境変数 ACCESS_TOKEN と ACCESS_SECRET も設定してください。",
              file=sys.stderr)
        sys.exit(255)

    # 引数の設定
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--oauthversion', type=int, default=0,
                        metavar='N', choices=(0, 1, 2),
                        help=u'OAuth のバージョン指定 [1|2]')
    parser.add_argument('-f', '--family', type=str, default='search',
                        metavar='Family',
                        help=u'API ファミリの指定。複数の場合はカンマ区切り')

    args = parser.parse_args()
    oauthversion = args.oauthversion
    family = args.family

    # GetTweetStatus オブジェクトの取得
    gts = GetTweetStatus(apikey, apisec, access_token=access_token, access_secret=access_secret)

    # User Auth (OAuth v1.1) による Rate Limit 取得と表示
    if (oauthversion in (0, 1)) and (access_token != "" and access_secret != ""):
        print("<<user auth (OAuth v1)>>")
        gts.disp_limit_status(version=1, resource_family=family)

    # App Auth (OAuth v2.0) による Rate Limit 取得と表示
    if oauthversion in (0, 2):
        print("<<app auth (OAuth v2)>>")
        gts.disp_limit_status(version=2, resource_family=family)

if __name__ == "__main__":
    main()