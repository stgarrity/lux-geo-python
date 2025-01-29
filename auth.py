import asyncio
import json

import aiohttp
import pkce

async def login(username, password):
    cv, cc = pkce.generate_pkce_pair()

    # TODO factor these out?
    client_id = "b335ca43-3bde-4406-b281-8816afb7cc91"
    redirect_uri = "connecteddevicesjci.luxmobile://connecteddevicesjci/path"

    scope = "https://connecteddevicesjci.onmicrosoft.com/mobile/user_impersonation https://connecteddevicesjci.onmicrosoft.com/mobile/read_write offline_access openid"

    # FIXME nonce should be random
    url = "https://connecteddevicesjci.b2clogin.com/te/connecteddevicesjci.onmicrosoft.com/B2C_1A_SignIn/oauth2/v2.0/authorize?" + \
			"nonce=FZ7xNNW3u6Gy-LMCrtntZ0yveaUvYRUtVRPPk9gneKM" + \
			"&audience=https://connecteddevicesjci.onmicrosoft.com" + \
			f"&scope={scope}" + \
			f"&response_type=code&client_id={client_id}" + \
			f"&code_challenge={cc}" + \
			f"&code_challenge_method=S256&redirect_uri={redirect_uri}" +\
            "&state=4rwh1Bs9s6OtdGfH0OWww_Y7qDfkdfxiOxRO8hpflFI" # FIXME state should be random

    res = ""
    cookies = []
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            res = await response.text()
            cookies = response.cookies
            csrf = response.headers.get("X-Csrf-Token")
            print("got first response")

    csrf = str(cookies.get("x-ms-cpim-csrf")).split("Set-Cookie: x-ms-cpim-csrf=")[-1].split(";")[0]

    cookie_dict = {}
    for k in cookies:
        cookie_dict[k] = str(cookies.get(k)).split("=", 1)[-1].split(";")[0].strip('"')

    try:
        split_result = res.split('"transId":"StateProperties=')
        if len(split_result) < 2:
            print("Error: Could not find StateProperties in response: ", split_result)
            return
        StateProperties = split_result[1].split('"')[0]
    except IndexError:
        print("Error: Malformed response when trying to extract StateProperties")
        return

    cookies = []
    async with aiohttp.ClientSession() as session:
        url2 = f"https://connecteddevicesjci.b2clogin.com/connecteddevicesjci.onmicrosoft.com/B2C_1A_SignIn/SelfAsserted?tx=StateProperties={StateProperties}&p=B2C_1A_SignIn"
        data = {"request_type": "RESPONSE", "logonIdentifier": username,"password": password}
        headers = {"Referer": url, "X-Csrf-Token": csrf}
        # The cookie values are being wrapped in quotes by aiohttp's cookie handling
        # We can pass the raw cookie string in the headers instead
        cookie_str = "; ".join(f"{k}={v}" for k,v in cookie_dict.items())
        headers["Cookie"] = cookie_str
        async with session.post(url2, data=data, headers=headers) as response:
            res = await response.text()
            cookies = response.cookies
            print("got second response")

    for k in cookies:
        cookie_dict[k] = str(cookies.get(k)).split("=", 1)[-1].split(";")[0].strip('"')

    redirect_url = ""
    async with aiohttp.ClientSession() as session:
        url3 = f"https://connecteddevicesjci.b2clogin.com/connecteddevicesjci.onmicrosoft.com/B2C_1A_SignIn/api/CombinedSigninAndSignup/confirmed?csrf_token={csrf}&tx=StateProperties={StateProperties}&p=B2C_1A_SignIn"
        headers = {"Referer": url3, "X-Csrf-Token": csrf}
        # The cookie values are being wrapped in quotes by aiohttp's cookie handling
        # We can pass the raw cookie string in the headers instead
        cookie_str = "; ".join(f"{k}={v}" for k,v in cookie_dict.items())
        headers["Cookie"] = cookie_str
        try:
            async with session.get(url3, headers=headers) as response:
                print(await response.text())
        except aiohttp.client_exceptions.NonHttpUrlRedirectClientError as e:
           print("got third response / redirect")
           redirect_url = str(e).split("Location: ")[-1].split()[0]

    code = ""
    if "code=" in redirect_url:
        code = redirect_url.split("code=")[1]
        if "&" in code:
            code = code.split("&")[0]

    async with aiohttp.ClientSession() as session:
        url4 = "https://connecteddevicesjci.b2clogin.com/te/connecteddevicesjci.onmicrosoft.com/B2C_1A_SignIn/oauth2/v2.0/token"
        data = {"client_id": client_id, "scope": scope, "code": code, "redirect_uri": redirect_uri, "grant_type": "authorization_code", "code_verifier": cv}
        async with session.post(url4, data=data) as response:
            res = await response.text()
            j = json.loads(res)
            print(j)
            return j


if __name__ == "__main__":
    import os
    import dotenv
    dotenv.load_dotenv()

    asyncio.run(login(os.getenv("USERNAME"), os.getenv("PASSWORD")))
