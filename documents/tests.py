import json
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Document, SharedAccess


class DocumentModelTests(TestCase):
    def setUp(self):
        self.alice = User.objects.create_user(username='alice_test', password='pass123')
        self.bob = User.objects.create_user(username='bob_test', password='pass123')

    def test_document_creation(self):
        """Document should be created with correct owner and default title"""
        doc = Document.objects.create(owner=self.alice)
        self.assertEqual(doc.title, "Untitled Document")
        self.assertEqual(doc.owner, self.alice)
        self.assertEqual(doc.content, "")

    def test_document_str_representation(self):
        doc = Document.objects.create(title="My Report", owner=self.alice)
        self.assertEqual(str(doc), "My Report")

    def test_shared_access_creation(self):
        """SharedAccess should correctly link a document to another user"""
        doc = Document.objects.create(title="Shared Doc", owner=self.alice)
        share = SharedAccess.objects.create(document=doc, shared_with=self.bob)
        self.assertEqual(share.document, doc)
        self.assertEqual(share.shared_with, self.bob)

    def test_duplicate_share_not_allowed(self):
        """unique_together constraint should prevent duplicate shares"""
        doc = Document.objects.create(title="Doc", owner=self.alice)
        SharedAccess.objects.create(document=doc, shared_with=self.bob)
        with self.assertRaises(Exception):
            SharedAccess.objects.create(document=doc, shared_with=self.bob)


class DocumentViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.alice = User.objects.create_user(username='alice_test', password='pass123')
        self.bob = User.objects.create_user(username='bob_test', password='pass123')
        self.doc = Document.objects.create(title="Alice's Doc", owner=self.alice, content="Hello")

    def test_login_required_redirects_dashboard(self):
        """Unauthenticated user should be redirected from dashboard"""
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)

    def test_login_success(self):
        response = self.client.post(reverse('login'), {
            'username': 'alice_test',
            'password': 'pass123'
        })
        self.assertEqual(response.status_code, 302)  # redirect to dashboard

    def test_dashboard_shows_owned_documents(self):
        self.client.login(username='alice_test', password='pass123')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.doc, response.context['owned_docs'])

    def test_non_owner_cannot_access_unshared_document(self):
        """Bob should NOT be able to access Alice's document without sharing"""
        self.client.login(username='bob_test', password='pass123')
        response = self.client.get(reverse('edit_document', args=[self.doc.id]))
        self.assertRedirects(response, reverse('dashboard'))

    def test_shared_document_accessible_by_shared_user(self):
        """After sharing, bob SHOULD be able to access alice's document"""
        SharedAccess.objects.create(document=self.doc, shared_with=self.bob)
        self.client.login(username='bob_test', password='pass123')
        response = self.client.get(reverse('edit_document', args=[self.doc.id]))
        self.assertEqual(response.status_code, 200)

    def test_owner_can_edit_document_content(self):
        """Owner should be able to update title/content via JSON POST"""
        self.client.login(username='alice_test', password='pass123')
        response = self.client.post(
            reverse('edit_document', args=[self.doc.id]),
            data=json.dumps({'title': 'Updated Title', 'content': '<p>Updated content</p>'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.doc.refresh_from_db()
        self.assertEqual(self.doc.title, 'Updated Title')
        self.assertEqual(self.doc.content, '<p>Updated content</p>')

    def test_non_owner_cannot_edit_document(self):
        """Shared (non-owner) user should NOT be able to edit content"""
        SharedAccess.objects.create(document=self.doc, shared_with=self.bob)
        self.client.login(username='bob_test', password='pass123')
        response = self.client.post(
            reverse('edit_document', args=[self.doc.id]),
            data=json.dumps({'title': 'Hacked Title', 'content': 'Hacked'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 403)
        self.doc.refresh_from_db()
        self.assertNotEqual(self.doc.title, 'Hacked Title')

    def test_share_document_creates_access(self):
        self.client.login(username='alice_test', password='pass123')
        self.client.post(reverse('share_document', args=[self.doc.id]), {
            'username': 'bob_test'
        })
        self.assertTrue(SharedAccess.objects.filter(document=self.doc, shared_with=self.bob).exists())

    def test_upload_rejects_invalid_file_type(self):
        """Uploading unsupported file type should not create a document"""
        self.client.login(username='alice_test', password='pass123')
        fake_file = SimpleUploadedFile("test.pdf", b"fake pdf content")
        initial_count = Document.objects.count()
        self.client.post(reverse('upload_file'), {'file': fake_file})
        self.assertEqual(Document.objects.count(), initial_count)

    def test_upload_creates_document_from_txt_file(self):
        self.client.login(username='alice_test', password='pass123')
        txt_file = SimpleUploadedFile("notes.txt", b"Hello world\nSecond line")
        self.client.post(reverse('upload_file'), {'file': txt_file})
        self.assertTrue(Document.objects.filter(title="notes.txt").exists())