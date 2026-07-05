import os
from dotenv import load_dotenv

load_dotenv()

key = os.getenv("GEMINI_API_KEY")

print("--- DIAGNÓSTICO DE CREDENCIALES ---")
if key is None:
    print("❌ Resultado: El archivo .env NO se está leyendo en absoluto.")
else:
    print(f"✅ Resultado: Clave detectada.")
    print(f"   Largo de la clave: {len(key)} caracteres.")
    print(f"   Empieza con: '{key[:6]}'")
    print(f"   Termina con: '{key[-4:]}'")
    if " " in key:
        print("⚠️ ALERTA: Tu clave tiene espacios ocultos por ahí metidos.")
    if '"' in key or "'" in key:
        print("⚠️ ALERTA: Tu clave tiene comillas metidas dentro del valor.")
print("----------------------------------")