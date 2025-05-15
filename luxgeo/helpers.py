import aiohttp
from typing import Optional, Dict, Any, Tuple

async def http_request(
    method: str,
    url: str,
    headers: Optional[Dict[str, str]] = None,
    data: Optional[Any] = None,
    json_data: Optional[Any] = None,
    allow_redirects: bool = True,
    **kwargs
) -> Tuple[str, Dict[str, str], aiohttp.ClientResponse]:
    """
    Make an HTTP request using aiohttp and return (response_text, cookies, response_obj).
    """
    async with aiohttp.ClientSession() as session:
        req_func = getattr(session, method.lower())
        try:
            async with req_func(
                url,
                headers=headers,
                data=data,
                json=json_data,
                allow_redirects=allow_redirects,
                **kwargs
            ) as response:
                text = await response.text()
                cookies = {k: v.value for k, v in response.cookies.items()}
                return text, cookies, response
        except Exception as e:
            # Optionally log or handle exceptions here
            raise