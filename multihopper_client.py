#!/usr/bin/env python3
"""
multihopper_client.py - Official-Spec Client for MultiHopper Solana Protocol
Ref: https://dev-docs.multihopper.com/

Handles the complete transfer lifecycle:
1. Fee Estimation: POST /transfers/estimate
2. Transfer Creation: POST /transfers
3. Transaction Preparation: POST /transfers/:id/prepare
4. Broadcast Confirmation: POST /transfers/:id/confirm-broadcast
5. Lifecycle Tracking: GET /transfers/:id
6. Hop Library & Usage: GET /hop-library, GET /usage
"""

import json
import time
import urllib.request
import urllib.error
from typing import Any, Dict, List, Optional, Union


class MultiHopperAPIError(Exception):
    def __init__(self, status_code: int, message: str, payload: Optional[Dict] = None):
        super().__init__(f"MultiHopper API [{status_code}]: {message}")
        self.status_code = status_code
        self.payload = payload or {}


class MultiHopperClient:
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = "https://api.multihopper.com",
        integrator_id: Optional[str] = None,
        timeout: int = 15,
        mock_mode: bool = False,
    ):
        self.api_key = api_key or ""
        self.base_url = base_url.rstrip("/")
        self.integrator_id = integrator_id
        self.timeout = timeout
        self.mock_mode = mock_mode

    def _headers(self) -> Dict[str, str]:
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "MultiHopperAgentPay/1.0.0",
        }
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
            headers["x-api-key"] = self.api_key
        if self.integrator_id:
            headers["x-integrator-id"] = self.integrator_id
        return headers

    def _request(
        self,
        method: str,
        path: str,
        data: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        if self.mock_mode:
            return self._mock_response(method, path, data)

        url = f"{self.base_url}{path}"
        body_bytes = json.dumps(data).encode("utf-8") if data is not None else None
        req = urllib.request.Request(
            url,
            data=body_bytes,
            headers=self._headers(),
            method=method,
        )

        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                text = resp.read().decode("utf-8")
                return json.loads(text) if text else {}
        except urllib.error.HTTPError as e:
            err_text = e.read().decode("utf-8", errors="ignore")
            try:
                err_json = json.loads(err_text)
                msg = err_json.get("message") or err_json.get("error") or err_text
            except Exception:
                err_json = {}
                msg = err_text
            raise MultiHopperAPIError(e.code, msg, err_json)
        except Exception as e:
            raise MultiHopperAPIError(0, str(e))

    def estimate_fees(
        self,
        sender_wallet: str,
        amount_lamports: int,
        token_mint: Optional[str] = None,
        recipient_wallet: Optional[str] = None,
        destinations: Optional[List[Dict[str, Any]]] = None,
        hops_count: int = 2,
    ) -> Dict[str, Any]:
        """Estimate fee tier and SOL requirements."""
        payload = {
            "senderWallet": sender_wallet,
            "amount": amount_lamports,
            "hopsCount": hops_count,
        }
        if token_mint:
            payload["tokenMint"] = token_mint
        if recipient_wallet:
            payload["recipientWallet"] = recipient_wallet
        if destinations:
            payload["destinations"] = destinations

        return self._request("POST", "/transfers/estimate", payload)

    def create_transfer(
        self,
        sender_wallet: str,
        amount_lamports: int,
        recipient_wallet: Optional[str] = None,
        destinations: Optional[List[Dict[str, Any]]] = None,
        token_mint: Optional[str] = None,
        route_template_id: Optional[str] = None,
        custom_route: Optional[Dict[str, Any]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Step 1: Create a quoted transfer."""
        if not recipient_wallet and not destinations:
            raise ValueError("Either 'recipient_wallet' or 'destinations' must be provided.")

        payload: Dict[str, Any] = {
            "senderWallet": sender_wallet,
            "amount": amount_lamports,
        }
        if recipient_wallet:
            payload["recipientWallet"] = recipient_wallet
        if destinations:
            payload["destinations"] = destinations
        if token_mint:
            payload["tokenMint"] = token_mint
        if route_template_id:
            payload["routeTemplateId"] = route_template_id
        if custom_route:
            payload["route"] = custom_route
        if metadata:
            payload["metadata"] = metadata

        return self._request("POST", "/transfers", payload)

    def prepare_transfer(self, transfer_id: str) -> Dict[str, Any]:
        """Step 2: Retrieve unsigned transaction bundles (base64)."""
        return self._request("POST", f"/transfers/{transfer_id}/prepare")

    def confirm_broadcast(
        self,
        transfer_id: str,
        keeper_funding_signature: Optional[str] = None,
        route_init_signatures: Optional[List[str]] = None,
        orchestrator_signature: Optional[str] = None,
        session_signatures: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Steps 4 and 6: Confirm transaction signatures."""
        payload: Dict[str, Any] = {}
        if keeper_funding_signature:
            payload["keeperFundingSignature"] = keeper_funding_signature
        if route_init_signatures:
            payload["routeInitSignatures"] = route_init_signatures
        if orchestrator_signature:
            payload["orchestratorSignature"] = orchestrator_signature
        if session_signatures:
            payload["sessionSignatures"] = session_signatures

        return self._request("POST", f"/transfers/{transfer_id}/confirm-broadcast", payload)

    def get_transfer(self, transfer_id: str) -> Dict[str, Any]:
        """Poll status, execution phase, and progress."""
        return self._request("GET", f"/transfers/{transfer_id}")

    def list_transfers(
        self,
        status: Optional[str] = None,
        limit: int = 50,
    ) -> Dict[str, Any]:
        """Query transfers by status or date."""
        query = f"?limit={limit}"
        if status:
            query += f"&status={status}"
        return self._request("GET", f"/transfers{query}")

    def get_hop_library(self) -> Dict[str, Any]:
        """Retrieve vetted public hops for custom route construction."""
        return self._request("GET", "/hop-library")

    def get_usage(self) -> Dict[str, Any]:
        """Get volume, fee, and 50% revenue-share metrics."""
        return self._request("GET", "/usage")

    def _mock_response(
        self,
        method: str,
        path: str,
        data: Optional[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """Deterministic simulation for tests and offline development."""
        if path == "/transfers/estimate":
            amount = data.get("amount", 1000000)
            fee = int(amount * 0.005)  # 0.5% standard fee
            return {
                "estimatedFeeLamports": fee,
                "percentageFee": 0.005,
                "integratorShareLamports": int(fee * 0.5),  # 0.25% share
                "requiredSolForKeepers": 15000000,  # 0.015 SOL
                "estimatedDurationSeconds": 45,
            }
        elif path == "/transfers" and method == "POST":
            transfer_id = f"mh_tx_{int(time.time())}_{hash(str(data)) % 10000}"
            return {
                "id": transfer_id,
                "status": "quoted",
                "senderWallet": data.get("senderWallet"),
                "amount": data.get("amount"),
                "tokenMint": data.get("tokenMint", "So11111111111111111111111111111111111111112"),
                "feePercentage": 0.005,
                "expiresAt": int(time.time()) + 900,
                "destinations": data.get("destinations", []),
            }
        elif "/prepare" in path:
            return {
                "keeperFundingTx": "AQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACAAQAGBQ...",
                "routeInitTxs": [{"base64": "AgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACAAQAGBQ..."}],
                "orchestratorInitTx": "AwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACAAQAGBQ...",
                "sessionInitTxs": ["BAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACAAQAGBQ..."],
            }
        elif "/confirm-broadcast" in path:
            return {
                "status": "deployed",
                "phase": "routing",
                "message": "Signatures accepted, keeper network executing hops.",
            }
        elif path.startswith("/transfers/"):
            return {
                "id": path.split("/")[-1],
                "status": "completed",
                "phase": "settled",
                "hopsCompleted": 2,
                "totalHops": 2,
                "qualifyingVolumeUsd": 5000.0,
            }
        elif path == "/usage":
            return {
                "totalRoutedVolumeUsd": 1250000.0,
                "qualifyingVolumeUsd": 1250000.0,
                "earnedRevenueShareUsd": 3125.0,  # 0.25% of 1.25M
                "totalTransfers": 420,
            }
        return {"status": "ok"}
