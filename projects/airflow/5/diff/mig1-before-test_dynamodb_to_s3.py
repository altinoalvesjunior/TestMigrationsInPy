from __future__ import annotations

import json
from decimal import Decimal
from unittest.mock import MagicMock, patch

from airflow.providers.amazon.aws.transfers.dynamodb_to_s3 import DynamoDBToS3Operator, JSONEncoder


class JSONEncoderTest:
    def test_jsonencoder_with_decimal(self):
        """Test JSONEncoder correctly encodes and decodes decimal values."""

        for i in ["102938.3043847474", 1.010001, 10, "100", "1E-128", 1e-128]:
            org = Decimal(i)
            encoded = json.dumps(org, cls=JSONEncoder)
            decoded = json.loads(encoded, parse_float=Decimal)
            self.assertAlmostEqual(decoded, org)