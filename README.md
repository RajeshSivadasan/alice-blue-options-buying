
# Algorithmic Trading Strategy: Nifty/BankNifty Options Buying Bot Developed in Python with SuperTrend Indicator, Utilizing Alice Blue Broker API for NSE Exchange


> **Disclaimer:** This code is intended for educational purposes only. Conduct your own research before making any investment or trading decisions. It is important to note that this code is not registered or approved by SEBI.


**Join Telegram Channel for Live Trading Performance** [@rajeshsivadasanalgo](https://t.me/rajeshsivadasanalgo)

To get the algorithm up and running, follow these steps:

1. Copy all three files into the same folder.
2. Update user credentials and preferences in `ab_options.ini`.
3. Install the required dependencies using the following commands:
    ```bash
    pip3 install pya3
    pip3 install pycryptodome
    ```
4. Run the algorithm from the command line using the following command:
    ```bash
    python3 ab_options.py
    ```

**Below are the settings along with their default values and descriptions for the `.ini` file:**

## Tokens:  

| **Key**                        | **Value**                               | **Optional** | **Other**                                                                                                          |
|--------------------------------|-----------------------------------------|--------------|--------------------------------------------------------------------------------------------------------------------|
| **uid**                        | XXXXXX                                  |              | (Alice Blue UserID/Client ID)                                                                                      |
| **pwd**                        | XXXXXX                                  |              | (Password)                                                                                                         |
| **twofa**                      | XXXXXX                                  |              |  (Year of Birth)                                                                                                   |
| **totp_key**                   | XXXXXXXXXXXXXXXXXX                      |              |  (Time based OTP key) - [Docs](https://www.youtube.com/watch?v=dxrHgmuSukE)                                        |
| **api_key**                    | (API Key)                               |              | API KEY - [Docs](https://v2api.aliceblueonline.com/introduction)                                                   |
| **autologin_date**             | 22/12/22                                |              | (Optional. Autologin date , managed by Algo, no need to update)                                                    |
| **bot_token**                  | bot1821162929:XXXXXXXXXXXXXXXXXXXXXXXX  |              | (Telegram Bot token ID, used for sending log messages as chat)                                                     |
| **chat_id**                    | XXXXXX                                  |              |  (Telegram Chat ID to which algo messages needs to be sent)                                                        |
| **channel_id**                 |                                         | YES          | Telegram Channel ID to which Algo messages needs to be sent                                                        |
| **enable_bg_process**          | 1                                       |              | (Activates the background process which you can interact with to update the realtime algo settings)                |
| **log_to_file**                | 1                                       |              | (Enable logging to the log file)                                                                                   |


### Realtime: Below are the realtime settings which can be changed during the live market also and will be captured by the Algo

| **Key**                        | **Value**                               | **Optional** | **Other**                                                                                                          |
|--------------------------------|-----------------------------------------|--------------|--------------------------------------------------------------------------------------------------------------------|
| **trade_nfo**                  | 1                                       |              | (Enable(1)/Disable(0) Nifty trading)                                                                               |
| **trade_bank**                 | 1                                       |              |  (Enable(1)/Disable(0) BankNifty trading)                                                                          |
| **enablebo2_nifty**            | 0                                       |              | 0 (Enable(1)/Disable(0) second Bracket Order for Nifty)                                                            |
| **enablebo3_nifty**            | 0                                       |              | 0 (Enable(1)/Disable(0) third Bracket Order for Nifty)                                                             |
| **enablebo2_bank**             | 0                                       |              | 0 (Enable(1)/Disable(0) second Bracket Order for BankNifty)                                                        |
| **enablebo3_bank**             | 0                                       |              | 0 (Enable(1)/Disable(0) third Bracket Order for BankNifty)                                                         |
| **nifty_sl**                   | 0                                       |              | 30.0 (Stop Loss points for Nifty orders)                                                                           |
| **bank_sl**                    | 40                                      |              | 40.0 (Stop Loss points for BankNifty orders)                                                                       |
| **mtm_sl**                     | -5000                                   |              | -5000 (MTM/PNL loss amount after which Algo will stop trading)                                                     |
| **mtm_target**                 | 50000                                   |              | 50000 (MTM/PNL profit amount after which Algo will stop trading)                                                   |
| **export_data**                | 0                                       |              | 0 (Export Nifty/BankNifty data to CSV file in between the Algo execution)                                          |
| **nifty_bo1_qty**              | 50                                      |              | 50 (Bracket Order quantity for the first Nifty Bracket Order)                                                      |
| **nifty_bo2_qty**              | 50                                      |              | 50 (Bracket Order quantity for the second Nifty Bracket Order)                                                     |
| **nifty_bo3_qty**              | 50                                      |              | 50 (Bracket Order quantity for the third Nifty Bracket Order)                                                      |
| **bank_bo1_qty**               | 25                                      |              | 25 (Bracket Order quantity for the first BankNifty Bracket Order)                                                  |
| **bank_bo2_qty**               | 25                                      |              | 25 (Bracket Order quantity for the second BankNifty Bracket Order)                                                 |
| **bank_bo3_qty**               | 25                                      |              | 25 (Bracket Order quantity for the second BankNifty Bracket Order)                                                 |
| **nifty_ord_type**             | BO                                      |              | BO (Nifty Order Type. BO/MIS Bracket Order or MIS order)                                                           |
| **bank_ord_type**              | BO                                      |              | BO (BankNifty Order Type. BO/MIS Bracket Order or MIS order)                                                       |
| **nifty_limit_price_offset**   | -10                                     |              | -10 (Price to be added to the Nifty LTP when the signal is generated)                                              |
| **bank_limit_price_offset**    | -30                                     |              | -30 (Price to be added to the BankNifty LTP when the signal is generated)                                          |
| **nifty_strike_ce_offset**     | -200                                    |              | -200 (Strike to be added to ATM Strike price for Nifty Call Options)                                               |
| **nifty_strike_pe_offset**     | 200                                     |              | 200 (Strike to be added to ATM Strike price for Nifty Put Options)                                                 |
| **bank_strike_ce_offset**      | -100                                    |              | -100 (Strike to be added to ATM Strike price for BankNifty Call Options)                                           |
| **bank_strike_pe_offset**      | 100                                     |              | 100 (Strike to be added to ATM Strike price for BankNifty Put Options)                                             |
| **tick_processing_sleep_secs** | 9                                       |              | 9 (Wait or sleep time for the main tick processing loop. Can reduce if the processing time alert is displayed.)    |

### Info: 

| **Key**                        | **Value**                               | **Optional** | **Other**                                                                                                          |
|--------------------------------|-----------------------------------------|--------------|--------------------------------------------------------------------------------------------------------------------|
| **olhc_duration**              | 3                                       |              | (Candle time interval in minutes e.g 3 for 3min candle. Min recommended is 2)                                    |
| **nifty_lot_size**             | 50                                      |              | (Standard Exchange lot size for Nifty)                                                                          |
| **bank_lot_size**              | 25                                      |              | (Standard Exchange lot size for BankNifty)                                                                      |
| **nifty_tgt1**                 | 20                                      |              | (First target points above Limit Price to be achieved for Nifty)                                              |
| **nifty_tgt2**                 | 100                                     |              | (Second target points above Limit Price to be achieved for Nifty, ensure enablebo2_nifty=1 for this to work) |
| **nifty_tgt3**                 | 300                                     |              | (Third target points above Limit Price to be achieved for Nifty, ensure enablebo3_nifty=1 for this to work)  |
| **bank_tgt1**                  | 20                                      |              |                                                                                                                    |
| **bank_tgt2**                  | 100                                     |              |                                                                                                                    |
| **bank_tgt3**                  | 600                                     |              |                                                                                                                    |
| **nifty_tsl**                  | 40                                      |              |                                                                                                                    |
| **bank_tsl**                   | 40                                      |              |                                                                                                                    |
| **nifty_sqoff_time**           | 1515                                    |              |                                                                                                                    |
| **use_rsi**                    | 1                                       |              |                                                                                                                    |
| **use_rsi_roc**                | 1                                       |              | (Enable(1)/Disable(0) RSI Rate of change check if consistent as per trend)                                       |
| **rsi_period**                 | 7                                       |              |                                                                                                                    |







# Algorithmic Trading Strategy: Nifty/BankNifty Options Buying Bot Developed in Python with SuperTrend Indicator, Utilizing Alice Blue Broker API for NSE Exchange

> **Disclaimer:** This code is intended for educational purposes only. Conduct your own research before making any investment or trading decisions. It is important to note that this code is not registered or approved by SEBI.

**Join Telegram Channel for Live Trading Performance** [@rajeshsivadasanalgo](https://t.me/rajeshsivadasanalgo)

To get the algorithm up and running, follow these steps:

1. Copy all three files into the same folder.
2. Update user credentials and preferences in `ab_options.ini`.
3. Install the required dependencies using the following commands:
    ```bash
    pip3 install pya3
    pip3 install pycryptodome
    ```
4. Run the algorithm from the command line using the following command:
    ```bash
    python3 ab_options.py
    ```

**Below are the settings along with their default values and descriptions for the `.ini` File:**

## Tokens:  

| **Key**                        | **Value**                               | **Optional** | **Other**                                                                                                          |
|--------------------------------|-----------------------------------------|--------------|--------------------------------------------------------------------------------------------------------------------|
| **uid**                        | XXXXXX                                  |              | (Alice Blue UserID/Client ID)                                                                                      |
| **pwd**                        | XXXXXX                                  |              | (Password)                                                                                                         |
| **twofa**                      | XXXXXX                                  |              |  (Year of Birth)                                                                                                   |
| **totp_key**                   | XXXXXXXXXXXXXXXXXX                      |              |  (Time based OTP key) - [Docs](https://www.youtube.com/watch?v=dxrHgmuSukE)                                        |
| **api_key**                    | (API Key)                               |              | API KEY - [Docs](https://v2api.aliceblueonline.com/introduction)                                                   |
| **autologin_date**             | 22/12/22                                |              | (Optional. Autologin date , managed by Algo, no need to update)                                                    |
| **bot_token**                  | bot1821162929:XXXXXXXXXXXXXXXXXXXXXXXX  |              | (Telegram Bot token ID, used for sending log messages as chat)                                                     |
| **chat_id**                    | XXXXXX                                  |              |  (Telegram Chat ID to which algo messages needs to be sent)                                                        |
| **channel_id**                 |                                         | YES          | Telegram Channel ID to which Algo messages needs to be sent                                                        |
| **enable_bg_process**          | 1                                       |              | (Activates the background process which you can interact with to update the realtime algo settings)                |
| **log_to_file**                | 1                                       |              | (Enable logging to the log file)                                                                                   |


## Realtime: 

Below are the realtime settings which can be changed during the live market also and will be captured by the Algo.

| **Key**                        | **Value**                               | **Optional** | **Other**                                                                                                          |
|--------------------------------|-----------------------------------------|--------------|--------------------------------------------------------------------------------------------------------------------|
| **trade_nfo**                  | 1                                       |              | (Enable(1)/Disable(0) Nifty trading)                                                                               |
| **trade_bank**                 | 1                                       |              |  (Enable(1)/Disable(0) BankNifty trading)                                                                          |
| **enablebo2_nifty**            | 0                                       |              | 0 (Enable(1)/Disable(0) second Bracket Order for Nifty)                                                            |
| **enablebo3_nifty**            | 0                                       |              | 0 (Enable(1)/Disable(0) third Bracket Order for Nifty)                                                             |
| **enablebo2_bank**             | 0                                       |              | 0 (Enable(1)/Disable(0) second Bracket Order for BankNifty)                                                        |
| **enablebo3_bank**             | 0                                       |              | 0 (Enable(1)/Disable(0) third Bracket Order for BankNifty)                                                         |
| **nifty_sl**                   | 0                                       |              | 30.0 (Stop Loss points for Nifty orders)                                                                           |
| **bank_sl**                    | 40                                      |              | 40.0 (Stop Loss points for BankNifty orders)                                                                       |
| **mtm_sl**                     | -5000                                   |              | -5000 (MTM/PNL loss amount after which Algo will stop trading)                                                     |
| **mtm_target**                 | 50000                                   |              | 50000 (MTM/PNL profit amount after which Algo will stop trading)                                                   |
| **export_data**                | 0                                       |              | 0 (Export Nifty/BankNifty data to CSV file in between the Algo execution)                                          |
| **nifty_bo1_qty**              | 50                                      |              | 50 (Bracket Order quantity for the first Nifty Bracket Order)                                                      |
| **nifty_bo2_qty**              | 50                                      |              | 50 (Bracket Order quantity for the second Nifty Bracket Order)                                                     |
| **nifty_bo3_qty**              | 50                                      |              | 50 (Bracket Order quantity for the third Nifty Bracket Order)                                                      |
| **bank_bo1_qty**               | 25                                      |              |

## Info: 

| **Key**                        | **Value**                               | **Optional** | **Other**                                                                                                          |
|--------------------------------|-----------------------------------------|--------------|--------------------------------------------------------------------------------------------------------------------|
| **olhc_duration**              | 3                                       |              | (Candle time interval in minutes e.g 3 for 3min candle. Min recommended is 2)                                    |
| **nifty_lot_size**             | 50                                      |              | (Standard Exchange lot size for Nifty)                                                                          |
| **bank_lot_size**              | 25                                      |              | (Standard Exchange lot size for BankNifty)                                                                      |
| **nifty_tgt1**                 | 20                                      |              | (First target points above Limit Price to be achieved for Nifty)                                              |
| **nifty_tgt2**                 | 100                                     |              | (Second target points above Limit Price to be achieved for Nifty, ensure enablebo2_nifty=1 for this to work) |
| **nifty_tgt3**                 | 300                                     |              | (Third target points above Limit Price to be achieved for Nifty, ensure enablebo3_nifty=1 for this to work)  |
| **bank_tgt1**                  | 20                                      |              |

