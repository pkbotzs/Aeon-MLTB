from aiohttp import web
import pyrogram
from config import (
    BOT_UNAME,
    SHORTLINK_URL1,
    SHORTLINK_API1,
    SHORTLINK_URL2,
    SHORTLINK_API2,
    CHANNEL_ID,
    URL,
    IS_VERIFY,
    STREAM_SHORT
)
from helper_func import get_shortlink, decode

routes = web.RouteTableDef()

@routes.get("/", allow_head=True)
async def root_route_handler(request):
    file_param = request.query.get("GET")
    hash = request.query.get("HASH")
    red_param = request.query.get("RED")

    # Handle case where both file_param and hash are present
    if file_param and hash:
        try:
            # Determine if file_param is a special type (ASHVER_, DBRE_, PRE_)
            if any(prefix in file_param for prefix in ["ASHVER_", "DBRE_", "PRE_"]):
                _, msgsstring = file_param.split("_", 1)
                base64_string = msgsstring.split(" ", 1)[1] if " " in msgsstring else msgsstring
            else:
                base64_string = file_param.split(" ", 1)[1] if " " in file_param else file_param
            
            _string = await decode(base64_string)
            argument = _string.split("-")

            if len(argument) == 2:
                try:
                    message_id = int(int(argument[1]) / abs(CHANNEL_ID))
                except (ValueError, ZeroDivisionError):
                    return web.HTTPBadRequest(text="Invalid message ID.")
            else:
                return web.HTTPBadRequest(text="Invalid argument format.")
            
            stream = f"{URL}exclusive/{message_id}/?HeartXBotz={hash}"
            dwn = f"{URL}{message_id}/?HeartXBotz={hash}"
            tg_url = f"https://t.me/{BOT_UNAME}?start={base64_string}"
            prem_tg_url = f"https://t.me/{BOT_UNAME}?start=PRE_{base64_string}"

            # Use short links if STREAM_SHORT is enabled
            if STREAM_SHORT:
                stream_url = await get_shortlink(SHORTLINK_URL1, SHORTLINK_API1, stream)
                dwn_url = await get_shortlink(SHORTLINK_URL1, SHORTLINK_API1, dwn)
            else:
                stream_url = stream
                dwn_url = dwn

            html_content = f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>HeartXBotz | Telegram</title>
                <link rel="icon" href="https://i.ibb.co/yNq8CXm/multimedia.png" type="image/x-icon">
                <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@100;200;300;400;600;700&display=swap" rel="stylesheet">
                <style>
                    /* General Reset */
                    * {{
                        margin: 0;
                        padding: 0;
                        box-sizing: border-box;
                    }}
                    body {{
                        background: url('https://envs.sh/HxH.jpg') no-repeat center center fixed;
                        background-size: cover;
                        font-family: 'Poppins', sans-serif;
                        color: #fff;
                        height: 100vh;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                    }}
                    .container {{
                        display: flex;
                        flex-direction: column;
                        justify-content: center;
                        align-items: center;
                        gap: 2rem;
                        background: rgba(0, 0, 0, 0.6);
                        border-radius: 1rem;
                        padding: 3rem;
                        box-shadow: 0 8px 15px rgba(0, 0, 0, 0.2);
                        z-index: 1;
                    }}
                    h1 {{
                        font-size: 3rem;
                        color: #ffd900;
                        margin-bottom: 0.5rem;
                        text-transform: uppercase;
                    }}
                    .button-container {{
                        display: flex;
                        flex-direction: column;
                        gap: 1rem;
                        width: 100%;
                    }}
                    .btn {{
                        width: 100%;
                        max-width: 350px;
                        padding: 1.2rem;
                        font-size: 1.1rem;
                        color: #fff;
                        background: linear-gradient(-45deg, #ffd900, #665700, #a88f00, #333333);
                        background-size: 300%;
                        border: none;
                        border-radius: 2rem;
                        cursor: pointer;
                        transition: transform 0.3s ease, box-shadow 0.3s ease;
                        animation: gradient 8s linear infinite;
                        text-transform: uppercase;
                        letter-spacing: 1px;
                    }}
                    .btn:hover {{
                        transform: translateY(-5px);
                        box-shadow: 0 8px 15px rgba(0, 0, 0, 0.3);
                    }}
                    @keyframes gradient {{
                        0% {{
                            background-position: 0% 50%;
                        }}
                        50% {{
                            background-position: 100% 50%;
                        }}
                        100% {{
                            background-position: 0% 50%;
                        }}
                    }}
                    @media (max-width: 768px) {{
                        h1 {{
                            font-size: 2rem;
                        }}
                        .btn {{
                            font-size: 1rem;
                            padding: 1rem;
                        }}
                    }}
                    .premium-section {{
                        display: none;
                        background: rgba(255, 255, 255, 0.8);
                        padding: 1rem;
                        border-radius: 1rem;
                        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
                        width: 100%;
                        max-width: 350px;
                        margin-top: 2rem;
                    }}
                    .premium-section h4 {{
                        font-size: 1.5rem;
                        color: #333;
                        margin-bottom: 0.5rem;
                    }}
                    .premium-section .btn {{
                        background: linear-gradient(-45deg, #ff5733, #c0392b, #9b2d20, #7f1d1b);
                    }}
                    .footer {{
                        margin-top: 1rem;
                        font-size: 1.2rem;
                        color: #ffd900;
                    }}
                    .footer a {{
                        color: #ffd900;
                        text-decoration: none;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>HeartXBotz</h1>
                    <div class="button-container">
                        <button onclick="window.open('{tg_url}', '_blank')" class="btn">Get Telegram File</button>
                        <button onclick="window.open('{dwn_url}', '_blank')" class="btn">Direct Download</button>
                        <button onclick="window.open('{stream_url}', '_blank')" class="btn">Watch Online</button>
                        <div id="premium-section" class="premium-section">
                            <h4>Premium - Ad Free</h4>
                            <button onclick="window.open('{prem_tg_url}', '_blank')" class="btn">Get Premium File</button>
                        </div>
                    </div>
                    <div class="footer">
                        <p><a href="https://t.me/Heart_thieft" target="_blank">Powered by Heart Thieft</a></p>
                    </div>
                    <p>© 2025 HeartXBotz All Rights Reserved</p>
                </div>
                <script>
                    if ("{IS_VERIFY}" === "True") {{
                        document.getElementById('premium-section').style.display = 'block';
                    }}
                </script>
            </body>
            </html>
            """
            return web.Response(text=html_content, content_type="text/html")
        
        except Exception as e:
            return web.HTTPBadRequest(text=f"Error processing file_param or hash: {str(e)}")

    # If only redirection parameter is present
    elif not file_param and not hash and red_param:
        url = await decode(red_param)
        final_url = await get_shortlink(SHORTLINK_URL2, SHORTLINK_API2, url)
        return web.HTTPFound(location=final_url)

    # If file_param is present but no hash or redirection
    elif file_param and not hash:
        open_url = f"https://t.me/{BOT_UNAME}?start={file_param}"
        return web.HTTPFound(location=open_url)

    # Default redirect
    else:
        return web.HTTPFound(location="https://t.me/HeartXBotz")
