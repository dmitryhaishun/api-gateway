from unittest.mock import patch

import pytest
import requests
from rest_framework import status

from card.helpers.enums import BlockReason, CardStatus


class TestCardPatch:
    card_id = 1
    card_url = "http://api-gateway:8000/api/card/"

    @patch("requests.patch")
    def test_patch_success(self, mock_patch):
        mock_response = requests.Response()
        mock_response.status_code = status.HTTP_200_OK
        mock_response.json = lambda: {"id": 1, "status": CardStatus.BLOCKED, "block_reason": BlockReason.SUSPICIOUS}
        mock_patch.return_value = mock_response

        data = {"status": CardStatus.BLOCKED, "block_reason": BlockReason.SUSPICIOUS}
        response = requests.patch(f"{self.card_url}{self.card_id}/", data)

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"id": 1, "status": CardStatus.BLOCKED, "block_reason": BlockReason.SUSPICIOUS}

    @patch("requests.patch")
    def test_patch_missing_card_status(self, mock_patch):
        mock_response = requests.Response()
        mock_response.status_code = status.HTTP_400_BAD_REQUEST
        mock_response.json = lambda: {"error": "Card new status is required"}
        mock_patch.return_value = mock_response

        data = {"block_reason": BlockReason.SUSPICIOUS}
        response = requests.patch(f"{self.card_url}{self.card_id}/", json=data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {"error": "Card new status is required"}

    @patch("requests.patch")
    def test_patch_missing_block_reason(self, mock_patch):
        mock_response = requests.Response()
        mock_response.status_code = status.HTTP_400_BAD_REQUEST
        mock_response.json = lambda: {"error": "Block reason is required"}
        mock_patch.return_value = mock_response

        data = {"status": CardStatus.BLOCKED}
        response = requests.patch(f"{self.card_url}{self.card_id}/", json=data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {"error": "Block reason is required"}

    @patch("requests.patch")
    @pytest.mark.parametrize("reason", [CardStatus.ISSUANCE, CardStatus.EXPIRED])
    def test_patch_wrong_status(self, mock_patch, reason: CardStatus):
        mock_response = requests.Response()
        mock_response.status_code = status.HTTP_400_BAD_REQUEST
        mock_response.json = lambda: {"message": "Invalid new status"}
        mock_patch.return_value = mock_response

        data = {"status": reason}
        response = requests.patch(f"{self.card_url}{self.card_id}/", json=data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {"message": "Invalid new status"}

    @patch("requests.patch")
    def test_patch_http_error(self, mock_patch):
        mock_response = requests.Response()
        mock_response.status_code = status.HTTP_404_NOT_FOUND
        mock_response.json = lambda: {"message": "Card with this id not found"}
        mock_patch.return_value = mock_response

        data = {"status": CardStatus.BLOCKED, "block_reason": BlockReason.SUSPICIOUS}
        response = requests.patch(f"{self.card_url}{self.card_id}/", data)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {"message": "Card with this id not found"}
