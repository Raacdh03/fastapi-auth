import datetime
import os
# from dotenv import load_dotenv

# load_dotenv()

expired = datetime.timedelta(minutes=30)
private_key = None
public_key = None

class Config:
    SECRET_KEY=os.getenv("SECRET_KEY")
    JWT_PUBLIC_KEY = "jwt_public_key"
    JWT_PRIVATE_KEY = "jwt_private_key"
    CLIENT_ID = os.getenv("CLIENT_ID")
    ENCRYPTION_KEY = "200af68706880879a7d30ecd5ad8bc407b15a7e38eb6a0bba8cc12283418656c"
    IV = "e0dadba31ca191db7b81f97a6436bc68"