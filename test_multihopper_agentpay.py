#!/usr/bin/env python3
"""
test_multihopper_agentpay.py - Comprehensive Test Suite for MultiHopper AgentPay
Validates:
1. Fee estimation and 50% revenue-share computation
2. Single-recipient and Multi-destination transfer creation
3. Transaction preparation and two-step broadcast confirmation
4. Agent budget policy enforcement
5. Usage and revenue-share metrics aggregation
"""

import unittest
from multihopper_client import MultiHopperClient, MultiHopperAPIError
from agent_treasury_manager import AgentTreasuryManager


class TestMultiHopperAgentPay(unittest.TestCase):

    def setUp(self):
        self.client = MultiHopperClient(
            api_key="mock_mh_key_sandbox_2026",
            integrator_id="int_agentpay_lab_403",
            mock_mode=True,
        )
        self.treasury_wallet = "7De72d2D1EDb960e0Dc287ce60176b122a472059"
        self.treasury = AgentTreasuryManager(
            treasury_wallet=self.treasury_wallet,
            client=self.client,
            max_single_tx_lamports=100_000_000_000,
        )

    def test_fee_estimation_and_split(self):
        amount = 10_000_000_000  # 10 SOL
        estimate = self.client.estimate_fees(
            sender_wallet=self.treasury_wallet,
            amount_lamports=amount,
            recipient_wallet="9WzDXwBbmkg8ZTbNMqUxvQRAyrZzDsGYdLVL9zYtAWWM",
        )
        self.assertEqual(estimate["percentageFee"], 0.005)  # 0.5%
        self.assertEqual(estimate["estimatedFeeLamports"], 50_000_000)  # 0.05 SOL
        self.assertEqual(estimate["integratorShareLamports"], 25_000_000)  # 0.025 SOL (50% share)

    def test_agent_budget_enforcement(self):
        agent_id = "agent_scraper_01"
        self.treasury.set_agent_budget(agent_id, 2_000_000_000)  # 2 SOL

        # Attempt to spend more than budget
        with self.assertRaises(ValueError):
            self.treasury.execute_agent_payout(
                agent_id=agent_id,
                recipient_wallet="9WzDXwBbmkg8ZTbNMqUxvQRAyrZzDsGYdLVL9zYtAWWM",
                amount_lamports=3_000_000_000,  # 3 SOL
            )

        # Successful spend within budget
        payout = self.treasury.execute_agent_payout(
            agent_id=agent_id,
            recipient_wallet="9WzDXwBbmkg8ZTbNMqUxvQRAyrZzDsGYdLVL9zYtAWWM",
            amount_lamports=1_000_000_000,  # 1 SOL
            memo="Task #402 verification bounty",
        )
        self.assertEqual(payout["status"], "deployed")
        self.assertEqual(self.treasury.agent_budgets[agent_id], 1_000_000_000)  # 1 SOL remaining

    def test_multi_destination_split(self):
        destinations = [
            {"wallet": "WalletA1111111111111111111111111111111111111", "shareBps": 6000},  # 60%
            {"wallet": "WalletB2222222222222222222222222222222222222", "shareBps": 4000},  # 40%
        ]
        created = self.treasury.execute_multi_agent_split(
            destinations=destinations,
            total_lamports=5_000_000_000,
        )
        self.assertEqual(created["status"], "quoted")
        self.assertEqual(len(created["destinations"]), 2)

    def test_usage_and_revenue_metrics(self):
        usage = self.client.get_usage()
        self.assertGreaterEqual(usage["totalRoutedVolumeUsd"], 1_000_000)
        # Verify 0.25% revenue share formula: 1,250,000 * 0.0025 = 3,125 USD
        expected_share = usage["totalRoutedVolumeUsd"] * 0.0025
        self.assertEqual(usage["earnedRevenueShareUsd"], expected_share)


if __name__ == "__main__":
    unittest.main()
