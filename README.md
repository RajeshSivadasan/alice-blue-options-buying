<h1>Nifty / BankNifty Options buying algo developed in python using the SuperTrend indicator for the NSE exchange using the Alice Blue broker API</h1><br>
  <br>Join Telegram channel <a href="https://t.me/rajeshsivadasanalgo">rajeshsivadasanalgo</a> to get live trading performance
<br>
<b>Follow the below steps to get the algo up and running:</b>
<br>
1. Copy all the three files in a same folder<br>
2. Update the user credentials and preferences in the ab_options.ini<br>
3. Install the below dependencies:<br>
   pip3 install pya3<br>
   pip3 install pycryptodome<br>
4. Run the algo using from the commandline using the below command:<br>
   python3 ab_options.py
<br>
<br>
Below are the settings with default values and their descriptions for the .ini file:<br>
<br>[tokens]
<br>uid = XXXXXX  (Alice Blue UserID/Client ID)
<br>pwd = XXXXXX  (Password)
<br>twofa = XXXXXX  (Year of Birth)
<br>totp_key = XXXXXXXXXXXXXXXXXX (Time based OTP key)
<br>api_key = XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX (API Key)
<br>autologin_date = 2022-12-22 (Optional. Autologin date , managed by Algo, no need to update)
<br>bot_token = bot1821162929:XXXXXXXXXXXXXXXXXXXXXXXX  (Telegram Bot token ID, used for sending log messages as chat)
<br>chat_id = XXXXXX  (Telegram Chat ID to which algo messages needs to be sent)
<br>channel_id =  (Optional. Telegram Channel ID to which Algo messages needs to be sent)
<br>enable_bg_process = 1 (Activates the background process which you can interact with to update the realtime algo settings)
<br>log_to_file = 1 (Enable logging to the log file)

<br>[realtime]  (Below are the realtime settings which can be changed during the live market also and will be captured by the Algo)
<br>trade_nfo = 1 (Enable(1)/Disable(0) Nifty trading)
<br>trade_bank = 1  (Enable(1)/Disable(0) BankNifty trading)
<br>enablebo2_nifty = 0 (Enable(1)/Disable(0) second Bracket Order for Nifty)
<br>enablebo3_nifty = 0 (Enable(1)/Disable(0) third Bracket Order for Nifty)
<br>enablebo2_bank = 0  (Enable(1)/Disable(0) second Bracket Order for BankNifty)
<br>enablebo3_bank = 0  (Enable(1)/Disable(0) third Bracket Order for BankNifty)
<br>nifty_sl = 30.0 (Stop Loss points for Nifty orders)
<br>bank_sl = 40.0  (Stop Loss points for BankNifty orders)
<br>mtm_sl = -5000  (MTM/PNL loss amount after which Algo will stop trading)
<br>mtm_target = 50000  (MTM/PNL profit amount after which Algo will stop trading)
<br>export_data = 0 (Export Nifty/BankNifty data to CSV file in between the Algo execution)
<br>nifty_bo1_qty = 50  (Bracket Order quantity for the first Nifty Bracket Order)
<br>nifty_bo2_qty = 50  (Bracket Order quantity for the second Nifty Bracket Order)
<br>nifty_bo3_qty = 50  (Bracket Order quantity for the third Nifty Bracket Order)
<br>bank_bo1_qty = 25 (Bracket Order quantity for the first BankNifty Bracket Order)
<br>bank_bo2_qty = 25 (Bracket Order quantity for the second BankNifty Bracket Order)
<br>bank_bo3_qty = 25 (Bracket Order quantity for the second BankNifty Bracket Order)
<br>nifty_ord_type = BO (Nifty Order Type. BO/MIS Bracket Order or MIS order)
<br>bank_ord_type = BO  (BankNifty Order Type. BO/MIS Bracket Order or MIS order)
<br>nifty_limit_price_offset = -10  (Price to be added to the Nifty LTP when the signal is generated)
<br>bank_limit_price_offset = -30 (Price to be added to the BankNifty LTP when the signal is generated)
<br>nifty_strike_ce_offset = -200 (Strike to be added to ATM Strike price for Nifty Call Options)
<br>nifty_strike_pe_offset = 200  (Strike to be added to ATM Strike price for Nifty Put Options)
<br>bank_strike_ce_offset = -100  (Strike to be added to ATM Strike price for BankNifty Call Options)
<br>bank_strike_pe_offset = 100 (Strike to be added to ATM Strike price for BankNifty Put Options)
<br>tick_processing_sleep_secs = 9 (Wait or sleep time for the main tick processing loop. Can reduce if the processing time alert is displayed.) 

<br>[info]
<br>olhc_duration = 3 (Candle time interval in minutes e.g 3 for 3min candle. Min recommended is 2)
<br>nifty_lot_size = 50 (Standard Exchange lot size for Nifty)
<br>bank_lot_size = 25  (Standard Exchange lot size for BankNifty)
<br>nifty_tgt1 = 20.0 (First target points above Limit Price to be achieved for Nifty)
<br>nifty_tgt2 = 100.0  (Second target points above Limit Price to be achieved for Nifty, ensure enablebo2_nifty=1 for this to work)
<br>nifty_tgt3 = 300.0  (Third target points above Limit Price to be achieved for Nifty, ensure enablebo3_nifty=1 for this to work)
<br>bank_tgt1 = 20.0
<br>bank_tgt2 = 100.0
<br>bank_tgt3 = 600.0
<br>nifty_tsl = 40 
<br>bank_tsl = 40
<br>nifty_sqoff_time = 1515
<br>use_rsi = 1
<br>use_rsi_roc = 1 (Enable(1)/Disable(0) RSI Rate of change check if consistent as per trend)
<br>rsi_period = 7
<br>rsi_buy_param = 25
<br>rsi_sell_param = 75
<br>enable_nfo = 0
<br>enable_bank = 0
<br>file_nifty = 
<br>file_bank = 
<br>no_of_trades_limit = 10
<br>weekly_expiry_holiday_dates = 2021-08-19,2021-11-04
<br>init_sleep_seconds = 1
<br>pending_ord_limit_mins = 30
<br>enable_nfo_data = 1
<br>enable_bank_data = 1
<br>nifty_trade_start_time = 920
<br>nifty_trade_end_time = 1440
<br>nifty_no_trade_zones = [(900,925),(1100,1330)]
<br>sl_wait_time = 600 (Seconds till algo needs to wait for the limit order to be completed post which the order would be cancelled. Default is 10 mins/600 seconds)
<br>nifty_limit_price_low = 50
<br>nifty_limit_price_high = 400
<br>bank_limit_price_low = 50
<br>bank_limit_price_high = 470
<br>get_opt_ltp_wait_seconds = 3
