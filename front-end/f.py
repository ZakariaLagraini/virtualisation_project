from datetime import datetime, timedelta, timezone
from cryptography import x509
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.x509.oid import NameOID
from cryptography.hazmat.backends import default_backend

# Generate a private key
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
    backend=default_backend()
)

# Generate a self-signed certificate
builder = x509.CertificateBuilder()
builder = builder.subject_name(x509.Name([
    x509.NameAttribute(NameOID.COMMON_NAME, u"localhost")
]))
builder = builder.issuer_name(x509.Name([
    x509.NameAttribute(NameOID.COMMON_NAME, u"localhost")
]))
builder = builder.not_valid_before(datetime.now(timezone.utc))
builder = builder.not_valid_after(datetime.now(timezone.utc) + timedelta(days=365))
builder = builder.serial_number(x509.random_serial_number())
builder = builder.public_key(private_key.public_key())

cert = builder.sign(private_key, hashes.SHA256(), default_backend())

# Write the private key to a file
with open("private_key.pem", "wb") as f:
    f.write(private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()    ))

# Write the certificate to a file
with open("certificate.pem", "wb") as f:
    f.write(cert.public_bytes(encoding=serialization.Encoding.PEM))
