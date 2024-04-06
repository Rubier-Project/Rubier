import httpx
import rubier.servers as servers

class Httpz(object):
    def __init__(self, __Auth: str):
        self.auth = __Auth

    def poolConnection(self, inputData: dict = {}, method: str = None):
        while 1:
            try:
                data = {
                    "api_version": "0",
                    "auth": self.auth,
                    "client":{
                        "app_name": "Main",
                        "app_version": "3.0.2",
                        "lang_code": "fa",
                        "package":"app.rbmain.a",
                        "platform": "Android"

                    },
                    "data": inputData,
                    "method": method
                }
                return httpx.Client().post(servers.RubinoApi.getApi(), json=data).json()

            except KeyboardInterrupt:
                break

            except Exception as ER:
                return {"error": str(ER)}

class AsyncHttpz(object):
    def __init__(self, __Auth: str):
        self.auth = __Auth

    async def poolConnection(self, inputData: dict = {}, method: str = None):
        while 1:
            try:
                data = {
                    "api_version": "0",
                    "auth": self.auth,
                    "client":{
                        "app_name": "Main",
                        "app_version": "3.0.2",
                        "lang_code": "fa",
                        "package":"app.rbmain.a",
                        "platform": "Android"

                    },
                    "data": inputData,
                    "method": method
                }

                async with httpx.AsyncClient() as client:
                    dt = await client.post(servers.RubinoApi.getApi(), json=data)
                    return dt.json()

            except KeyboardInterrupt:
                break