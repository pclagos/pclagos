#!/usr/bin/env python
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pc_repair.settings')
django.setup()

from django.db import connection

def test_database():
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT version();")
            version = cursor.fetchone()
            print("✅ Conexión a base de datos exitosa!")
            print(f"PostgreSQL version: {version[0]}")
            return True
    except Exception as e:
        print(f"❌ Error conectando a la base de datos: {e}")
        return False

if __name__ == "__main__":
    test_database()
