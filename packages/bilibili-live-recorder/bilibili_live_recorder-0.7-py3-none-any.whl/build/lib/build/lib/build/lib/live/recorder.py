import http.client as client
import asyncio
import aiohttp
import os
import time
from yarl import URL

from live.log import log
from live.utils import header
from live.param import Api
from live.utils import naming

class Rec:
    def __init__(self, url, name, sdir):
        self.url = url
        self.name = name
        self.file_name = naming(sdir, name, 'flv')
        self.size = 0
        self.break_warning = 0
        self.rec_on = False
    
    async def record(self):
        h = header(self.url)
        async with aiohttp.ClientSession() as s:
            ret = await self._get(session=s, url=self.url, headers=h)
            if ret['err']:
                log.info(f'record error, status {ret["status"]}')
            else:
                log.info("Record ended")
            return
    
    async def _get(self, session, url, headers):
        async with session.get(url, headers=headers) as res:
            code = res.status
            ret = {'err': False, 'status': code}
            if code == 475:
                ret['err'] = True

            elif code == 302:
                loc = res.headers['Location']
                ret['new_url'] = loc
                log.info('Redirecting...')
                r = await self._get(session, url=loc, headers=headers)
                if r['err']:
                    ret['err'] = True

            elif code == 200:
                log.info(f'Start to record from url [{url}]')
                self.break_warning = 0
                ff = open(self.file_name, 'wb')
                while chunk := await res.content.read(2048):
                    ff.write(chunk)
                    self.rec_on = True
                ff.close()
                self.rec_on = False

            else:
                log.error(f'unknown error, status {code}')
                ret['err'] = True

            return ret

    async def rec_stat(self):
        while self.break_warning < 2:
            await asyncio.sleep(1)
            if not self.rec_on:
                self.break_warning += 1
                continue
            
            sz = os.stat(self.file_name).st_size / 1024
            if self.size == sz:
                self.break_warning += 1
                continue
            dif = sz - self.size
            print(f'[{self.name}], size: {round(sz/1024, 2):>8}Mb, speed: {round(dif, 2):>9} kb/s', end='\r')

            self.size = sz
            self.break_warning = 0
