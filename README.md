<h1>Nifty / BankNifty Options buying algo developed in python using the SuperTrend indicator for the NSE exchange using the Alice Blue broker API</h1><br>
  
<b>Follow the below steps to get the algo up and running:</b>
1. Copy all the three files in a same folder
2. Update the user credentials and preferences in the ab_options.ini
3. Install the below dependencies:<br>
   ```pip3 install pya3```<br>
   ```pip3 install pycryptodome```
4. Run the algo using from the commandline using the below command:<br>
```python3 ab_options.py```

Below are the settings with default values and their descriptions for the .ini file:

[tokens]
uid = XXXXXX  (Alice Blue UserID/Client ID)
pwd = XXXXXX  (Password)
twofa = XXXXXX  (Year of Birth)
totp_key = XXXXXXXXXXXXXXXXXX (Time based OTP key)
api_key = XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX (API Key)
autologin_date = 2022-12-22 (Optional. Autologin date , managed by Algo, no need to update)
bot_token = bot1821162929:XXXXXXXXXXXXXXXXXXXXXXXX  (Telegram Bot token ID, used for sending log messages as chat)
chat_id = XXXXXX  (Telegram Chat ID to which algo messages needs to be sent)
channel_id =  (Optional. Telegram Channel ID to which Algo messages needs to be sent)
enable_bg_process = 1 (Activates the background process which you can interact with to update the realtime algo settings)
log_to_file = 1 (Enable logging to the log file)

[realtime]  (Below are the realtime settings which can be changed during the live market and will be captured by the Algo)
trade_nfo = 1 (Enable(1)/Disable(0) Nifty trading)
trade_bank = 1  (Enable(1)/Disable(0) BankNifty trading)
enablebo2_nifty = 0 (Enable(1)/Disable(0) second Bracket Order for Nifty)
enablebo3_nifty = 0 (Enable(1)/Disable(0) third Bracket Order for Nifty)
enablebo2_bank = 0  (Enable(1)/Disable(0) second Bracket Order for BankNifty)
enablebo3_bank = 0  (Enable(1)/Disable(0) third Bracket Order for BankNifty)
nifty_sl = 30.0 (Stop Loss points for Nifty orders)
bank_sl = 40.0  (Stop Loss points for BankNifty orders)
mtm_sl = -5000  (MTM/PNL loss amount after which Algo will stop trading)
mtm_target = 50000  (MTM/PNL profit amount after which Algo will stop trading)
export_data = 0 (Export Nifty/BankNifty data to CSV file in between the Algo execution)
nifty_bo1_qty = 50  (Bracket Order quantity for the first Nifty Bracket Order)
nifty_bo2_qty = 50  (Bracket Order quantity for the second Nifty Bracket Order)
nifty_bo3_qty = 50  (Bracket Order quantity for the third Nifty Bracket Order)
bank_bo1_qty = 25 (Bracket Order quantity for the first BankNifty Bracket Order)
bank_bo2_qty = 25 (Bracket Order quantity for the second BankNifty Bracket Order)
bank_bo3_qty = 25 (Bracket Order quantity for the second BankNifty Bracket Order)
sl_buffer = 5 
nifty_ord_type = BO
bank_ord_type = BO
nifty_limit_price_offset = -5
bank_limit_price_offset = -10
nifty_strike_ce_offset = -200
nifty_strike_pe_offset = 200
bank_strike_ce_offset = -100
bank_strike_pe_offset = 100

[info]
olhc_duration = 3
nifty_lot_size = 50
bank_lot_size = 25
nifty_tgt1 = 20.0
nifty_tgt2 = 100.0
nifty_tgt3 = 300.0
bank_tgt1 = 20.0
bank_tgt2 = 100.0
bank_tgt3 = 600.0
nifty_tsl = 40
bank_tsl = 40
nifty_sqoff_time = 1515
use_rsi = 1
rsi_period = 7
rsi_buy_param = 25
rsi_sell_param = 75
enable_nfo = 0
enable_bank = 0
file_nifty = ./data/NIFTY_OPT_20220110_153103.csv
file_bank = 
no_of_trades_limit = 10
weekly_expiry_holiday_dates = 2021-08-19,2021-11-04
init_sleep_seconds = 1
pending_ord_limit_mins = 30
enable_nfo_data = 1
enable_bank_data = 1
nifty_trade_start_time = 920
nifty_trade_end_time = 1440
nifty_no_trade_zones = [(900,925),(1100,1330)]
sl_wait_time = 100
nifty_limit_price_low = 50
nifty_limit_price_high = 400
bank_limit_price_low = 50
bank_limit_price_high = 470
get_opt_ltp_wait_seconds = 3
