from io import BytesIO

from collect_offline_app.models import TestModel
from django.test import TestCase, tag
from django_collect_offline.models import OutgoingTransaction
from django_collect_offline.serializers import OutgoingTransactionSerializer
from django_collect_offline.site_offline_models import site_offline_models
from django_crypto_fields.constants import LOCAL_MODE
from django_crypto_fields.cryptor import Cryptor
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer


class TestSerializers(TestCase):

    databases = "__all__"

    def setUp(self):
        TestModel.objects.create(f1="give any one species too much rope ...")
        site_offline_models.registry = {}
        site_offline_models.loaded = False
        sync_models = ["collect_offline_app.testmodel"]
        site_offline_models.register(sync_models)

    def test_outgoingtransaction_serializer_inits(self):
        obj = OutgoingTransaction.objects.last()
        serializer = OutgoingTransactionSerializer(obj)
        self.assertTrue(serializer.data)

    def test_outgoingtransaction_serializer_renders(self):
        obj = OutgoingTransaction.objects.last()
        serializer = OutgoingTransactionSerializer(obj)
        serializer.data
        self.assertTrue(JSONRenderer().render(serializer.data))

    def test_outgoingtransaction_serializer_parses(self):
        obj = OutgoingTransaction.objects.last()
        serializer = OutgoingTransactionSerializer(obj)
        serializer.data
        content = JSONRenderer().render(serializer.data)
        stream = BytesIO(content)
        data = JSONParser().parse(stream)
        self.assertEqual(data["tx"], serializer.data["tx"])

    def test_outgoingtransaction_serializer_validates(self):
        obj = OutgoingTransaction.objects.last()
        serializer = OutgoingTransactionSerializer(obj)
        serializer.data
        content = JSONRenderer().render(serializer.data)
        stream = BytesIO(content)
        data = JSONParser().parse(stream)
        serializer = OutgoingTransactionSerializer(data=data)
        serializer.is_valid()
        self.assertEqual(obj.tx, serializer.validated_data["tx"])

    def test_outgoingtransaction_serializer_tx_decrypts(self):
        obj = OutgoingTransaction.objects.last()
        serializer = OutgoingTransactionSerializer(obj)
        serializer.data
        content = JSONRenderer().render(serializer.data)
        stream = BytesIO(content)
        data = JSONParser().parse(stream)
        serializer = OutgoingTransactionSerializer(data=data)
        serializer.is_valid()
        cryptor = Cryptor()
        self.assertTrue(
            cryptor.aes_decrypt(serializer.validated_data["tx"], LOCAL_MODE)
        )
        value = cryptor.aes_decrypt(
            serializer.validated_data["tx"], LOCAL_MODE
        ).encode()
        stream = BytesIO(value)
        json_data = JSONParser().parse(stream)
        self.assertTrue(
            json_data[0]["fields"]["f1"], "give any one species too much rope ..."
        )
