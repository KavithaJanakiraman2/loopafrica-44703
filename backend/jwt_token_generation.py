from datetime import datetime
from datetime import timezone
from datetime import timedelta
import requests
import jwt
import os
import uuid
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.x509 import load_pem_x509_certificate

# load key pair created by following https://fhir.epic.com/Documentation?docId=oauth2&section=Creating-Key-Pair
#os.chdir('replace-with-path-to-key-files')
with open('key.pem', 'rb') as private_key_file:
    lines = private_key_file.read()
    private_key = load_pem_private_key(lines, None, default_backend())

with open('cert.pem', 'rb') as cert_file:
    cert_str = cert_file.read()
    cert_obj = load_pem_x509_certificate(cert_str)
    public_key = cert_obj.public_key()

# build the JWT
algorithm = "RS384"
client_id = "ab4810f1-905f-40a5-9a56-e5dcbc0e16db"
endpoint = "https://fhir.epic.com/interconnect-fhir-oauth/oauth2/token"
payload = {
    "iss": client_id,
    "sub": client_id,
    "aud": endpoint,
    "jti": str(uuid.uuid4()),
    "exp": datetime.now(tz=timezone.utc) + timedelta(minutes=+1),
    "scope": "Patient.read Patient.search"
}
token = jwt.encode(
    payload, 
    private_key, 
    algorithm=algorithm,
    headers={"alg": "RS384", "typ": "JWT"},
    )
print(f"headers {jwt.get_unverified_header(token)}")
decoded = jwt.decode(token, public_key, audience=endpoint, algorithms=[algorithm])
print(f"payload {decoded}")

payload = {
    "grant_type": "client_credentials",
    "client_assertion_type": "urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
    "client_assertion": token
}
r = requests.post('https://fhir.epic.com/interconnect-fhir-oauth/oauth2/token', data=payload, timeout=10)
print(r.status_code, f"\n------{r}\n-------",  f"\n<---Token\n-->{r.content}") # is everything 200 OK?
