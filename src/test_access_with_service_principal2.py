import os, base64, json, requests
from azure.identity import ClientSecretCredential

TENANT_ID = os.environ["AZURE_TENANT_ID"]
CLIENT_ID = os.environ["AZURE_CLIENT_ID"]
CLIENT_SECRET = os.environ["AZURE_CLIENT_SECRET"]

API_APP_ID_URI = "api://27bbd221-f549-4c57-b8a4-a6fc688636f4"
SCOPE = f"{API_APP_ID_URI}/.default"  # client-credentials flow uses .default

cred = ClientSecretCredential(TENANT_ID, CLIENT_ID, CLIENT_SECRET)
token = cred.get_token(SCOPE).token

def decode(token):
    p = token.split(".")[1]
    p += "=" * (-len(p) % 4)
    return json.loads(base64.urlsafe_b64decode(p))

claims = decode(token)
print("aud:", claims.get("aud"))
print("appid:", claims.get("appid"))
print("roles:", claims.get("roles"))
print("azp:", claims.get("azp"))

base = "https://wa-sharepoint-gpt-middleware-02.azurewebsites.net"

# optional health check
r = requests.get(f"{base}/alive", headers={"Authorization": f"Bearer {token}"})
print("alive:", r.status_code, r.text)