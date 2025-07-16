# brains.py

import random
import time
from datetime import datetime

class BotState:
    def __init__(self, initial_cash=10000):
        self.cash = initial_cash
        self.position = 0  # Number of shares
        self.avg_price = 0  # Average price per share held
        self.trade_history = []

    def as_dict(self):
        return {
            "cash": self.cash,
            "position": self.position,
            "avg_price": self.avg_price,
            "trade_history": self.trade_history[-10:]  # last 10 trades
        }

def fetch_mock_price():
    """Simulate getting the current price."""
    return round(random.uniform(90, 110), 2)

def check_signal():
    """Randomly decide to buy, sell, or hold."""
    roll = random.random()
    if roll < 0.3:
        return "buy"
    elif roll < 0.6:
        return "sell"
    else:
        return "hold"

def execute_trade(state: BotState, action: str, price: float):
    """Update cash and positions based on the action."""
    quantity = 10  # Fixed lot size

    if action == "buy":
        cost = quantity * price
        if state.cash >= cost:
            prev_position_value = state.position * state.avg_price
            state.position += quantity
            # Update avg price
            state.avg_price = (
                prev_position_value + cost
            ) / state.position
            state.cash -= cost
            state.trade_history.append({
                "time": datetime.utcnow().isoformat(),
                "action": "buy",
                "price": price,
                "quantity": quantity
            })
            print(f"BUY {quantity} @ {price}")

    elif action == "sell":
        if state.position >= quantity:
            proceeds = quantity * price
            state.position -= quantity
            state.cash += proceeds
            state.trade_history.append({
                "time": datetime.utcnow().isoformat(),
                "action": "sell",
                "price": price,
                "quantity": quantity
            })
            print(f"SELL {quantity} @ {price}")

    else:
        print("HOLD")


state = BotState()  # Global state instance

def main_loop():
    print("Starting trading bot...")
    try:
        while True:
            price = fetch_mock_price()
            print(f"\nCurrent price: {price}")

            action = check_signal()
            execute_trade(state, action, price)

            print(f"Cash: {state.cash:.2f}, Position: {state.position}, Avg Price: {state.avg_price:.2f}")

            time.sleep(5)

    except KeyboardInterrupt:
        print("Bot stopped by user.")

if __name__ == "__main__":
    main_loop()

