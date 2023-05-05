# pylint: disable=unused-wildcard-import
# Refer to https://github.com/RajeshSivadasan/alice-blue-futures/blob/main/ab.py verison comments for previous changes

# ---- Dependencies ----
# pip3 install pya3
# pip3 install pycryptodome

# ---- Version History ----
#v7.3.8 New AliceBlue login process implemented
#v7.4.0 New AliceBlue API V2 implemented
#v7.4.1 line 980, fixed banknifty SL taking as nifty SL issue
#v7.4.2 Fixed trade_limit_reached() generating issue due to the new API update miss here.
#v7.4.3 Made changes in the strike selection logic Strike = ATM  + Offset eg for CALL ITM 200pts = ATM - 200 (offset = -200), OTM 200pts = ATM + 200 (offset = 200); For PUT ITM 200pts = ATM + 200 
#v7.4.4 Fixed type object 'datetime.time' has no attribute 'sleep' at line 439
#v7.4.5 Fixed KeyError: 'Emsg'
#v7.4.6 Added feature to save and read previous day data to maintain continuity in the supertrend indicator otherwise we have to wait for 6 candles to complete for the indicator value generation 
#v7.4.7 Fixed cancel_all_orders issue
#v7.4.8 updated MTM logic in check_MTM_Limit() and changed the loop logic to check MTM after every 9 seconds 
#v7.4.9 Added RSI indicator support and created generic get_buy_sell() function to process the indicators and generate signal; Fixed banknifty previous day data load issue
#v7.5.0 Added "use_rsi" option to enable or disable use of RSI indictor along with supertrend
# v7.5.1 Fixed TypeError: string indices must be integers in close_all_orders(); file_nifty name updated
# v7.5.2 file_nifty name updated, added all_variables printing, removed logging in get_buy_sell()
# v7.5.3 Fixed KeyError: 'NOrdNo' in buy_nifty_options() line 594 
# v7.5.4 Publish to channel functionality added. channel_is is @channel name from the channel link. e.g if channel link is https://t.me/mychannelname then channel_id will be @mychannelname, Added messages in the algo for publishing performance data to the channel, Included option name in the signal log
# v7.5.5 Fixed messages not getting logged in case of MIS orders
# v7.5.6 Fixed KeyError: 'data' @ line 451, changed get_options() to wait till ce/pe ltp appears, removed mkt timimgs check from the loop and moved it before it  
# v7.5.7 check_orders() tsl print changes
# v7.5.8 Removed sl_buffer parameter as its not used. SL to be adjusted using the SL parameters;
# v7.5.9 Fixed expiry date calculation issue due to datetime module
# v7.6.0 Debug in progress. Added comments to check_MTM_limit() and check_orders(). Neeed to find a way to check if SL price is below ltp. 
# v7.6.1 Additional condition added in check_orders() to handle order fetch issues from the API 
# v7.6.2 Handled exception in check_orders() while processing alice.get_order_history()
# v7.6.3 dict_sl_orders.clear() / Clear internal orders dict if there are no open orders.
# v7.6.4 close_all_orders() called immediately after signal is generated. Added more logging in place_sl_order
# v7.6.5 close_all_orders(). Enabled closure of previous orders while creating new positions. Commented lot of logging.

# Last issue caused due to SL price set was above LTP i.e LTP came down drastically below the SL already. 
# May be a health check of SLs are required time to time or MTM needs to actually handle it. This time MTM check also failed. 
# Find a way to print all the setting using configparser loop
# 17070 : The Price is out of the LPP range
# alice.get_scrip_info(ins_nifty_ce)
version = "7.6.5" 

###### STRATEGY / TRADE PLAN #####
# Trading Style     : Intraday
# Trade Timing      : Morning 9:15 to 10:40 AM , After noon 1.30 PM to 3.30 PM (Can be set in the parameter)
# Trading Capital   : Rs 20,000
# Trading Qty       : 1 Lot for short goal, 1 lot long goal
# Premarket Routine : TBD
# Trading Goals     : Nifty(Short Goal = 20 Points, Long Goal = 200 pts with TSL)
# Time Frame        : 3 min Default (Can be changed through parameter)
# Entry Criteria    : Nifty50 Supertrend buy(CE)/Sell(PE)
# Exit Criteria     : BO Set for Target/SL, Exit CE position on Supertrend Sell/PE trigger, exit PE position the other way  
# Risk Capacity     : Taken care by BO
# Order Management  : BO orders else MIS/Normal(may need additional exit criteria)

# Supertrend Buy signal will trigger ATM CE buy
# Supertrend Sell signal will trigger ATM PE buy 
# Existing positions to be closed before order trigger
# For option price, ATM ltp CE and ATM ltp PE to be subscribed dynamically and stored in global variables
# Nifty option order trigger to be based on Nifty50 Index movement hence nifty50 dataframe required 
# BankNifty option order trigger to be based on BankNifty Index movement hence banknifty dataframe required to be maintained seperately

# ---- Open issues/tasks:
# Check use of float in place_order_BO() as it is working in ab.py without it
# Instead of check_trade_time_zone() plan for no_trade_zone() 
# Update Contract Symbol ab.update_contract_symbol(). If last friday is holiday this code dosent run and the symbol is not updated and the program fails
# Check if order parameters like order type and others can be paramterised
# Look at close pending orders, my not be efficient, exception handling and all
# WebSocket disconnection and subscription/tick loss issue. Upgraded the package  
# Option of MIS orders for bank to be added, maybe for nifty as well. Can test with nifty 
# check_MTM_Limit() limitation : if other nifty or bank scrips are traded this will messup the position
# trade_limit_reached() moved before check_pending_orders(). Need to check if this is the correct approach
# get_trade_price bo_level to be parameterised from .ini 0 , 1 (half of atr), 2 (~atr)
# If ATR > 10 or something activate BO3
# In ST up/down if ST_MEDIUM is down/Up - If high momentum (check rate of change) chances are it will break medium SL 
# Look at 3 min to 6 min crossover points , compare ST values of low and medium for possible override
# Return/Exit function after Postion check in buy/sell function fails 
# Look at df_nifty.STX.values; Can we use tail to get last n values in the list
# Can have few tasks to be taken care/check each min like MTM/Tradefalg check/set. This is apart from interval
# Delay of 146 secs, 57 secs, 15 secs etc seen. Check and Need to handle 
# Look at 5/10 mins trend, dont take positions against the trend
# Keep limit price at 10% from ST and Sl beyond 10% from ST
# Relook at supertrend multiplier=2.5 option instead of current 3
# NSE Premarket method values may not be current as bank open time is considered . Need to fetch this realtime around 915 
# May need try/catch in reading previous day datafile due to copy of ini file or failed runs
# Can look at frequency of data export through parameter, say 60,120,240 etc.. 

# Guidelines:
# TSL to be double of SL (Otherwise mostly SLs are hit as they tend to )
# SL will be hit in high volatility. SL may be set to ATR*3 or medium df Supertrend Value
# Always buy market, in case SL reverse and get out cost to cost. Market has to come up, but mind expiry :)  
# SLs are usually hit in volatile market, so see if you can use less qty and no SLs, especially bank.
# Dont go against the trend in any case. 
# Avoid manual trades

# To Manually run program in lunix use following command
# python3 ab_options.py &


# Release notes for ab_options.py

import sys
import threading
from pya3 import *
import numpy as np
import configparser
from datetime import datetime, date, timedelta

# Reduce position to cut loss if price is going against the trade, can close BO1

# Manual Activities
# Frequency - Monthly , Change Symbol of nifty/bank in .ini

# If log, data folder is not present create it
if not os.path.exists("./log") : os.makedirs("./log")
if not os.path.exists("./data") : os.makedirs("./data")


###################################
#      Logging method
###################################
# Custom logging: Default Info=1, data =0
def iLog(strLogText,LogType=1,sendTeleMsg=False,publishToChannel=False):
    '''0=data, 1=Info, 2-Warning, 3-Error, 4-Abort, 5-Signal(Buy/Sell) ,6-Activity/Task done

        sendTelegramMsg=True - Send Telegram message as well. 
        Do not use special characters like #,& etc  
    '''
    #0- Data format TBD; symbol, price, qty, SL, Tgt, TSL
    
    print(f"{datetime.now()}|{LogType}|{strLogText}",flush=True)
    
    if sendTeleMsg :
        try:
            requests.get("https://api.telegram.org/"+strBotToken+"/sendMessage?chat_id="+strChatID+"&text="+strLogText)
        except:
            iLog("Telegram message failed."+strLogText)

    if publishToChannel and channel_id:
        try:
            strLogText = f"[{ORDER_TAG}]{strLogText}"
            requests.get("https://api.telegram.org/"+strBotToken+"/sendMessage?chat_id="+channel_id+"&text="+strLogText)
        except:
            iLog("Telegram channel publish failed."+strLogText)

######################################
#       Initialise variables
######################################
supertrend_period = 7 #5 #7 #30 NOte: This changes the ATR period also
supertrend_multiplier = 2.5 #1.5 #3

INI_FILE = __file__[:-3]+".ini"              # Set .ini file name used for storing config info.
ORDER_TAG = __file__[:-3].split("/")[-1]   # Used as order tag while placing the orders to identify the source of orders windows \\, unix /

# Load parameters from the config file
cfg = configparser.ConfigParser()
cfg.read(INI_FILE)

# Enable logging to file, based on the settings 
log_to_file = int(cfg.get("tokens", "log_to_file"))
if log_to_file : sys.stdout = sys.stderr = open(r"./log/ab_options_" + datetime.now().strftime("%Y%m%d") +".log" , "a") 


# Set user profile; Access token and other user specific info from .ini will be pulled from this section
strChatID = cfg.get("tokens", "chat_id")
strBotToken = cfg.get("tokens", "bot_token")    #Bot include "bot" prefix in the token
channel_id = cfg.get("tokens", "channel_id").strip()

strMsg = f"Initialising {__file__} version={version}"
iLog(strMsg,sendTeleMsg=True)

iLog(f"Starting Algo {ORDER_TAG} version={version}",sendTeleMsg=False,publishToChannel=True)

# Get user credentials
susername = cfg.get("tokens", "uid")
spassword = cfg.get("tokens", "pwd")
api_key = cfg.get("tokens", "api_key")


# Below Realtime variables are loaded using get_realtime_config()
enableBO2_nifty = int(cfg.get("realtime", "enableBO2_nifty"))       # True = 1 (or non zero) False=0 
enableBO3_nifty = int(cfg.get("realtime", "enableBO3_nifty"))       # True = 1 (or non zero) False=0 
enableBO2_bank = int(cfg.get("realtime", "enableBO2_bank"))         # BankNifty ;True = 1 (or non zero) False=0 
enableBO3_bank = int(cfg.get("realtime", "enableBO3_bank"))         # BankNifty ;True = 1 (or non zero) False=0 
trade_nfo = int(cfg.get("realtime", "trade_nfo"))                   # Trade Nifty options. True = 1 (or non zero) False=0
trade_bank = int(cfg.get("realtime", "trade_bank"))                 # Trade Bank Nifty options. True = 1 (or non zero) False=0
nifty_sl = float(cfg.get("realtime", "nifty_sl"))                   # 15.0 ?
bank_sl = float(cfg.get("realtime", "bank_sl"))                     # 30.0 ?
mtm_sl = int(cfg.get("realtime", "mtm_sl"))                         # Overall Stop Loss Amount below which program exits all positions 
mtm_target = int(cfg.get("realtime", "mtm_target"))                 # Overall Profit Target Amount above which program exits all positions and doses not take any new positions
nifty_bo1_qty = int(cfg.get("realtime", "nifty_bo1_qty"))
nifty_bo2_qty = int(cfg.get("realtime", "nifty_bo2_qty"))
nifty_bo3_qty = int(cfg.get("realtime", "nifty_bo3_qty"))
bank_bo1_qty = int(cfg.get("realtime", "bank_bo1_qty"))
bank_bo2_qty = int(cfg.get("realtime", "bank_bo2_qty"))
bank_bo3_qty = int(cfg.get("realtime", "bank_bo3_qty"))
nifty_ord_type = cfg.get("realtime", "nifty_ord_type")      # BO / MIS
bank_ord_type = cfg.get("realtime", "bank_ord_type")      # MIS / BO

nifty_limit_price_offset = float(cfg.get("realtime", "nifty_limit_price_offset"))
bank_limit_price_offset = float(cfg.get("realtime", "bank_limit_price_offset"))

nifty_strike_ce_offset = float(cfg.get("realtime", "nifty_strike_ce_offset"))
nifty_strike_pe_offset = float(cfg.get("realtime", "nifty_strike_pe_offset"))
bank_strike_ce_offset = float(cfg.get("realtime", "bank_strike_ce_offset"))
bank_strike_pe_offset = float(cfg.get("realtime", "bank_strike_pe_offset"))

tick_processing_sleep_secs = int(cfg.get("realtime", "tick_processing_sleep_secs"))


#List of thursdays when its NSE holiday, hence reduce 1 day to get expiry date 
weekly_expiry_holiday_dates = cfg.get("info", "weekly_expiry_holiday_dates").split(",")

nifty_tgt1 = float(cfg.get("info", "nifty_tgt1"))   #30.0
nifty_tgt2 = float(cfg.get("info", "nifty_tgt2"))   #60.0 medium target
nifty_tgt3 = float(cfg.get("info", "nifty_tgt3"))   #150.0 high target
bank_tgt1 = float(cfg.get("info", "bank_tgt1"))     #30.0
bank_tgt2 = float(cfg.get("info", "bank_tgt2"))     #90.0
bank_tgt3 = float(cfg.get("info", "bank_tgt2"))     #200.0

olhc_duration = int(cfg.get("info", "olhc_duration"))   #3
nifty_sqoff_time = int(cfg.get("info", "nifty_sqoff_time")) #1512 time after which orders not to be processed and open orders to be cancelled

nifty_tsl = int(cfg.get("info", "nifty_tsl"))   #Trailing Stop Loss for Nifty
bank_tsl = int(cfg.get("info", "bank_tsl"))     #Trailing Stop Loss for BankNifty


# Below 2 are base Flag for nifty /bank nifty trading_which is used to reset daily(realtime) flags(trade_nfo,trade_bank) as 
# they might have been changed during the day in realtime 
enable_bank = int(cfg.get("info", "enable_bank"))                       # 1=Original flag for BANKNIFTY trading. Daily(realtime) flag to be reset eod based on this.  
enable_NFO = int(cfg.get("info", "enable_NFO"))                         # 1=Original flag for Nifty trading. Daily(realtime) flag to be reset eod based on this.

enable_bank_data = int(cfg.get("info", "enable_bank_data"))             # 1=CRUDE data subscribed, processed and saved/exported 
enable_NFO_data = int(cfg.get("info", "enable_NFO_data"))               # 1=NIFTY data subscribed, processed and saved/exported
file_nifty = cfg.get("info", "file_nifty")
file_bank = cfg.get("info", "file_bank")
no_of_trades_limit = int(cfg.get("info", "no_of_trades_limit"))         # 2 BOs trades per order; 6 trades for 3 orders
pending_ord_limit_mins = int(cfg.get("info", "pending_ord_limit_mins")) # Close any open orders not executed beyond the set limit

nifty_trade_start_time = int(cfg.get("info", "nifty_trade_start_time"))
nifty_trade_end_time = int(cfg.get("info", "nifty_trade_end_time"))
sl_wait_time = int(cfg.get("info", "sl_wait_time"))
nifty_limit_price_low = int(cfg.get("info", "nifty_limit_price_low"))
nifty_limit_price_high = int(cfg.get("info", "nifty_limit_price_high"))
bank_limit_price_low = int(cfg.get("info", "bank_limit_price_low"))
bank_limit_price_high = int(cfg.get("info", "bank_limit_price_high"))

use_rsi = int(cfg.get("info", "use_rsi"))
rsi_period = int(cfg.get("info", "rsi_period"))
rsi_buy_param = int(cfg.get("info", "rsi_buy_param"))
rsi_sell_param = int(cfg.get("info", "rsi_sell_param"))



all_variables = f"enableBO2_nifty={enableBO2_nifty}\nenableBO3_nifty={enableBO3_nifty}\nenableBO2_bank={enableBO2_bank}\nenableBO3_bank={enableBO3_bank}\ntrade_nfo={trade_nfo}\ntrade_bank={trade_bank}\nnifty_sl={nifty_sl}\nbank_sl={bank_sl}\nmtm_sl={mtm_sl}\nmtm_target={mtm_target}\nnifty_bo1_qty={nifty_bo1_qty}\nnifty_bo2_qty={nifty_bo2_qty}\nnifty_bo3_qty={nifty_bo3_qty}\nbank_bo1_qty={bank_bo1_qty}\nbank_bo2_qty={bank_bo2_qty}\nbank_bo3_qty={bank_bo3_qty}\nnifty_ord_type={nifty_ord_type}\nbank_ord_type={bank_ord_type}\nnifty_limit_price_offset={nifty_limit_price_offset}\nbank_limit_price_offset={bank_limit_price_offset}\nnifty_strike_ce_offset={nifty_strike_ce_offset}\nnifty_strike_pe_offset={nifty_strike_pe_offset}\nbank_strike_ce_offset={bank_strike_ce_offset}\nbank_strike_pe_offset={bank_strike_pe_offset}\nweekly_expiry_holiday_dates={weekly_expiry_holiday_dates}\nnifty_tgt1={nifty_tgt1}\nnifty_tgt2={nifty_tgt2}\nnifty_tgt3={nifty_tgt3}\nbank_tgt1={bank_tgt1}\nbank_tgt2={bank_tgt2}\nbank_tgt3={bank_tgt3}\nolhc_duration={olhc_duration}\nnifty_sqoff_time={nifty_sqoff_time}\nnifty_tsl={nifty_tsl}\nbank_tsl={bank_tsl}\nenable_bank={enable_bank}\nenable_NFO={enable_NFO}\nenable_bank_data={enable_bank_data}\nenable_NFO_data={enable_NFO_data}\nfile_nifty={file_nifty}\nfile_bank={file_bank}\nno_of_trades_limit={no_of_trades_limit}\npending_ord_limit_mins={pending_ord_limit_mins}\nnifty_trade_start_time={nifty_trade_start_time}\nnifty_trade_end_time={nifty_trade_end_time}\nsl_wait_time={sl_wait_time}\nnifty_limit_price_low={nifty_limit_price_low}\nnifty_limit_price_high={nifty_limit_price_high}\nbank_limit_price_low={bank_limit_price_low}\nbank_limit_price_high={bank_limit_price_high}\nuse_rsi={use_rsi}\nrsi_period={rsi_period}\nrsi_buy_param={rsi_buy_param}\nrsi_sell_param={rsi_sell_param}"
iLog("Settings Used:\n"+all_variables,sendTeleMsg=True,publishToChannel=True)
# Lists for storing Nifty50 and BankNifty LTPs
lst_nifty_ltp = []
lst_bank_ltp = []


socket_opened = False

# Counters for dataframe indexes
df_nifty_cnt = 0           
df_bank_cnt = 0


df_cols = ["cur_HHMM","open","high","low","close","signal","sl"]  # v1.1 added signal column

df_nifty = pd.DataFrame(data=[],columns=df_cols)        # Low - to store 3 mins level OHLC data for nifty
df_bank = pd.DataFrame(data=[],columns=df_cols)         # Low - to store 3 mins level OHLC data for banknifty


dict_ltp = {}       #Will contain dictionary of token and ltp pulled from websocket
dict_sl_orders = {} #Dictionary to store SL Order ID: token,target price, instrument, quantity; if ltp > target price then update the SL order limit price.

 
cur_min = 0
flg_min = 0
MTM = 0.0                       # Float
pos_bank = 0                    # current banknifty position 
pos_nifty = 0                   # current nifty position


super_trend_nifty = []          # Supertrend list Nifty
super_trend_bank = []           # Supertrend list BankNifty
interval = olhc_duration        # Time interval of candles in minutes; 3 
processNiftyEOD = False         # Process pending Nifty order cancellation and saving of df data; Flag to run procedure only once
export_data = 0                 # Realtime export of bn and nifty dataframe; triggered through .ini; reset to 0 after export


token_nifty_ce = 1111           # Set by get instrument later in the code
token_nifty_pe = 2222
token_bank_ce = 1111           
token_bank_pe = 2222


ltp_nifty_ATM_CE = 0            # Last traded price for Nifty ATM CE
ltp_nifty_ATM_PE = 0            # Last traded price for Nifty ATM PE
ltp_bank_ATM_CE = 0             # Last traded price for BankNifty ATM CE
ltp_bank_ATM_PE = 0             # Last traded price for BankNifty ATM PE


############################################################################
#       Functions(Methods)
############################################################################
def get_realtime_config():
    '''This procedure can be called during execution to get realtime values from the .ini file'''

    global trade_nfo, trade_bank, enableBO2_bank, enableBO2_nifty, enableBO3_nifty,nifty_limit_price_offset,bank_limit_price_offset\
    ,mtm_sl,mtm_target, cfg, nifty_sl, bank_sl, export_data, nifty_ord_type, bank_ord_type\
    ,nifty_strike_ce_offset, nifty_strike_pe_offset, bank_strike_ce_offset, bank_strike_pe_offset

    cfg.read(INI_FILE)
    
    trade_nfo = int(cfg.get("realtime", "trade_nfo"))                   # True = 1 (or non zero) False=0
    trade_bank = int(cfg.get("realtime", "trade_bank"))                 # True = 1 (or non zero) False=0
    enableBO2_nifty = int(cfg.get("realtime", "enableBO2_nifty"))       # True = 1 (or non zero) False=0
    enableBO3_nifty = int(cfg.get("realtime", "enableBO3_nifty"))       # True = 1 (or non zero) False=0
    enableBO2_bank = int(cfg.get("realtime", "enableBO2_bank"))         # True = 1 (or non zero) False=0 
    nifty_sl = float(cfg.get("realtime", "nifty_sl"))                   #20.0
    bank_sl = float(cfg.get("realtime", "bank_sl"))                     #15.0
    export_data = float(cfg.get("realtime", "export_data"))
    mtm_sl = float(cfg.get("realtime", "mtm_sl"))
    mtm_target  = float(cfg.get("realtime", "mtm_target"))
    nifty_ord_type = cfg.get("realtime", "nifty_ord_type")      # BO / MIS
    bank_ord_type = cfg.get("realtime", "bank_ord_type")        # MIS / BO

    nifty_limit_price_offset = float(cfg.get("realtime", "nifty_limit_price_offset"))
    bank_limit_price_offset = float(cfg.get("realtime", "bank_limit_price_offset"))

    nifty_strike_ce_offset = float(cfg.get("realtime", "nifty_strike_ce_offset"))
    nifty_strike_pe_offset = float(cfg.get("realtime", "nifty_strike_pe_offset"))
    bank_strike_ce_offset = float(cfg.get("realtime", "bank_strike_ce_offset"))
    bank_strike_pe_offset = float(cfg.get("realtime", "bank_strike_pe_offset"))

    tick_processing_sleep_secs = int(cfg.get("realtime", "tick_processing_sleep_secs"))

def savedata(flgUpdateConfigFile=True):
    '''flgUpdateConfigFile = True Updates datafilename in the .ini file for nextday reload.
    
     In case of intermediary exports you may not want to update the datafile in the .ini file'''

    iLog("In savedata(). Exporting dataframes to .csv files.",6)    # Log as activity

    try:
        ts_ext = datetime.now().strftime("%Y%m%d_%H%M%S") + ".csv"
        if enable_NFO_data:
            file_nifty = "./data/NIFTY_" + ts_ext 
            # file_nifty_med = "./data/NIFTY_OPT_MED_" + ts_ext
            df_nifty.to_csv(file_nifty,index=False)
            # df_nifty_med.to_csv(file_nifty_med,index=False)

        if enable_bank_data:
            file_bank = "./data/BN_" + ts_ext
            # file_bn_med = "./data/BN_MED_" + ts_ext
            df_bank.to_csv(file_bank,index=False)
            # df_bank_med.to_csv(file_bn_med,index=False)

        # Save Nifty and BankNifty filenames for use in next day to load last 40 rows
        if flgUpdateConfigFile :
            if enable_NFO_data:
                cfg.set("info","file_nifty",file_nifty)
                # cfg.set("info","file_nifty_med",file_nifty_med)
            
            if enable_bank_data:
                cfg.set("info","file_bank",file_bank)
                # cfg.set("info","file_bn_med",file_bn_med)

            with open(INI_FILE, 'w') as configfile:
                cfg.write(configfile)
                configfile.close()

    except Exception as ex:
        iLog("In savedata(). Exception occured = " + str(ex),3)

def place_sl_order(main_order_id, nifty_bank, ins_opt):
    ''' 1. This procedure checks if the main_order_id is executed till the wait time is over
        2. If the main order is executed then places a StopLoss Order
        3. Checks if SL2 (enableBO2_*) is enabled, if yes places the second SL order
    nifty_bank = NIFTY | BANK '''

    iLog(f"In place_sl_order():main_order_id={main_order_id}, nifty_bank={nifty_bank}")

    lt_price = 0.0
    wait_time = sl_wait_time      # Currently set to 100 * 2 (sleep) = 200 seconds(~3 mins).  
    order_executed = False
    strMsg = ""
    
    while wait_time > 0:
        print(f"wait_time={wait_time}",flush=True)

        # Check if main order is completed
        try:
            main_ord = [ord for ord in alice.get_order_history('') if (ord['Nstordno']==main_order_id and ord['Status']=='complete') ] 
            print(f"main_ord={main_ord}",flush=True)
            if main_ord == []:
                pass
            else:
                # Order status is completed
                lt_price = float(main_ord[0]['Prc'])
                order_executed = True
                break
        
        except Exception as ex:
            iLog(f"place_sl_order(): Exception={ex}")
        
        # if order_executed : break   #break while loop
        sleep(2)
        wait_time = wait_time - 1



    if order_executed:
        sleep(2)  #As order might not be completely filled / alice blue takes time to recognise margin.
        
        if nifty_bank == "NIFTY": 
            # ins_opt =  ins_bank_opt
            bo1_qty = nifty_bo1_qty
            sl = nifty_sl
            tgt1 = nifty_tgt1
            tgt2 = nifty_tgt2
        
        elif nifty_bank == "BANK":
            # ins_opt =  ins_nifty_opt
            bo1_qty = bank_bo1_qty
            sl = bank_sl
            tgt1 = bank_tgt1
            tgt2 = bank_tgt2

        sl_price = float(lt_price-sl)
        
        #place SL order 1
        #---- Intraday order (MIS) , SL Order
        order = place_order_MIS(TransactionType.Sell, ins_opt, bo1_qty, OrderType.StopLossLimit, sl_price)
        
        # if order['status'] == 'success':
        if order['stat'] == 'Ok':
            strMsg = f"In place_sl_order(1): MIS SL1 order_id={order['NOrdNo']}, StopLoss Price={sl_price}"
            #update dict with SL order ID : [0-token, 1-target price, 2-instrument, 3-quantity, 4-SL Price]
            dict_sl_orders.update({order['NOrdNo']:[ins_opt[1], lt_price+tgt1, ins_opt, bo1_qty, sl_price] } )
            print("place_sl_order(1): dict_sl_orders=",dict_sl_orders, flush=True)
        else:
            strMsg = f"In place_sl_order(1): MIS SL1 Order Failed.={order}" 
        
        #Place SL order2, If second/medium range target (BO2) order is enabled then execute that
        
        if (nifty_bank == "NIFTY" and enableBO2_nifty ) or (nifty_bank == "BANK" and enableBO2_bank) :
            order = place_order_MIS(TransactionType.Sell, ins_opt, bo1_qty, OrderType.StopLossLimit, sl_price)
            # if order['status'] == 'success':
            if order['stat'] == 'Ok':
                strMsg = strMsg + f"In place_sl_order(2): MIS SL2 order_id={order}, StopLoss Price={sl_price}"
                #update dict with SL order ID : [0-token, 1-target price, 2-instrument, 3-quantity, 4-SL Price]
                dict_sl_orders.update({order['NOrdNo']:[ins_opt[1], lt_price+tgt2, ins_opt, bo1_qty, sl_price] } )
                print("place_sl_order(2): dict_sl_orders=",dict_sl_orders, flush=True)
            else:
                # {'stat': 'Not_Ok', 'Emsg': 'Not able to Retrieve  PlaceOrder '}
                strMsg = strMsg + f"In place_sl_order(2): MIS SL2 Order Failed.={order}"



    else:
        # cancel main order
        # {'stat': 'Ok', 'Result': ' NEST Order Number :221212000158180'}
        ret = alice.cancel_order(main_order_id)
        iLog(f"place_sl_order(): ret=alice.cancel_order()=>{ret}")
        strMsg = f"place_sl_order(): main order not executed within the wait time of {sl_wait_time} seconds, hence cancelled the order " + main_order_id

    iLog(strMsg,sendTeleMsg=True)

def place_order_MIS(buy_sell,ins_scrip,qty, order_type = OrderType.Market, limit_price=0.0):
    '''Places orders to the exchange based on the parameters  
    buy_sell = TransactionType.Buy/TransactionType.Sell
    order_type = OrderType.StopLossLimit Default is Market order
    limit_price = limit price in case SL order needs to be placed 
    '''
    global alice

    ord_obj = {}

    if limit_price > 1 : 
        trigger_price = limit_price
    else:
        trigger_price = None

    try:
        ord_obj=alice.place_order(transaction_type = buy_sell,
                         instrument = ins_scrip,
                         quantity = qty,
                         order_type = order_type,
                         product_type = ProductType.Intraday,
                         price = limit_price,
                         trigger_price = trigger_price,
                         stop_loss = None,
                         square_off = None,
                         trailing_sl = None,
                         is_amo = False,
                         order_tag = ORDER_TAG)

    except Exception as ex:
        iLog("Exception occured in place_order_MIS():"+str(ex),3)

    return ord_obj

def place_order_BO(ins_scrip,qty,limit_price,stop_loss_abs,target_abs,trailing_sl_abs):
    global alice
    
    try:
        ord_obj=alice.place_order(transaction_type = TransactionType.Buy,
                         instrument = ins_scrip,
                         quantity = qty,
                         order_type = OrderType.Limit,
                         product_type = ProductType.BracketOrder,
                         price = float(limit_price),
                         trigger_price = float(limit_price),
                         stop_loss = float(stop_loss_abs),
                         square_off = target_abs,
                         trailing_sl = trailing_sl_abs,
                         is_amo = False,
                         order_tag=ORDER_TAG)
    except Exception as ex:
            iLog("Exception occured in place_order_BO():"+str(ex),3)

    return ord_obj

def buy_nifty_options(strMsg):
   
    global df_nifty

    if df_nifty.empty:
        iLog(strMsg+" No candle data found",3)
        return

    df_nifty.iat[-1,5] = "B"  # v1.1 set signal column value


    # Cancel pending buy orders and close existing sell orders if any
    close_all_orders("NIFTY")


    # strMsg == NIFTY_CE | NIFTY_PE 
    lt_price, nifty_sl = get_trade_price_options(strMsg)   # Get trade price and SL for BO1 
   
    df_nifty.iat[-1,6] = nifty_sl  # v3.7 set sl column value. This is only for BO1; rest BOs will different SLs 

    # iLog(strMsg)    #can be commented later
   
    #Warning: No initialisation done
    if strMsg == "NIFTY_CE" :
        ins_nifty_opt = ins_nifty_ce
    elif strMsg == "NIFTY_PE" :
        ins_nifty_opt = ins_nifty_pe

    strMsg = strMsg + f" {ins_nifty_opt[3]}" + " Limit Price=" + str(lt_price) + " SL=" + str(nifty_sl)

    
    if lt_price<nifty_limit_price_low or lt_price>nifty_limit_price_high :
        strMsg = strMsg + " buy_nifty(): Limit Price not in buying range."
        iLog(strMsg,2,sendTeleMsg=True)
        return
    
    if not trade_nfo:
        strMsg = strMsg + " buy_nifty(): trade_nfo=0. Order not initiated."
        iLog(strMsg,2,sendTeleMsg=True)
        return

    if not check_trade_time_zone("NIFTY"):
        strMsg = strMsg + " buy_nifty(): No trade time zone. Order not initiated."
        iLog(strMsg,2,sendTeleMsg=True)
        return
        
    
    # Find CE or PE Position
    if pos_nifty > 0:   # Position updates in MTM check
        strMsg = f"buy_nifty(): Position already exists={pos_nifty}. " + strMsg    #do not buy if position already exists; 
        iLog(strMsg,sendTeleMsg=True)
    else:

        if trade_limit_reached("NIFTY"):
            strMsg = strMsg + "buy_nifty(): NIFTY Trade limit reached."
            iLog(strMsg,2,sendTeleMsg=True)
            return

        
        if nifty_ord_type == "MIS" : 
            #---- Intraday order (MIS) , Market Order
            # order = place_order_MIS(TransactionType.Buy, ins_nifty_opt,nifty_bo1_qty)
            # order_tag = datetime.datetime.now().strftime("NF_%H%M%S")
            
            bo1_qty = nifty_bo1_qty
            if enableBO2_nifty: 
                bo1_qty = nifty_bo1_qty*2
            
            # {'stat': 'Ok', 'NOrdNo': '221212000158180'}
            order = place_order_MIS(TransactionType.Buy, ins_nifty_opt, bo1_qty, OrderType.Limit, lt_price)
            if order['stat'] == 'Ok':
                strMsg = strMsg + " buy_nifty(): Initiating place_sl_order(). main_order_id==" +  order['NOrdNo'] 
                iLog(strMsg,sendTeleMsg=True)   # Can be commented later
                t = threading.Thread(target=place_sl_order,args=(order['NOrdNo'],"NIFTY",ins_nifty_opt,))
                t.start()

            else:
                strMsg = strMsg + f' buy_nifty(): MIS Order Failed. {order}'
                iLog(strMsg,sendTeleMsg=True)

        elif nifty_ord_type == "BO" :
            #---- First Bracket order for initial target
            order = place_order_BO(ins_nifty_opt,nifty_bo1_qty,lt_price,nifty_sl,nifty_tgt1,nifty_tsl)    #SL to be float; 
            if order['stat'] == 'Ok':
                # buy_order1_nifty = order['data']['oms_order_id']
                strMsg = strMsg + f" 1st BO order_id={order}"
            else:
                strMsg = strMsg + f' buy_nifty() 1st BO Failed. {order}'

            #---- Second Bracket order for open target
            if enableBO2_nifty:
                # lt_price, nifty_sl = get_trade_price("NIFTY","BUY",nifty_ord_exec_level2)   # Get trade price and SL for BO2
                order = place_order_BO(ins_nifty_opt,nifty_bo2_qty,lt_price,nifty_sl,nifty_tgt2,nifty_tsl)
                strMsg = strMsg + " BO2 Limit Price=" + str(lt_price) + " SL=" + str(nifty_sl)
                if order['stat'] == 'Ok':
                    # buy_order2_nifty = order['data']['oms_order_id']
                    strMsg = strMsg + f" 2nd BO order_id={order}"
                else:
                    strMsg=strMsg + f' buy_nifty() 2nd BO Failed. {order}'

            #---- Third Bracket order for open target
            if enableBO3_nifty:  
                # lt_price, nifty_sl = get_trade_price("NIFTY","BUY",nifty_ord_exec_level3)   # Get trade price and SL for BO3
                order = place_order_BO(ins_nifty_opt,nifty_bo3_qty,lt_price,nifty_sl,nifty_tgt3,nifty_tsl)
                strMsg = strMsg + " BO3 Limit Price=" + str(lt_price) + " SL=" + str(nifty_sl)
                if order['stat'] == 'Ok':
                    # buy_order3_nifty = order['data']['oms_order_id']
                    strMsg = strMsg + f" 3rd BO order_id={order}"
                else:
                    strMsg=strMsg + f' buy_nifty() 3rd BO Failed. {order}'

        iLog(strMsg,sendTeleMsg=True,publishToChannel=True)

def buy_bank_options(strMsg):
    '''Buy Banknifty options '''
    global df_bank

    df_bank.iat[-1,5] = "B"  # v1.1 set signal column value

    # Cancel pending buy orders and close existing sell orders if any
    close_all_orders("BANK")

    # strMsg == CE | PE 
    lt_price, bank_sl = get_trade_price_options(strMsg)   # Get trade price and SL for BO1 
   
    df_bank.iat[-1,6] = bank_sl  # v3.7 set sl column value. This is only for BO1; rest BOs will different SLs 


    #Warning: No initialisation done
    if strMsg == "BANK_CE" :
        ins_bank_opt = ins_bank_ce
    elif strMsg == "BANK_PE" :
        ins_bank_opt = ins_bank_pe
    

    strMsg = strMsg + f" {ins_bank_opt[3]}" + " Limit Price=" + str(lt_price) + " SL=" + str(bank_sl)

    
    if lt_price<bank_limit_price_low or lt_price>bank_limit_price_high :
        strMsg = strMsg + " buy_bank(): Limit Price not in buying range."
        iLog(strMsg,2,sendTeleMsg=True)
        return

    if not trade_bank :
        strMsg = strMsg + " buy_bank(): trade_bank=0. Order not initiated."
        iLog(strMsg,2,sendTeleMsg=True)
        return

    if not check_trade_time_zone("NIFTY"):
        strMsg = strMsg + " buy_bank(): No trade time zone. Order not initiated."
        iLog(strMsg,2,sendTeleMsg=True)
        return
    
    # Find CE or PE Position
    if pos_bank > 0:   # Position updates in MTM check
        strMsg = f"buy_bank(): Position already exists={pos_bank}. " + strMsg    #do not buy if position already exists; 
        iLog(strMsg,sendTeleMsg=True)
    else:

        if trade_limit_reached("BANKN"):
            strMsg = strMsg + "buy_bank(): BankNIFTY Trade limit reached."
            iLog(strMsg,2,sendTeleMsg=True)
            return

        
        if bank_ord_type == "MIS" : 
            #---- Intraday order (MIS) , Market Order
            # order = place_order_MIS(TransactionType.Buy, ins_bank_opt,bank_bo1_qty)
            # order_tag = datetime.datetime.now().strftime("BN_%H%M%S")
            # IF BO2 is enabled then trade quantity needs to    be doubled. Two SL/TGT Orders will be placed with the below quantity 
            bo1_qty = bank_bo1_qty
            if enableBO2_bank: 
                bo1_qty = bank_bo1_qty*2
            
            order = place_order_MIS(TransactionType.Buy, ins_bank_opt, bo1_qty, OrderType.Limit, lt_price)
            if order['stat'] == 'Ok':
                strMsg = strMsg + " buy_bank(): Initiating place_sl_order(). main_order_id=" + order['NOrdNo']
                iLog(strMsg,sendTeleMsg=True)   # Can be commented later
                t = threading.Thread(target=place_sl_order,args=( order['NOrdNo'] ,"BANK",ins_bank_opt,))
                t.start()

            else:
                strMsg = strMsg + f" buy_bank(): MIS Order Failed. {order}" 
                iLog(strMsg,sendTeleMsg=True)

        # BO option may not work as usually BO is disabled in alice blue for options, hence not updating the below code for BO
        elif bank_ord_type == "BO" :
            #---- First Bracket order for initial target
            order = place_order_BO(ins_bank_opt,bank_bo1_qty,lt_price,bank_sl,bank_tgt1,bank_tsl)    #SL to be float; 
            if order['stat'] == 'Ok':
                # buy_order1_bank = order['data']['oms_order_id']
                strMsg = strMsg + f" 1st BO order = {order}" 
            else:
                strMsg = strMsg + f" buy_bank() 1st BO Failed. {order}"

            #---- Second Bracket order for open target
            if enableBO2_bank:
                # lt_price, bank_sl = get_trade_price("NIFTY","BUY",bank_ord_exec_level2)   # Get trade price and SL for BO2
                order = place_order_BO(ins_bank_opt,bank_bo2_qty,lt_price,bank_sl,bank_tgt2,bank_tsl)
                strMsg = strMsg + " BO2 Limit Price=" + str(lt_price) + " SL=" + str(bank_sl)
                if order['stat'] == 'Ok':
                    # buy_order2_bank = order['data']['oms_order_id']
                    strMsg = strMsg + f" 2nd BO order = {order}"
                else:
                    strMsg=strMsg + f" buy_bank() 2nd BO Failed. {order}" 

            #---- Third Bracket order for open target
            if enableBO3_bank:  
                # lt_price, bank_sl = get_trade_price("NIFTY","BUY",bank_ord_exec_level3)   # Get trade price and SL for BO3
                order = place_order_BO(ins_bank_opt,bank_bo3_qty,lt_price,bank_sl,bank_tgt3,bank_tsl)
                strMsg = strMsg + " BO3 Limit Price=" + str(lt_price) + " SL=" + str(bank_sl)
                if order['stat'] == 'Ok':
                    # buy_order3_bank = order['data']['oms_order_id']
                    strMsg = strMsg + f" 3rd BO order = {order}"
                else:
                    strMsg=strMsg + f" buy_bank() 3rd BO Failed. {order}" 

        iLog(strMsg,sendTeleMsg=True,publishToChannel=True)

def subscribe_ins():
    # global alice,ins_nifty,ins_bank

    subscribe_list_nifty = [ins_nifty,ins_nifty_ce,ins_nifty_pe]
    subscribe_list_bank = [ins_bank,ins_bank_ce,ins_bank_pe]
    try:
        if enable_NFO_data : 
            # Check if one cal
            # alice.subscribe(ins_nifty, LiveFeedType.TICK_DATA)
            alice.subscribe(subscribe_list_nifty)
            iLog(f"subscribe_ins(): Subscribed to {subscribe_list_nifty}")

        if enable_bank_data : 
            # Check if one cal
            alice.subscribe(subscribe_list_bank)
            iLog(f"subscribe_ins(): Subscribed to {subscribe_list_bank}")
        # if enable_bn_data : alice.subscribe(ins_bn, LiveFeedType.COMPACT)
        pass     
    except Exception as ex:
        iLog("subscribe_ins(): Exception="+ str(ex),3)

    # print(datetime.datetime.now() ,"In subscribe_ins()",flush=True)
    iLog("subscribe_ins().")

def close_all_orders(opt_index="ALL",buy_sell="ALL",ord_open_time=0):
    '''Cancel pending orders. opt_index=ALL/BANKN/NIFTY , buy_sell = ALL/BUY/SELL'''
    # print(datetime.datetime.now(),"In close_all_orders().",opt_index,flush=True)

    #Square off MIS Positions if any
    if (opt_index=='NIFTY' or opt_index=='ALL') and nifty_ord_type == "MIS":
        if pos_nifty > 0 :
            iLog(f"Closing Nifty Open Positions pos_nifty={pos_nifty}",2,sendTeleMsg=True)   
            place_order_MIS(TransactionType.Sell, ins_nifty_opt,pos_nifty)
            # SL orders should be cancelled in the below try...catch block
        elif pos_nifty < 0 :
            iLog(f"Option position cannot be negative pos_nifty={pos_nifty}",2,sendTeleMsg=True)
            # place_order_MIS(TransactionType.Buy, ins_nifty_opt, abs(pos_nifty))

    if (opt_index=='BANK'  or opt_index=='ALL') and nifty_ord_type == "MIS":
        if pos_bank > 0 :
            iLog(f"Closing BankNifty Open Positions pos_bank={pos_bank}",2,sendTeleMsg=True)   
            place_order_MIS(TransactionType.Sell, ins_bank_opt ,pos_bank)
            #  SL orders should be cancelled in the below try...catch block
        elif pos_bank < 0 :
            iLog(f"Option position cannot be negative pos_bank={pos_bank}",2,sendTeleMsg=True)

    # Get pending orders and cancel them
    try:
        # lst_open_orders=[ord for ord in dict_ord if ord['Status']=='open']
        # orders = alice.get_order_history('')['data']['pending_orders'] 
        # Get all open orders
        lst_open_orders = []
        lst_orders = alice.get_order_history('')
        if lst_orders==list:
            lst_open_orders = [ord for ord in lst_orders if ord['Status']=='open']
            if not lst_open_orders:
                # print(datetime.datetime.now(),"In close_all_orders(). No Pending Orders found.",opt_index,flush=True)
                iLog(f"close_all_orders(): No Pending Orders found for {opt_index}")
                return    
        
    except Exception as ex:
        lst_open_orders = None
        # print("In close_all_orders(). Exception="+ str(ex),flush=True)
        iLog("close_all_orders(): Exception="+ str(ex),3)
        return

    if opt_index == "ALL":
        # If this proc is called in each interval, Check for order open time and leg indicator is blank for main order
        if ord_open_time > 0 :
            today = datetime.now()
            for c_order in lst_open_orders:
                diff =  today - datetime.strptime(c_order['OrderedTime'], '%d/%m/%Y %H:%M:%S')
                # print("diff.total_seconds()=",diff.total_seconds(), "c_order['leg_order_indicator']=",c_order['leg_order_indicator'], flush=True)
                # See if its not a BO/CO and having leg order
                if (c_order['SyomOrderId'] == '') and  (diff.total_seconds() / 60) > ord_open_time :
                    iLog("close_all_orders(): Cancelling order due to order open limit time crossed for Ord. no. : " + c_order['Nstordno'],sendTeleMsg=True)
                    alice.cancel_order(c_order['Nstordno'])

        else:
            #Cancel all open orders
            iLog("close_all_orders(): Cancelling all orders ") #+ c_order['oms_order_id'])
            # alice.cancel_order .cancel_all_orders()
            for c_order in lst_open_orders:
                iLog("close_all_orders(): Cancelling order "+c_order['Nstordno'])
                alice.cancel_order(c_order['Nstordno'])
    else:
        for c_order in lst_open_orders:
            #if c_order['leg_order_indicator']=='' then its actual pending order not leg order
            if opt_index == c_order['Trsym'][:5]:
                if buy_sell == "ALL" :
                    iLog("close_all_orders(): Cancelling order "+c_order['Nstordno'])
                    alice.cancel_order(c_order['Nstordno'])    

                elif buy_sell[0] == c_order['Trantype']:
                    iLog("close_all_orders(): Cancelling order "+c_order['Nstordno'])
                    alice.cancel_order(c_order['Nstordno'])

    iLog(f"close_all_orders(): opt_index={opt_index}, buy_sell={buy_sell}, ord_open_time={ord_open_time}") #6 = Activity/Task done

def check_MTM_Limit():
    ''' Checks and returns the current MTM and sets the trading flag based on the limit specified in the 
    .ini. This needs to be called before buy/sell signal generation in processing. 
    Also updates the postion counter for Nifty and bank which are used in buy/sell procs.'''
    
    global trade_bank, trade_nfo, pos_nifty, pos_bank

    trading_symbol = ""
    mtm = 0.0
    pos_bank = 0
    pos_nifty = 0

    ####### MTM needs manual calculation as ab provides wrong numbers
    # Get position and mtm
    try:    # Get netwise postions (MTM)
        # pos = alice.get_netwise_positions()
        pos = alice.get_netwise_positions() # Returns list of dicts if position is there else returns dict {'emsg': 'No Data', 'stat': 'Not_Ok'}
        if type(pos)==list:
            df_pos = pd.DataFrame(pos)
            # print("df_pos=",df_pos)
            if df_pos.empty:
                 iLog("check_MTM_Limit(): Unable to fetch position from alice.get_netwise_positions()")
            else:
                # MtoM = sum(pd.to_numeric(df_pos.MtoM.str.replace(",","")))
                pos_nifty = sum(pd.to_numeric(df_pos[df_pos.Symbol=='NIFTY'].Netqty))
                pos_bank = sum(pd.to_numeric(df_pos[df_pos.Symbol=='BANKNIFTY'].Netqty))

                df_pos["sell_amt"] = df_pos.netsellqty.str.replace(",","").astype(float) * df_pos.NetSellavgprc.str.replace(",","").astype(float)
                df_pos["buy_amt"]  = df_pos.netbuyqty.str.replace(",","").astype(float) * df_pos.NetBuyavgprc.str.replace(",","").astype(float)
                df_pos["open_amt"] = df_pos.Netqty.str.replace(",","").astype(float) * df_pos.LTP.str.replace(",","").astype(float)
                df_pos["mtm_amt"]  = df_pos["sell_amt"] - df_pos["buy_amt"] + df_pos["open_amt"]
                # Can sum the above statement directly into mtm
                mtm = sum(df_pos.mtm_amt)

                # iLog(f"MtoM={MtoM} mtm={mtm}")

        # if type(pos)==list:
            # print("pos:")
            # print(pos)

            # df_pos = pd.DataFrame(pos)
            # print("df_pos:")
            # print(df_pos)

            # mtm = sum(pd.to_numeric(df_pos.MtoM.str.replace(",","")))
            # pos_nifty = sum(pd.to_numeric(df_pos[df_pos.Symbol=='NIFTY'].Netqty))
            # pos_bank = sum(pd.to_numeric(df_pos[df_pos.Symbol=='BANKNIFTY'].Netqty))

            # print("mtm,pos_nifty,pos_bank: ",mtm,pos_nifty,pos_bank,flush=True)
            # if pos["emsg"]!='No Data':
            #     for p in  pos['data']['positions']:
            #         mtm = float(p['m2m'].replace(",","")) + mtm
            #         # print("get_position()",p['trading_symbol'],p['net_quantity'],flush=True)
            #         trading_symbol = p['trading_symbol'][:5]
            #         if trading_symbol == 'NIFTY':
            #             pos_nifty = pos_nifty + int(p['net_quantity'])

            #         elif trading_symbol == 'BANKN':
            #             pos_bank = pos_bank + int(p['net_quantity'])

            #         # below to be commented
            #         iLog(f"check_MTM_Limit():trading_symbol={trading_symbol}, pos_nifty={pos_nifty}, pos_bank={pos_bank}")

    
    except Exception as ex:
        mtm = -1.0  # To ignore in calculations in case of errors
        iLog(f"check_MTM_Limit(): Exception={ex}")
    
    # iLog(f"check_MTM_Limit(): mtm={mtm} mtm_sl={mtm_sl} mtm_target={mtm_target} trade_bank={trade_bank} trade_nfo={trade_nfo}")


    # Enable trade flags based on MTM limits set
    if (mtm < mtm_sl or mtm > mtm_target) and (trade_bank==1 or trade_nfo==1): # or mtm>mtm_target:
        trade_bank = 0
        trade_nfo = 0
        # Stop further trading and set both the trading flag to 0
        cfg.set("realtime","trade_nfo","0")
        cfg.set("realtime","trade_bank","0")

        try:
            with open(INI_FILE, 'w') as configfile:
                cfg.write(configfile)
                configfile.close()
            
            strMsg = "check_MTM_Limit(): Trade flags set to false. MTM={}, trade_nfo={}, trade_bank={}".format(mtm,trade_nfo,trade_bank)
            iLog(strMsg,6)  # 6 = Activity/Task done
            
        except Exception as ex:
            strMsg = "check_MTM_Limit(): Trade flags set to false. May be overwritten. Could not update ini file. Ex="+str(ex)
            iLog(strMsg,3)


        iLog(f"check_MTM_Limit(): MTM {mtm} {'less than SL' if mtm<mtm_sl else 'greater than Target' }. Squareoff will be triggered for MIS orders...",2,sendTeleMsg=True)

        close_all_orders("ALL")

    return mtm

def get_trade_price_options(bank_nifty):
    '''Returns the trade price and stop loss abs value for bank/nifty=CRUDE/NIFTY
    buy_sell=BUY/SELL, bo_level or Order execution level = 1(default means last close),2,3 and 0 for close -1 for market order
    '''

    iLog(f"In get_trade_price_options():{bank_nifty}")

    lt_price = 0.0

    # atr = 0
    sl = nifty_sl

    # Refresh the tokens and ltp
    if bank_nifty == "NIFTY_CE" or bank_nifty == "NIFTY_PE":
        get_option_tokens("NIFTY")
    elif bank_nifty == "BANK_CE" or bank_nifty == "BANK_PE":
        get_option_tokens("BANK")
        sl = bank_sl

    # 1. Set default limit price, below offset can be parameterised
    if bank_nifty == "NIFTY_CE" :
        lt_price = int(ltp_nifty_ATM_CE) + nifty_limit_price_offset # Set Default trade price
    elif bank_nifty == "NIFTY_PE" :
        lt_price = int(ltp_nifty_ATM_PE) + nifty_limit_price_offset # Set Default trade price
    elif bank_nifty == "BANK_CE" :
        lt_price = int(ltp_bank_ATM_CE) + bank_limit_price_offset
    elif bank_nifty == "BANK_PE" :
        lt_price = int(ltp_bank_ATM_PE) + bank_limit_price_offset
    else:
        iLog(f"get_trade_price_options(): {bank_nifty}")
    
    lt_price = float(lt_price)
    iLog(f"get_trade_price_options(): lt_price={lt_price} sl={sl}")
    
    return lt_price, sl

def trade_limit_reached(bank_nifty="NIFTY"):
    # Check if completed order can work here
    '''Check if number of trades reached/crossed the parameter limit . Return true if reached or crossed else false.
     Dont process the Buy/Sell order if returns true
     bank_nifty=CRUDE/NIFTY '''
    
    try:
        trade_book = alice.get_trade_book()
        if type(trade_book)==list and len(trade_book) >= no_of_trades_limit :
            print(f"len(trade_book)={len(trade_book)}")
            return True
        else:
            return False
           
    except Exception as ex:
        iLog("trade_limit_reached(): Exception="+ str(ex),3)
        return True     # To be safe in case of exception

def set_config_value(section,key,value):
    '''Set the config file (.ini) value. Applicable for setting only one parameter value. 
    All parameters are string

    section=info/realtime,key,value
    '''
    cfg.set(section,key,value)
    try:
        with open(INI_FILE, 'w') as configfile:
            cfg.write(configfile)
            configfile.close()
    except Exception as ex:
        iLog("Exception writing to config. section={},key={},value={},ex={}".format(section,key,value,ex),2)

def check_trade_time_zone(bank_nifty="NIFTY"):
    result = False

    cur_time = int(datetime.now().strftime("%H%M"))

    # if bank_nifty=="CRUDE" and (cur_time > curde_trade_start_time and cur_time < curde_trade_end_time) :
    #     result = True

    if bank_nifty=="NIFTY" and (cur_time > nifty_trade_start_time and cur_time < nifty_trade_end_time) :
        result = True

    return result

def get_option_tokens(nifty_bank="ALL"):
    '''This procedure sets the current option tokens to the latest ATM tokens
    nifty_bank="NIFTY" | "BANK" | "ALL"
    '''
    
    iLog(f"get_option_tokens():{nifty_bank}")

    #WIP
    global token_nifty_ce, token_nifty_pe, ins_nifty_ce, ins_nifty_pe, \
        token_bank_ce, token_bank_pe, ins_bank_ce, ins_bank_pe

    intCounter = 3

    if nifty_bank=="NIFTY" or nifty_bank=="ALL":
        while intCounter>0:
            if len(lst_nifty_ltp)>0:
            
                nifty50 = int(lst_nifty_ltp[-1])
                # print("nifty50=",nifty50,flush=True)

                nifty_atm = round(int(nifty50),-2)
                iLog(f"get_option_tokens(): nifty_atm={nifty_atm}")

                strike_ce = float(nifty_atm + nifty_strike_ce_offset)   #ITM Options
                strike_pe = float(nifty_atm + nifty_strike_pe_offset)


                tmp_ins_nifty_ce = alice.get_instrument_for_fno(exch="NFO",symbol = 'NIFTY', expiry_date=expiry_date.isoformat(), is_fut=False, strike=strike_ce, is_CE = True)
                tmp_ins_nifty_pe = alice.get_instrument_for_fno(exch="NFO",symbol = 'NIFTY', expiry_date=expiry_date.isoformat(), is_fut=False, strike=strike_pe, is_CE = False)
            

                if ins_nifty_ce != tmp_ins_nifty_ce:
                    ins_nifty_ce = tmp_ins_nifty_ce
                    token_nifty_ce = int(ins_nifty_ce[1])
                    alice.subscribe([ins_nifty_ce])

                if ins_nifty_pe != tmp_ins_nifty_pe:
                    ins_nifty_pe = tmp_ins_nifty_pe
                    token_nifty_pe = int(ins_nifty_pe[1])
                    alice.subscribe([ins_nifty_pe])
                
                iLog(f"get_option_tokens(): Selected ins_nifty_ce={ins_nifty_ce} ltp_nifty_ATM_CE={ltp_nifty_ATM_CE}")
                iLog(f"get_option_tokens(): Selected ins_nifty_pe={ins_nifty_pe} ltp_nifty_ATM_PE={ltp_nifty_ATM_PE}")
                

                if ltp_nifty_ATM_CE<1 or ltp_nifty_ATM_PE<1:
                    iLog(f"get_option_tokens(): Waiting 3 seconds for Nifty ltp ticks to be loaded...",2)
                    sleep(3)
                    intCounter = intCounter - 1
                    iLog(f"get_option_tokens(): ltp_nifty_ATM_CE={ltp_nifty_ATM_CE} ltp_nifty_ATM_PE={ltp_nifty_ATM_PE}")
                else:
                    break
                    
            else:
                intCounter = intCounter - 1
                if intCounter>0:
                    iLog(f"get_option_tokens(): Waiting 3 seconds for Nifty ltp ticks to be loaded...",2)
                    sleep(3)
                    iLog(f"get_option_tokens(): len(lst_nifty_ltp)={len(lst_nifty_ltp)}",2)
                
                

    intCounter = 3
    if nifty_bank=="BANK" or nifty_bank=="ALL":
        while intCounter>0:
            if len(lst_bank_ltp)>0:
                bank50 = int(lst_bank_ltp[-1])
                # print("Bank50=",bank50,flush=True)

                bank_atm = round(int(bank50),-2)
                iLog(f"get_option_tokens(): bank_atm={bank_atm}")

                strike_ce = float(bank_atm + bank_strike_ce_offset) #ITM Options
                strike_pe = float(bank_atm + bank_strike_pe_offset)

                # print(strike_ce,expiry_date.isoformat())

                tmp_ins_bank_ce = alice.get_instrument_for_fno(exch="NFO",symbol = 'BANKNIFTY', expiry_date=expiry_date.isoformat(), is_fut=False, strike=strike_ce, is_CE = True)
                tmp_ins_bank_pe = alice.get_instrument_for_fno(exch="NFO",symbol = 'BANKNIFTY', expiry_date=expiry_date.isoformat(), is_fut=False, strike=strike_pe, is_CE = False)

                
                if ins_bank_ce!=tmp_ins_bank_ce:
                    ins_bank_ce=tmp_ins_bank_ce
                    token_bank_ce = int(ins_bank_ce[1])
                    alice.subscribe([ins_bank_ce])
                
                if ins_bank_pe!=tmp_ins_bank_pe:
                    ins_bank_pe=tmp_ins_bank_pe
                    token_bank_pe = int(ins_bank_pe[1])
                    alice.subscribe([ins_bank_pe])


                iLog(f"get_option_tokens(): Selected ins_bank_ce={ins_bank_ce} ltp_bank_ATM_CE={ltp_bank_ATM_CE}")
                iLog(f"get_option_tokens(): Selected ins_bank_pe={ins_bank_pe} ltp_bank_ATM_PE{ltp_bank_ATM_PE}")


                if ltp_bank_ATM_CE <1 or ltp_bank_ATM_PE<1:
                    iLog(f"get_option_tokens(): Waiting 3 seconds for BankNifty ltp ticks to be loaded...",2)
                    sleep(3)
                    intCounter = intCounter - 1
                    iLog(f"get_option_tokens(): ltp_bank_ATM_CE={ltp_bank_ATM_CE} ltp_bank_ATM_PE={ltp_bank_ATM_PE}")
                else:
                    break
                



            else:
                intCounter = intCounter - 1
                if intCounter>0:
                    iLog(f"get_option_tokens(): Waiting 3 seconds for Banknifty ltp ticks to be loaded...",2)
                    sleep(3)
                    iLog(f"get_option_tokens(): len(lst_bank_ltp)={len(lst_bank_ltp)}",2)

                
    
    
    if nifty_bank=="NIFTY" or nifty_bank=="ALL":
        # alice.get_scrip_info(ins_nifty_ce)
        iLog(f"get_option_tokens(): ltp_nifty_ATM_CE={ltp_nifty_ATM_CE}")
        iLog(f"get_option_tokens(): ltp_nifty_ATM_PE={ltp_nifty_ATM_PE}")
    
    if nifty_bank=="BANK" or nifty_bank=="ALL":
        iLog(f"get_option_tokens(): ltp_bank_ATM_CE={ltp_bank_ATM_CE}")
        iLog(f"get_option_tokens(): ltp_bank_ATM_PE={ltp_bank_ATM_PE}")

def check_orders():
    ''' 1. Checks for pending SL orders and update/maintain local sl order dict 
        2. Updates SL order to target price if reached
        2.1 Update SL order target price and trigger price to TSL, ltp - tsl used to find new SL price and not ltp - (tsl+sl)
    '''
    # iLog("In check_orders()")   # can be disabled later to reduce logging  

    #1 Remove completed orders/keep only pending orders from the SL orders dict
    try:
        # orders = alice.get_order_history('')['data']['pending_orders']
        orders = alice.get_order_history('')
        # print(f"check_orders(): alice.get_order_history -> orders {orders} \ntype(orders) = {type(orders)}")
        if type(orders)==list:
            df_orders = pd.DataFrame(orders)

            df_orders = df_orders[df_orders.Status=='open'].ExchOrdID 
            
            if not df_orders.empty:
                for key, value in dict_sl_orders.items():
                    order_found = False
                    if key in df_orders.ExchOrdID.values:
                        order_found = True
                        break
                    
                    # remove the order from sl dict which is not pending
                    if not order_found:
                        dict_sl_orders.pop(key)
                        iLog(f"check_orders(): Removed order {key} from dict_sl_orders")
            else:
                dict_sl_orders.clear()
                # iLog(f"check_orders(): No open orders found. Cleared dict_sl_orders.")

        else:
            # iLog(f"check_orders(): No orders found. Clearing the internal order dict.")
            dict_sl_orders.clear()
        
    except Exception as ex:
        iLog(f"check_orders(): Exception Occured while processing alice.get_order_history. Exception = {ex}")
    
    
    # print("dict_ltp=",dict_ltp,flush=True)

    #2. Check the current price of the SL orders and if they are above tgt modify them to target price
    # dict_sl_orders => key=order ID : value = [0-token, 1-target price, 2-instrument, 3-quantity, 4-SL Price]
    tsl = bank_tsl  #+ bank_sl
    sl = nifty_sl
    # iLog(f"tsl={tsl}")
    
    for oms_order_id, value in dict_sl_orders.items():
        opt_name = value[2][3]
        ltp = dict_ltp[str(value[0])]
        if value[2][2][:5]=="BANKN":    #Check if the instrument is nifty or banknifty and get the tsl accordingly
            tsl = bank_tsl
            sl = bank_sl
        else:
            tsl = nifty_tsl
            sl = nifty_sl
        
        iLog(f"check_orders(): {opt_name} oms_order_id={oms_order_id}, ltp={ltp}, Target={float(value[1])}, tsl={tsl}, SL Price={float(value[4])}")
        #Set Target Price : current ltp > target price
        if ltp > value[1]+1 :
            try:
                alice.modify_order(TransactionType.Sell,value[2],ProductType.Intraday,oms_order_id,OrderType.Limit,value[3], price=float(value[1]))
                iLog(f"check_orders(): {opt_name} BullsEye! Target price for OrderID {oms_order_id} modified to {value[1]}")
            
            except Exception as ex:
                iLog(f"check_orders(): {opt_name} Exception occured during Target price modification = {ex}",3)

        
        #Set StopLoss(TargetPrice) to Trailing SL
        elif (ltp - value[4]) > tsl :
            tsl_price = float(int(ltp - tsl))
            try:
                alice.modify_order(TransactionType.Sell,value[2],ProductType.Intraday,oms_order_id,OrderType.StopLossLimit,value[3], tsl_price,tsl_price )
                #Update dictionary with the new SL price
                dict_sl_orders.update({oms_order_id:[value[0], value[1], value[2], value[3],tsl_price]} )
                iLog(f"check_orders(): {opt_name} TSL for OrderID {oms_order_id} modified to {tsl_price}")
                # \n dict_sl_orders={dict_sl_orders}
            except Exception as ex:
                iLog(f"check_orders(): {opt_name} Exception occured during TSL modification = {ex}",3)

        
        # Check if LTP has gone below SL Price. This condition should not occur until there is an API issue with order fetching
        elif (value[4] - ltp) > tsl :
            # Try to modify the order to be executed at market, if failed remove the order from the dict
            iLog(f"check_orders(): In SL Breached condition. Trying to modify order to market. {opt_name} OrderID {oms_order_id} SL {value[4]}")
            try:
                alice.modify_order(TransactionType.Sell,value[2],ProductType.Intraday,oms_order_id,OrderType.Market,value[3])
            except Exception as ex:
                iLog(f"check_orders(): In SL Breached condition. Removing OrderID {oms_order_id} from the dict_sl_orders.")
                dict_sl_orders.pop(oms_order_id)

def get_buy_sell(df_data):

    strMsgPrefix = "get_buy_sell():"
    # iLog(f"{strMsgPrefix} use_rsi={use_rsi} rsi_period={rsi_period}" )

    # Apply supertrend and RSI indicators to the data
    SuperTrend(df_data)                        # Supertrend calculations
    lst_super_trend = df_data.STX.values        # Get ST values into a list
    RSI(df_data,period=rsi_period)


    # strMsg=f"Nifty: #={df_nifty_cnt}, ST={super_trend_nifty[-1]}, ST_SL={round(df_nifty.ST.iloc[-1])}, ATR={round(df_nifty.ATR.iloc[-1],1)}, ltp_nifty_ATM_CE={ltp_nifty_ATM_CE}, ltp_nifty_ATM_PE={ltp_nifty_ATM_PE}"
    # iLog(strMsg)
    result = "NA"

    #--BUY---BUY---BUY---BUY---BUY---BUY---BUY---BUY---BUY---BUY
    if lst_super_trend[-1]=='up' and lst_super_trend[-2]=='down' and lst_super_trend[-3]=='down' and lst_super_trend[-4]=='down' and lst_super_trend[-5]=='down' and lst_super_trend[-6]=='down':
        if use_rsi:
            if df_data.RSI.iloc[-1] > rsi_buy_param and df_data.RSI.iloc[-1] < rsi_sell_param:
                c1 = round((df_data.RSI.iloc[-2] - df_data.RSI.iloc[-3]) / df_data.RSI.iloc[-3], 3 )
                c2 = round((df_data.RSI.iloc[-1] - df_data.RSI.iloc[-2]) / df_data.RSI.iloc[-2], 3 )

                iLog(f"{strMsgPrefix} ST=up - RSI Rate of change c2(latest)={c2},c1(previous)={c1}")
                if c2 > c1: #percent Rate of change is increasing
                    result = "B" 
                else:
                    strMsg = f"{strMsgPrefix} ST=up - RSI Rate of change not as per trend. CE Buy not initiated."
                    iLog(strMsg,sendTeleMsg=True)
        else:
            iLog(f"{strMsgPrefix} Use of RSI disabled.",sendTeleMsg=True)
            result = "B" 

    #---SELL---SELL---SELL---SELL---SELL---SELL---SELL---SELL---SELL        
    elif lst_super_trend[-1]=='down' and lst_super_trend[-2]=='up' and lst_super_trend[-3]=='up' and lst_super_trend[-4]=='up' and lst_super_trend[-5]=='up' and lst_super_trend[-6]=='up':
        if use_rsi:
            if df_data.RSI.iloc[-1] < rsi_sell_param and df_data.RSI.iloc[-1] > rsi_buy_param:
                c1 = round( ( df_data.RSI.iloc[-2] - df_data.RSI.iloc[-3] ) / df_data.RSI.iloc[-3] , 3 )
                c2 = round( ( df_data.RSI.iloc[-1] - df_data.RSI.iloc[-2] ) / df_data.RSI.iloc[-2] , 3 )
                
                iLog(f"{strMsgPrefix} ST=down - RSI Rate of change c2(latest)={c2},c1(previous)={c1}")
                
                if c2 < c1: # percent Rate of change is decreasing
                    result = "S"
                else:
                    strMsg = f"{strMsgPrefix} ST=down - RSI Rate of change not as per trend. PE Buy not inititated."
                    iLog(strMsg,sendTeleMsg=True)
        else:
            iLog(f"{strMsgPrefix} Use of RSI disabled.",sendTeleMsg=True)
            result = "S"

    return result





#################################
##     INDICATORS
#################################
# Source for tech indicator : https://github.com/arkochhar/Technical-Indicators/blob/master/indicator/indicators.py
def EMA(df, base, target, period, alpha=False):
    """
    Function to compute Exponential Moving Average (EMA)
    Args :
        df : Pandas DataFrame which contains ['date', 'open', 'high', 'low', 'close', 'volume'] columns
        base : String indicating the column name from which the EMA needs to be computed from
        target : String indicates the column name to which the computed data needs to be stored
        period : Integer indicates the period of computation in terms of number of candles
        alpha : Boolean if True indicates to use the formula for computing EMA using alpha (default is False)
    Returns :
        df : Pandas DataFrame with new column added with name 'target'
    """

    con = pd.concat([df[:period][base].rolling(window=period).mean(), df[period:][base]])

    if (alpha == True):
        # (1 - alpha) * previous_val + alpha * current_val where alpha = 1 / period
        df[target] = round(con.ewm(alpha=1 / period, adjust=False).mean(),1) #Rajesh - added round function
    else:
        # ((current_val - previous_val) * coeff) + previous_val where coeff = 2 / (period + 1)
        df[target] = round(con.ewm(span=period, adjust=False).mean(),1) #Rajesh - added round function

    df[target].fillna(0, inplace=True)
    return df

def ATR(df, period, ohlc=['open', 'high', 'low', 'close']):
    """
    Function to compute Average True Range (ATR)
    Args :
        df : Pandas DataFrame which contains ['date', 'open', 'high', 'low', 'close', 'volume'] columns
        period : Integer indicates the period of computation in terms of number of candles
        ohlc: List defining OHLC Column names (default ['Open', 'High', 'Low', 'Close'])
    Returns :
        df : Pandas DataFrame with new columns added for
            True Range (TR)
            ATR (ATR_$period)
    """
    #atr = 'ATR_' + str(period)
    atr = 'ATR'
    # Compute true range only if it is not computed and stored earlier in the df
    #if not 'TR' in df.columns:
    df['h-l'] = df[ohlc[1]] - df[ohlc[2]]
    df['h-yc'] = abs(df[ohlc[1]] - df[ohlc[3]].shift())
    df['l-yc'] = abs(df[ohlc[2]] - df[ohlc[3]].shift())

    #Rajesh - Updated round function below
    df['TR'] = round(df[['h-l', 'h-yc', 'l-yc']].max(axis=1),1)

    df.drop(['h-l', 'h-yc', 'l-yc'], inplace=True, axis=1)

    # Compute EMA of true range using ATR formula after ignoring first row
    EMA(df, 'TR', atr, period, alpha=True)

    return df

def SuperTrend(df, period = supertrend_period, multiplier=supertrend_multiplier, ohlc=['open', 'high', 'low', 'close']):
    """
    Function to compute SuperTrend
    Args :
        df : Pandas DataFrame which contains ['date', 'open', 'high', 'low', 'close', 'volume'] columns
        period : Integer indicates the period of computation in terms of number of candles
        multiplier : Integer indicates value to multiply the ATR
        ohlc: List defining OHLC Column names (default ['Open', 'High', 'Low', 'Close'])
    Returns :
        df : Pandas DataFrame with new columns added for
            True Range (TR), ATR (ATR_$period)
            SuperTrend (ST_$period_$multiplier)
            SuperTrend Direction (STX_$period_$multiplier)
    """

    ATR(df, period, ohlc=ohlc)
    atr = 'ATR' #+ str(period)
    st = 'ST' #+ str(period) + '_' + str(multiplier)
    stx = 'STX' #  + str(period) + '_' + str(multiplier)

    """
    SuperTrend Algorithm :
        BASIC UPPERBAND = (HIGH + LOW) / 2 + Multiplier * ATR
        BASIC LOWERBAND = (HIGH + LOW) / 2 - Multiplier * ATR
        FINAL UPPERBAND = IF( (Current BASICUPPERBAND < Previous FINAL UPPERBAND) or (Previous Close > Previous FINAL UPPERBAND))
                            THEN (Current BASIC UPPERBAND) ELSE Previous FINALUPPERBAND)
        FINAL LOWERBAND = IF( (Current BASIC LOWERBAND > Previous FINAL LOWERBAND) or (Previous Close < Previous FINAL LOWERBAND)) 
                            THEN (Current BASIC LOWERBAND) ELSE Previous FINAL LOWERBAND)
        SUPERTREND = IF((Previous SUPERTREND = Previous FINAL UPPERBAND) and (Current Close <= Current FINAL UPPERBAND)) THEN
                        Current FINAL UPPERBAND
                    ELSE
                        IF((Previous SUPERTREND = Previous FINAL UPPERBAND) and (Current Close > Current FINAL UPPERBAND)) THEN
                            Current FINAL LOWERBAND
                        ELSE
                            IF((Previous SUPERTREND = Previous FINAL LOWERBAND) and (Current Close >= Current FINAL LOWERBAND)) THEN
                                Current FINAL LOWERBAND
                            ELSE
                                IF((Previous SUPERTREND = Previous FINAL LOWERBAND) and (Current Close < Current FINAL LOWERBAND)) THEN
                                    Current FINAL UPPERBAND
    """

    # Compute basic upper and lower bands
    df['basic_ub'] = (df[ohlc[1]] + df[ohlc[2]]) / 2 + multiplier * df[atr]
    df['basic_lb'] = (df[ohlc[1]] + df[ohlc[2]]) / 2 - multiplier * df[atr]

    # Compute final upper and lower bands
    df['final_ub'] = 0.00
    df['final_lb'] = 0.00
    for i in range(period, len(df)):
        df['final_ub'].iat[i] = df['basic_ub'].iat[i] if df['basic_ub'].iat[i] < df['final_ub'].iat[i - 1] or \
                                                         df[ohlc[3]].iat[i - 1] > df['final_ub'].iat[i - 1] else \
        df['final_ub'].iat[i - 1]
        df['final_lb'].iat[i] = df['basic_lb'].iat[i] if df['basic_lb'].iat[i] > df['final_lb'].iat[i - 1] or \
                                                         df[ohlc[3]].iat[i - 1] < df['final_lb'].iat[i - 1] else \
        df['final_lb'].iat[i - 1]

    # Set the Supertrend value
    df[st] = 0.00
    for i in range(period, len(df)):
        df[st].iat[i] = df['final_ub'].iat[i] if df[st].iat[i - 1] == df['final_ub'].iat[i - 1] and df[ohlc[3]].iat[
            i] <= df['final_ub'].iat[i] else \
            df['final_lb'].iat[i] if df[st].iat[i - 1] == df['final_ub'].iat[i - 1] and df[ohlc[3]].iat[i] > \
                                     df['final_ub'].iat[i] else \
                df['final_lb'].iat[i] if df[st].iat[i - 1] == df['final_lb'].iat[i - 1] and df[ohlc[3]].iat[i] >= \
                                         df['final_lb'].iat[i] else \
                    df['final_ub'].iat[i] if df[st].iat[i - 1] == df['final_lb'].iat[i - 1] and df[ohlc[3]].iat[i] < \
                                             df['final_lb'].iat[i] else 0.00

        # Mark the trend direction up/down
    df[stx] = np.where((df[st] > 0.00), np.where((df[ohlc[3]] < df[st]), 'down', 'up'), np.NaN)

    # Remove basic and final bands from the columns
    df.drop(['basic_ub', 'basic_lb', 'final_ub', 'final_lb'], inplace=True, axis=1)

    df.fillna(0, inplace=True)
    return df

def RSI(df, base="close", period=7):
    """
    Function to compute Relative Strength Index (RSI)
    
    Args :
        df : Pandas DataFrame which contains ['date', 'open', 'high', 'low', 'close', 'volume'] columns
        base : String indicating the column name from which the MACD needs to be computed from (Default Close)
        period : Integer indicates the period of computation in terms of number of candles
        
    Returns :
        df : Pandas DataFrame with new columns added for 
            Relative Strength Index (RSI_$period)
    """
 
    delta = df[base].diff()
    up, down = delta.copy(), delta.copy()

    up[up < 0] = 0
    down[down > 0] = 0
    
    rUp = up.ewm(com=period - 1,  adjust=False).mean()
    rDown = down.ewm(com=period - 1, adjust=False).mean().abs()

    # df['RSI_' + str(period)] = round(100 - 100 / (1 + rUp / rDown))
    # df['RSI_' + str(period)].fillna(0, inplace=True)
    df['RSI'] = round(100 - 100 / (1 + rUp / rDown))
    df['RSI'].fillna(0, inplace=True)
    
    return df
 


########################################################################
#       Events
########################################################################
def event_handler_quote_update(message):
    global dict_ltp, lst_bank_ltp,ltp_bank_ATM_CE,ltp_bank_ATM_PE, lst_nifty_ltp, ltp_nifty_ATM_CE, ltp_nifty_ATM_PE

    feed_message = json.loads(message)

    if feed_message["t"]=='tf':
        if(feed_message["tk"]==str(token_nifty_ce)):
            ltp_nifty_ATM_CE = float(feed_message['lp'] if 'lp' in feed_message else ltp_nifty_ATM_CE)

        if(feed_message["tk"]==str(token_nifty_pe)):
            ltp_nifty_ATM_PE = float(feed_message['lp'] if 'lp' in feed_message else ltp_nifty_ATM_PE)

        if(feed_message["tk"]==str(token_bank_ce)):
            ltp_bank_ATM_CE = float(feed_message['lp'] if 'lp' in feed_message else ltp_bank_ATM_CE)

        if(feed_message["tk"]==str(token_bank_pe)):
            ltp_bank_ATM_PE = float(feed_message['lp'] if 'lp' in feed_message else ltp_bank_ATM_PE)

        #For Nifty 50, token number should ideally not change
        if(feed_message["tk"]=='26000'):
            if 'lp' in feed_message:
                lst_nifty_ltp.append(float(feed_message['lp']))

        #For BankNifty
        if(feed_message["tk"]=='26009'):
            if 'lp' in feed_message:
                lst_bank_ltp.append(float(feed_message['lp']))

        #Update the ltp for all the tokens
        if 'lp' in feed_message:
            dict_ltp.update({feed_message["tk"]:float(feed_message['lp'])})

def open_callback():
    global socket_opened
    socket_opened = True
    iLog("In open_callback().")
    # Call the instrument subscription, Hope this will resolve the tick discontinuation issue
    subscribe_ins()   # 2020-08-13 moving this to main call

def error_callback(error):
    iLog("In error_callback(). {}".format(error),3)
  
def close_callback():
    iLog("In close_callback().")




# ============================================
# Main program starts from here...
# ============================================
iLog("User = " + susername)

autologin_date = cfg.get("tokens", "autologin_date")
if autologin_date == date.today().isoformat():
    iLog("Ant portal autologin already run for the day.")
else:
    iLog("Running Ant portal autologin.")
    import ab_auto_login_totp

# pya3
alice = Aliceblue(user_id=susername,api_key=api_key)
session_id = alice.get_session_id() # Get Session ID


alice.get_contract_master("INDICES")
alice.get_contract_master("NSE")
alice.get_contract_master("NFO")


# Get Nifty and BankNifty spot instrument object
ins_nifty = alice.get_instrument_by_symbol('INDICES', 'NIFTY 50')
ins_bank = alice.get_instrument_by_symbol('INDICES', 'NIFTY BANK')


# Get expiry date
expiry_date = date.today() + timedelta( (3-date.today().weekday()) % 7 )
# Reduce one day if thursday is a holiday
if str(expiry_date) in weekly_expiry_holiday_dates :
    expiry_date = expiry_date - timedelta(days=1)

iLog(f"expiry_date={expiry_date}")


# Temp assignment for CE/PE instrument tokens
ins_nifty_ce = ins_nifty
ins_nifty_pe = ins_nifty
ins_nifty_opt = ins_nifty

ins_bank_ce = ins_bank
ins_bank_pe = ins_bank
ins_bank_opt = ins_bank



# Start Websocket
strMsg = "Starting Websocket."
iLog(strMsg,sendTeleMsg=True)

alice.start_websocket(socket_open_callback=open_callback, socket_close_callback=close_callback,
                      socket_error_callback=error_callback, subscription_callback=event_handler_quote_update, run_in_background=True)


# Check Websocket open status
while(socket_opened==False):
    sleep(5)
    iLog("Awaiting websocket connectivity")
    pass

iLog("websocket started...")

# Get Previous day saved data if available
try:
    if int(datetime.now().strftime("%H%M")) < 915:
        # 1. --- Read from previous day. In case of rerun or failures do not load previous day
        # Can clear the parameter file_nifty in the .ini if previous day data is not required
        if enable_NFO_data and file_nifty.strip()!="":
            iLog("Reading previous 40 period Nifty data from " + file_nifty)

            df_nifty = pd.read_csv(file_nifty).tail(40) 
            df_nifty.reset_index(drop=True, inplace=True)   # To reset index from 0 to 9 as tail gets the last 10 indexes
            df_nifty_cnt = len(df_nifty.index)

        if enable_bank_data and file_bank.strip()!="":
            iLog("Reading previous 40 period BankNifty data from " + file_bank)
            
            df_bank = pd.read_csv(file_bank).tail(40) 
            df_bank.reset_index(drop=True, inplace=True)   # To reset index from 0 to 9 as tail gets the last 10 indexes
            df_bank_cnt = len(df_bank.index)

except Exception as ex:
    iLog(f"Loading previous day data failed ! Exception occured = {ex}" ,3)


# Get the option tokens for Nifty and Bank based on the settings, when the market opens or is open
while True:
    cur_HHMM = int(datetime.now().strftime("%H%M"))
    if cur_HHMM > 914 and cur_HHMM<1532:
        get_option_tokens("ALL")
        break
    
    iLog(f"Non Market hours {cur_HHMM}(HHMM) , waiting for market hours... Press CTRL+C to abort.")
    sleep(5)


strMsg = "Starting tick processing."
iLog(strMsg,sendTeleMsg=True)




# Process tick data/indicators and generate buy/sell and execute orders
while True:
    # Process as per start of market timing
    cur_HHMM = int(datetime.now().strftime("%H%M"))

    cur_min = datetime.now().minute 

    # Below "If block" will run after every time as per the interval specified in the .ini file
    if( cur_min % interval == 0 and flg_min != cur_min):

        flg_min = cur_min       # Set the minute flag to run the code only once post the interval
        t1 = datetime.today()   # Set timer to record the processing time of all the indicators
        
        # Can include the below code to work in debug mode only
        strMsg = "BN_TIK_CNT=" + str(len(lst_bank_ltp))
        strMsg = strMsg +  " N_TIK_CNT="+ str(len(lst_nifty_ltp))

        
        if len(lst_bank_ltp) > 1:    #BANKNIFTY Candle
            tmp_lst = lst_bank_ltp.copy()  # Copy the ticks to a temp list
            lst_bank_ltp.clear()           # Reset the ticks list; There can be gap in the ticks during this step ???
            
            # Formation of BankNifty candle
            df_bank.loc[df_bank_cnt, df_cols]=[cur_HHMM, tmp_lst[0], max(tmp_lst), min(tmp_lst), tmp_lst[-1],"",0]
            df_bank_cnt = df_bank_cnt + 1 
            strMsg = strMsg + " BN=" + str(round(tmp_lst[-1]))      #Crude close 

                
        if len(lst_nifty_ltp) > 1: #and cur_HHMM > 914 and cur_HHMM < 1531:    #Nifty Candle
            tmp_lst = lst_nifty_ltp.copy()  # Copy the ticks to a temp list
            lst_nifty_ltp.clear()           # Reset the ticks list
            
            # Formation of Nifty candle
            df_nifty.loc[df_nifty_cnt,df_cols] = [cur_HHMM,tmp_lst[0],max(tmp_lst),min(tmp_lst),tmp_lst[-1],"",0]
            df_nifty_cnt = df_nifty_cnt + 1

            strMsg = strMsg + " N=" + str(round(tmp_lst[-1]))      #Nifty close


        # Get realtime config changes from .ini file and reload variables
        get_realtime_config()

        # Print Nifty and BankNift positions and MTM 
        strMsg = strMsg + f" POS(N,BN)=({pos_nifty}, {pos_bank}), MTM={MTM} {ins_nifty_ce.name}={ltp_nifty_ATM_CE} {ins_nifty_pe.name}={ltp_nifty_ATM_PE} {ins_bank_ce.name}={ltp_bank_ATM_CE} {ins_bank_pe.name}={ltp_bank_ATM_PE}" 

        iLog(strMsg,sendTeleMsg=True)

        # #######################################
        #           BANKNIFTY Order Generation
        # #######################################
        if df_bank_cnt > 6 and cur_HHMM > 914 and cur_HHMM < 1531:        # Calculate BankNifty indicators and call buy/sell
            # Calculate indicators and generate buy/sell signal
            iLog("Checking BANKNIFTY signal from get_buy_sell()")
            signal =  get_buy_sell(df_bank) 
            if signal=="B":
                buy_bank_options("BANK_CE")
            elif signal=="S":
                buy_bank_options("BANK_PE")

            
        # ////////////////////////////////////////
        #           NIFTY Order Generation
        # ////////////////////////////////////////
        if df_nifty_cnt > 6 and cur_HHMM > 914 and cur_HHMM < 1531:        # Calculate Nifty indicators and call buy/sell
            # Calculate indicators and generate buy/sell signal
            iLog("Checking NIFTY signal from get_buy_sell()")
            signal =  get_buy_sell(df_nifty)
            if signal=="B":
                buy_nifty_options("NIFTY_CE")
            elif signal=="S":
                buy_nifty_options("NIFTY_PE")



        #-- Find processing time and Log only if processing takes more than 2 seconds
        t2 = (datetime.today() - t1).total_seconds()
        if t2 > 2.0: 
            strMsg="Processing time(secs)= {0:.2f}".format(t2)
            iLog(strMsg,2)

        #-- Export data on demand
        if export_data:     
            savedata(False)     # Export dataframe data, both bank and nifty
            export_data = 0     # Reset config value to 0 in both file and variable
            set_config_value("realtime","export_data","0")


        #-- Cancel Nifty open orders, reset flags save data
        if cur_HHMM > nifty_sqoff_time and not processNiftyEOD: 
            close_all_orders()
            processNiftyEOD = True    # Set this flag so that we don not repeatedely process this

        

    if cur_HHMM > 1530 and cur_HHMM < 1532 :   # Exit the program post NSE closure
        # Reset trading flag for bank if bank is enabled on the instance
        if enable_bank : 
            iLog("Enabling BankNifty trading...")
            set_config_value("realtime","trade_bank","1")
        
        # Reset trading flag for nifty if nifty is enabled on the instance
        if enable_NFO : 
            iLog("Enabling NFO trading...")
            set_config_value("realtime","trade_nfo","1")
    
        savedata()      # Export dataframe data, both 
        iLog(f"Close of the day. Exiting Algo {ORDER_TAG}... @{cur_HHMM} MTM={MTM}",sendTeleMsg=True,publishToChannel=True)
        sys.exit()


        
        # #-- Cancel all open Crude orders after 11:10 PM, time can be parameterised
        # if cur_HHMM > bank_sqoff_time and not processCrudeEOD:
        #     close_all_orders('CRUDE')
        #     processCrudeEOD = True

        
        #-- Check if any open order greater than pending_ord_limit_mins and cancel the same 
        close_all_orders(ord_open_time=pending_ord_limit_mins)

    sleep(tick_processing_sleep_secs)        # May be reduced to accomodate the processing delay

    check_orders()  # Checks SL orders and sets target, should be called every 10 seconds. check logs
            
    # Check MTM and stop trading if limit reached; This can be parameterised to % gain/loss
    MTM = check_MTM_Limit()
