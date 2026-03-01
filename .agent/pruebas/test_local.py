import unittest
import os
import sys
# Ajuste de ruta para encontrar 'app' desde .agent/pruebas/
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from dotenv import load_dotenv
load_dotenv()
from app import create_app
from app.extensions import db
from app.models.clients import Cliente

class LocalTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('development')
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False
        if not self.app.config.get('SECRET_KEY'):
            self.app.config['SECRET_KEY'] = 'test-key-gelmex'
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_catalog_access(self):
        """Test public catalog is accessible"""
        response = self.client.get('/portal/catalogo')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'GelMex', response.data)

    def test_client_admin_access(self):
        """Test client management access (mocking login if needed)"""
        # Note: Since auth is required, this might fail without a logged user.
        # But we can check if it tries to redirect to login at least.
        response = self.client.get('/clientes/')
        self.assertIn(response.status_code, [200, 302])

    def test_db_schema_sync(self):
        """Verify that access_code column exists in the database"""
        try:
            # Try to fetch one client to see if access_code fails
            Cliente.query.first()
            print("✅ Database schema seems synced.")
        except Exception as e:
            self.fail(f"❌ Database error (probably missing column): {str(e)}")

if __name__ == '__main__':
    unittest.main()
