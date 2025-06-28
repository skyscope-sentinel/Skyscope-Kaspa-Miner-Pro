import time

# In a real application, you'd use a library to fetch KAS/USD price, e.g., requests with CoinGecko API
# For now, we'll simulate it.

class RewardsManager:
    """
    Manages the distribution of mined Kaspa (KAS) rewards, including
    developer fee calculation and the owner's allocation target.
    """
    DEV_FEE_PERCENTAGE = 10.0 # 10%

    def __init__(self,
                 user_kaspa_address: str,
                 dev_fee_address: str,
                 owner_kaspa_address: str, # Owner's KAS wallet for their allocation
                 owner_allocation_target_usd: float = 50000.0):

        if not user_kaspa_address or not user_kaspa_address.startswith("kaspa:"):
            raise ValueError("Invalid user Kaspa address provided.")
        if not dev_fee_address or not dev_fee_address.startswith("kaspa:"):
            raise ValueError("Invalid developer fee Kaspa address provided.")
        if not owner_kaspa_address or not owner_kaspa_address.startswith("kaspa:"):
            raise ValueError("Invalid owner Kaspa address for allocation provided.")

        self.user_kaspa_address = user_kaspa_address
        self.dev_fee_address = dev_fee_address
        self.owner_kaspa_address = owner_kaspa_address

        self.owner_allocation_target_usd = owner_allocation_target_usd
        self.current_kas_usd_price: float | None = None # To be updated externally or via method

        self.cumulative_dev_fee_kas: float = 0.0
        self.cumulative_owner_allocation_kas: float = 0.0
        self.cumulative_user_net_kas: float = 0.0
        self.total_gross_kas_processed: float = 0.0

        self.owner_target_met = False
        self._update_owner_target_met_status() # Initial check

        print(f"RewardsManager Initialized:")
        print(f"  User KAS Address: {self.user_kaspa_address}")
        print(f"  Dev Fee KAS Address: {self.dev_fee_address} ({self.DEV_FEE_PERCENTAGE}%)")
        print(f"  Owner KAS Address (for allocation): {self.owner_kaspa_address}")
        print(f"  Owner Allocation Target: ${self.owner_allocation_target_usd:,.2f} USD in KAS")

    def update_kas_usd_price(self, new_price: float):
        """
        Updates the current KAS/USD price.
        In a real application, this would be fetched from a reliable price oracle or API.
        """
        if new_price <= 0:
            print("Warning (RewardsManager): KAS/USD price must be positive.")
            # Keep old price if new one is invalid and an old one exists
            if self.current_kas_usd_price is None:
                 self.current_kas_usd_price = 0.000001 # Avoid division by zero if it was None
            return

        self.current_kas_usd_price = new_price
        # print(f"RewardsManager: KAS/USD price updated to ${self.current_kas_usd_price:.4f}")
        self._update_owner_target_met_status()

    def _get_owner_allocation_target_kas(self) -> float:
        """Calculates the owner's allocation target in KAS based on the current price."""
        if self.current_kas_usd_price is None or self.current_kas_usd_price <= 0:
            # print("Warning (RewardsManager): KAS/USD price not set or invalid. Owner allocation cannot be calculated in KAS.")
            return float('inf') # Effectively means target can't be met if price is unknown
        return self.owner_allocation_target_usd / self.current_kas_usd_price

    def _update_owner_target_met_status(self):
        """Checks if the owner's allocation target in KAS has been met."""
        if self.owner_target_met: # Already met, no need to re-check unless reset
            return

        target_kas = self._get_owner_allocation_target_kas()
        if self.cumulative_owner_allocation_kas >= target_kas:
            self.owner_target_met = True
            print(f"INFO (RewardsManager): Owner's KAS allocation target of {target_kas:,.4f} KAS (approx. ${self.owner_allocation_target_usd:,.2f}) has been met!")


    def process_mined_reward(self, gross_kas_reward: float) -> list[dict]:
        """
        Processes a gross KAS reward from a mined block or share aggregation.
        Calculates dev fee, owner allocation (if target not met), and user's net share.
        Updates cumulative totals.

        Args:
            gross_kas_reward (float): The total KAS reward before any deductions.

        Returns:
            list[dict]: A list of conceptual payout instructions. Each dict contains:
                        {'address': str, 'amount_kas': float, 'type': str}
                        Types: 'dev_fee', 'owner_allocation', 'user_reward'
        """
        if gross_kas_reward <= 0:
            return []

        self.total_gross_kas_processed += gross_kas_reward
        payout_instructions = []

        # 1. Calculate Developer Fee
        dev_fee_amount = gross_kas_reward * (self.DEV_FEE_PERCENTAGE / 100.0)
        self.cumulative_dev_fee_kas += dev_fee_amount
        payout_instructions.append({
            "address": self.dev_fee_address,
            "amount_kas": dev_fee_amount,
            "type": "dev_fee"
        })

        kas_after_dev_fee = gross_kas_reward - dev_fee_amount

        # 2. Calculate Owner's Allocation (if target not yet met)
        kas_for_owner = 0.0
        if not self.owner_target_met:
            self._update_owner_target_met_status() # Ensure status is current based on price
            if not self.owner_target_met: # Check again
                owner_target_kas = self._get_owner_allocation_target_kas()
                needed_for_owner = owner_target_kas - self.cumulative_owner_allocation_kas

                if needed_for_owner > 0:
                    kas_for_owner = min(kas_after_dev_fee, needed_for_owner)
                    self.cumulative_owner_allocation_kas += kas_for_owner
                    payout_instructions.append({
                        "address": self.owner_kaspa_address,
                        "amount_kas": kas_for_owner,
                        "type": "owner_allocation"
                    })
                    self._update_owner_target_met_status() # Check if target met after this allocation

        # 3. Calculate User's Net Reward
        user_net_reward = kas_after_dev_fee - kas_for_owner
        if user_net_reward > 0: # Ensure user reward is not negative
            self.cumulative_user_net_kas += user_net_reward
            payout_instructions.append({
                "address": self.user_kaspa_address,
                "amount_kas": user_net_reward,
                "type": "user_reward"
            })

        return payout_instructions

    def get_cumulative_stats(self) -> dict:
        """Returns a dictionary of all cumulative reward statistics."""
        owner_target_kas = self._get_owner_allocation_target_kas()
        return {
            "total_gross_kas_processed": self.total_gross_kas_processed,
            "cumulative_dev_fee_kas": self.cumulative_dev_fee_kas,
            "cumulative_owner_allocation_kas": self.cumulative_owner_allocation_kas,
            "owner_allocation_target_usd": self.owner_allocation_target_usd,
            "owner_allocation_target_kas": owner_target_kas if owner_target_kas != float('inf') else "N/A (Price Unknown)",
            "owner_target_met": self.owner_target_met,
            "cumulative_user_net_kas": self.cumulative_user_net_kas,
            "current_kas_usd_price": self.current_kas_usd_price
        }

if __name__ == '__main__':
    print("--- RewardsManager Conceptual Test ---")

    user_addr = "kaspa:qzrhasap30pzrth070tx6m0nslk03xl0qgmpguex68nmd68g277fuqfsqg0ls"
    dev_addr  = "kaspa:qqggvdrxjqdgwql4aac8hg0pq2v4z5p46l86f98hq7ax29k7x55v7sycs9kvm"
    owner_addr= "kaspa:qp0vf0q0y0g0l0j0c0s030z0k0f0d0a0q0g0f0e0d0c0b0a0g0f0e0d0c0b0a" # Dummy owner address

    rewards_mgr = RewardsManager(
        user_kaspa_address=user_addr,
        dev_fee_address=dev_addr,
        owner_kaspa_address=owner_addr,
        owner_allocation_target_usd=10.0 # Small target for testing
    )

    rewards_mgr.update_kas_usd_price(0.10) # $0.10 per KAS -> Owner target is 100 KAS

    print("\nSimulating mined blocks...")
    block_rewards = [10, 20, 30, 40, 50, 60] # Gross KAS rewards
    total_sim_gross_kas = 0

    for i, reward in enumerate(block_rewards):
        total_sim_gross_kas += reward
        print(f"\nProcessing Block {i+1} Reward: {reward} KAS (Gross)")
        payouts = rewards_mgr.process_mined_reward(reward)
        for p in payouts:
            print(f"  -> {p['type']}: {p['amount_kas']:.8f} KAS to {p['address'][:15]}...")

        stats = rewards_mgr.get_cumulative_stats()
        print(f"  Cumulative User Net: {stats['cumulative_user_net_kas']:.8f} KAS")
        print(f"  Cumulative Owner Allocation: {stats['cumulative_owner_allocation_kas']:.4f} / {stats['owner_allocation_target_kas']} KAS")
        if stats['owner_target_met']:
            print("  OWNER TARGET MET!")
        time.sleep(0.1)

    print("\n--- Final Cumulative Stats ---")
    final_stats = rewards_mgr.get_cumulative_stats()
    for key, value in final_stats.items():
        if isinstance(value, float):
            print(f"  {key.replace('_', ' ').title()}: {value:,.8f}")
        else:
            print(f"  {key.replace('_', ' ').title()}: {value}")

    expected_total_dev_fee = total_sim_gross_kas * (RewardsManager.DEV_FEE_PERCENTAGE / 100.0)
    print(f"  Expected Total Dev Fee: {expected_total_dev_fee:.8f}")

    if abs(final_stats['cumulative_dev_fee_kas'] - expected_total_dev_fee) > 0.0000001:
        print("\033[91mError in dev fee calculation!\033[0m")

    if final_stats['owner_target_met']:
         if abs(final_stats['cumulative_owner_allocation_kas'] - final_stats['owner_allocation_target_kas']) > 0.0000001:
              print("\033[91mError: Owner target met but allocation amount mismatch!\033[0m")

    print("\n--- Test Complete ---")
