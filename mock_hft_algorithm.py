import time
import random

def get_current_market_price():
    """Simulates fetching the current market mid-price from an exchange order book."""
    # Simulating a stock price hovering around $150
    return round(random.uniform(149.80, 150.20), 2)

class HighFrequencyMarketMaker:
    """
    A simplified simulation of an HFT Market Making algorithm.
    The goal is to quote a bid and an ask price slightly above and below 
    the market price to capture the 'spread' as profit.
    """
    def __init__(self, spread_tolerance=0.03, inventory_limit=100):
        self.spread_tolerance = spread_tolerance
        self.inventory_limit = inventory_limit
        self.current_inventory = 0
        self.cash = 10000.0  # Starting capital

    def calculate_quotes(self, market_price):
        """Calculates bid (buy) and ask (sell) prices."""
        
        # Inventory Risk Management: Skew quotes based on how much stock we hold.
        # If we hold too much stock, lower both prices to encourage selling and discourage buying.
        inventory_skew = (self.current_inventory / self.inventory_limit) * 0.05
        
        bid_price = market_price - self.spread_tolerance - inventory_skew
        ask_price = market_price + self.spread_tolerance - inventory_skew
        
        return round(bid_price, 2), round(ask_price, 2)

    def evaluate_and_trade(self):
        """Simulates the microsecond decision-making loop."""
        market_price = get_current_market_price()
        bid, ask = self.calculate_quotes(market_price)
        
        # Mocking microsecond timestamps for the output
        ms_timestamp = int(time.time() * 1000) % 1000
        
        print(f"[{time.strftime('%H:%M:%S')}.{ms_timestamp:03d}] "
              f"Market Mid: ${market_price:.2f} | Quoting -> Bid: ${bid:.2f}, Ask: ${ask:.2f} | Inventory: {self.current_inventory}")
        
        # Simulate the market executing against our resting limit orders
        market_action = random.choice(["hit_bid", "lift_ask", "nothing", "nothing"])
        
        if market_action == "hit_bid" and self.current_inventory < self.inventory_limit:
            # Another trader sold to us at our bid price
            trade_qty = 10
            self.current_inventory += trade_qty
            self.cash -= bid * trade_qty
            print(f"   ⚡ Executed BUY  {trade_qty} shares at ${bid:.2f}")
            
        elif market_action == "lift_ask" and self.current_inventory > -self.inventory_limit:
            # Another trader bought from us at our ask price
            trade_qty = 10
            self.current_inventory -= trade_qty
            self.cash += ask * trade_qty
            print(f"   ⚡ Executed SELL {trade_qty} shares at ${ask:.2f}")

if __name__ == "__main__":
    print("======================================================")
    print("Initiating High-Frequency Market Maker (Simulated)")
    print("Target Execution Latency: < 50 Microseconds")
    print("======================================================")
    
    algo = HighFrequencyMarketMaker()
    
    try:
        # Run the trading loop for a limited series of 'ticks'
        for i in range(15):
            algo.evaluate_and_trade()
            # Sleeping to make the console output readable for the demonstration. 
            # Real algorithms do NOT sleep!
            time.sleep(0.4) 
            
    except KeyboardInterrupt:
        print("\nAlgorithm halted by user.")
        
    finally:
        print("\n======================================================")
        print("Trading Session Terminated.")
        print(f"Final Inventory Held: {algo.current_inventory} shares")
        print(f"Final Cash Balance: ${algo.cash:.2f}")
        
        # Calculate final estimated profit/loss based on current market value
        final_value = algo.cash + (algo.current_inventory * get_current_market_price())
        profit = final_value - 10000.0
        
        print(f"Estimated Gross PnL: ${profit:.2f}")
        print("======================================================")
