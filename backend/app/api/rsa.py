from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os
import io
import base64
import secrets

router = APIRouter()

class RSAKeyGenRequest(BaseModel):
    key_size: Optional[int] = 2048

class RSAKeyResponse(BaseModel):
    public_key: str
    private_key: str
    key_size: int

WARNING = "⚠️ RSA may become vulnerable to future quantum computers. Consider migrating to Post-Quantum Cryptography."

@router.post("/rsa/generate-keys")
async def generate_rsa_keys(request: RSAKeyGenRequest):
    try:
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=request.key_size
        )
        public_key = private_key.public_key()

        private_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ).decode()

        public_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode()

        return RSAKeyResponse(
            public_key=public_pem,
            private_key=private_pem,
            key_size=request.key_size
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating RSA keys: {str(e)}")

def encrypt_aes(data: bytes, key: bytes) -> bytes:
    iv = secrets.token_bytes(16)
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted = encryptor.update(data) + encryptor.finalize()
    return iv + encrypted

def decrypt_aes(encrypted_data: bytes, key: bytes) -> bytes:
    iv = encrypted_data[:16]
    ciphertext = encrypted_data[16:]
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    return decryptor.update(ciphertext) + decryptor.finalize()

@router.post("/rsa/encrypt-file")
async def rsa_encrypt_file(
    file: UploadFile = File(...),
    key_size: int = Form(2048)
):
    try:
        # Generate RSA keys
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=key_size
        )
        public_key = private_key.public_key()

        # Read file content
        file_content = await file.read()

        # Generate random AES key
        aes_key = secrets.token_bytes(32)  # 256-bit AES key

        # Encrypt file with AES
        encrypted_file_content = encrypt_aes(file_content, aes_key)

        # Encrypt AES key with RSA
        encrypted_aes_key = public_key.encrypt(
            aes_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        # Combine encrypted AES key and encrypted file content
        # Format: [encrypted_aes_key_length (4 bytes)][encrypted_aes_key][encrypted_file]
        key_length = len(encrypted_aes_key).to_bytes(4, byteorder='big')
        combined = key_length + encrypted_aes_key + encrypted_file_content

        # Serialize private key
        private_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )

        # Return as zip-like structure in response
        from io import BytesIO
        import zipfile

        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
            zf.writestr(f"encrypted_{file.filename}.rsa", combined)
            zf.writestr("private_key.pem", private_pem)
        
        zip_buffer.seek(0)

        return StreamingResponse(
            zip_buffer,
            media_type="application/zip",
            headers={"Content-Disposition": f"attachment; filename=encrypted_files.zip"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error encrypting file: {str(e)}")

@router.post("/rsa/decrypt-file")
async def rsa_decrypt_file(
    encrypted_file: UploadFile = File(...),
    private_key_file: UploadFile = File(...)
):
    try:
        # Read encrypted file content
        encrypted_content = await encrypted_file.read()

        # Read and load private key
        private_key_pem = await private_key_file.read()
        private_key = serialization.load_pem_private_key(private_key_pem, password=None)

        # Extract encrypted AES key and encrypted file content
        key_length = int.from_bytes(encrypted_content[:4], byteorder='big')
        encrypted_aes_key = encrypted_content[4:4 + key_length]
        encrypted_file_content = encrypted_content[4 + key_length:]

        # Decrypt AES key with RSA
        try:
            aes_key = private_key.decrypt(
                encrypted_aes_key,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
        except Exception as e:
            raise HTTPException(status_code=400, detail="Decryption Failed: Invalid RSA Key")

        # Decrypt file content with AES
        try:
            decrypted_content = decrypt_aes(encrypted_file_content, aes_key)
        except Exception as e:
            raise HTTPException(status_code=400, detail="File Integrity Error or Corrupted File")

        # Get original filename (remove .rsa extension if present)
        original_filename = encrypted_file.filename
        if original_filename.endswith('.rsa'):
            original_filename = original_filename[:-4]

        return StreamingResponse(
            io.BytesIO(decrypted_content),
            media_type="application/octet-stream",
            headers={"Content-Disposition": f"attachment; filename=decrypted_{original_filename}"}
        )
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error decrypting file: {str(e)}")
