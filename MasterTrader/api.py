# api.py

from fastapi import FastAPI
from threading import Thread, Event
from fastapi.middleware.cors import CORSMiddleware
import trader  

app = FastAPI()

# for local testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict to ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Flag to control whether the bot is running
bot_running = Event()
bot_running.set()  # Start in running state

# Background thread that runs the bot
def trading_loop():
    print("Trading loop started in background.")
    while True:
        if bot_running.is_set():
            price = trader.fetch_mock_price()
            action = trader.check_signal()
            trader.execute_trade(trader.state, action, price)
            print(f"Loop: {action} at {price}")
        else:
            print("Bot paused.")
        # Sleep regardless of state
        import time
        time.sleep(5)

# Start background thread when API launches
@app.on_event("startup")
def start_bot():
    t = Thread(target=trading_loop, daemon=True)
    t.start()

@app.get("/")
def root():
    return {"message": "Trading Bot API is running"}

@app.get("/portfolio")
def get_portfolio():
    return trader.state.as_dict()

@app.get("/trades")
def get_trades():
    return trader.state.trade_history

@app.post("/pause")
def pause_bot():
    bot_running.clear()
    return {"status": "paused"}

@app.post("/resume")
def resume_bot():
    bot_running.set()
    return {"status": "running"}
