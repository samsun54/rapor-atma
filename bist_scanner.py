import os
import time
import datetime
import pandas as pd
import yfinance as yf
from tradingview_screener import Query, Column
import matplotlib
matplotlib.use('Agg')
import mplfinance as mpf
import matplotlib.pyplot as plt
from fpdf import FPDF
import asyncio
from telegram import Bot

# --- AYARLAR ---
TELEGRAM_BOT_TOKEN = os.environ.get('TG_TOKEN', 'SIZIN_TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.environ.get('TG_CHAT_ID', 'SIZIN_KANAL_CHAT_ID') 

# --- SİZİN TARAFINIZDAN GELEN 50 TARAMA FONKSİYONU ---
def Tarama_1():
    Tarama = (Query().set_markets('turkey').select('name', 'change','close','volume','Perf.W').where(Column('RSI').between(50,65), Column('Perf.W').between(0,15), Column('close') > Column('open'), Column('close').crosses_above('SMA20'), Column('relative_volume_10d_calc')>1.0).get_scanner_data())[1]
    return Tarama

def Tarama_2():
    Tarama = (Query().set_markets('turkey').select('name', 'change','close','volume','Perf.W').where(Column('RSI').between(50,65), Column('Perf.W').between(0,15), Column('ADX').between(30,60), Column('Stoch.RSI.K') < 20.0, Column('Stoch.RSI.K').crosses_above(Column('Stoch.RSI.D')), Column('relative_volume_10d_calc')>1.0).get_scanner_data())[1]
    return Tarama

def Tarama_3():
    Tarama = (Query().set_markets('turkey').select('name', 'change','close','volume','Perf.W').where(Column('RSI')>50, Column('Perf.1M') > 20, Column('Mom')>1.0, Column('SMA5') < Column('close'), Column('SMA20') < Column('close'), Column('SMA200') < Column('close'), Column('relative_volume_10d_calc')>1.5, Column('market_cap_basic') >2E9).get_scanner_data())[1]
    return Tarama

def Tarama_4():
    Tarama = (Query().set_markets('turkey').select('name', 'change','close','volume','Perf.W').where(Column('RSI')>55, Column('EMA5') < Column('close'), Column('EMA20') < Column('EMA5'), Column('EMA50') < Column('EMA20'), Column('VWAP') <Column('close'), Column('CCI20') > 100, Column('relative_volume_10d_calc')>1.3, Column('Ichimoku.CLine') < (Column('Ichimoku.BLine'))).get_scanner_data())[1]
    return Tarama

def Tarama_5():
    Tarama = (Query().set_markets('turkey').select('name', 'change','close','volume','Perf.W').where(Column('volume') > 10E6, Column('average_volume_10d_calc') > 10E6, Column('relative_volume_10d_calc')>1.7, Column('BB.upper') < Column('close'), Column('P.SAR') < Column('close'), Column('Stoch.RSI.K')> (Column('Stoch.RSI.D')), Column('MACD.macd') > Column('MACD.signal')).get_scanner_data())[1]
    return Tarama

def Tarama_6():
    Tarama = (Query().set_markets('turkey').select('name', 'change','close','volume','Perf.W').where(Column('volume') > 5E6, Column('Perf.W') < 0, Column('EMA5').crosses_above(Column('SMA5')), Column('HullMA9') < Column('close'), Column('Stoch.RSI.K').crosses_above(Column('Stoch.RSI.D'))).get_scanner_data())[1]
    return Tarama

def Tarama_7():
    Tarama = (Query().set_markets('turkey').select('name', 'change','close','volume','Perf.W').where(Column('Mom').between(1,4), Column('P.SAR') < Column('close'), Column('MACD.macd') > Column('MACD.signal'), Column('Stoch.RSI.K') > Column('Stoch.RSI.D'), Column('Ichimoku.BLine') < Column('close'), Column('Ichimoku.CLine') > Column('Ichimoku.BLine'), Column('Ichimoku.Lead1') > Column('Ichimoku.Lead2'), Column('relative_volume_10d_calc') > 1.5).get_scanner_data())[1]
    return Tarama

def Tarama_8():
    Tarama = (Query().set_markets('turkey').select('name', 'change','close','volume','Perf.W').where(Column('W.R').between(-100,-70), Column('Perf.W').between(3,15), Column('relative_volume_10d_calc') > 1.5).get_scanner_data())[1]
    return Tarama

def Tarama_9():
    Tarama = (Query().set_markets('turkey').select('name', 'change','close','volume','Perf.W').where(Column('volume') > 1E6, Column('close') > Column('open'), Column('ChaikinMoneyFlow').between(-0.2,0.3), Column('HullMA9') < Column('close'), Column('relative_volume_10d_calc') > 1.5, Column('Perf.W') < 15, Column('RSI').between(45,60), Column('RSI7') < 70, Column('Stoch.RSI.K') >= Column('Stoch.RSI.D'), Column('Ichimoku.CLine') <Column('close')).get_scanner_data())[1]
    return Tarama

def Tarama_10():
    Tarama = (Query().set_markets('turkey').select('name', 'change','close','volume','Perf.W').where(Column('volume') > 5E6, Column('close') > Column('open'), Column('HullMA9') < Column('close'), Column('relative_volume_10d_calc') > 1.3, Column('RSI').between(40,65), Column('RSI7').between(40,65), Column('SMA5') > Column('SMA100'), Column('Stoch.RSI.K') >= Column('Stoch.RSI.D')).get_scanner_data())[1]
    return Tarama

def Tarama_11():
    Tarama = (Query().set_markets('turkey').select('name', 'change','close','volume','Perf.W').where(Column('Perf.W') < 15, Column('relative_volume_10d_calc') > 1.3, Column('Ichimoku.CLine').crosses_above(Column('Ichimoku.BLine'))).get_scanner_data())[1]
    return Tarama

def Tarama_12():
    Tarama = (Query().set_markets('turkey').select('name', 'change','close','volume','Perf.W').where(Column('RSI').between(30,40), Column('change') > 0, Column('MACD.macd').crosses_above(Column('MACD.signal')), Column('MACD.signal') < 0).get_scanner_data())[1]
    return Tarama

def Tarama_13():
    Tarama = (Query().set_markets('turkey').select('name', 'change','close','volume','Perf.W').where(Column('Perf.W') < 15, Column('close').crosses_above('EMA20'), Column('ADX').between(30,40)).get_scanner_data())[1]
    return Tarama

def Tarama_14():
    Tarama = (Query().set_markets('turkey').select('name', 'change','close','volume','Perf.W').where(Column('Perf.W') < 15, Column('close') > Column('open'), Column('close').crosses_above('SMA20'), Column('RSI').between(50,55)).get_scanner_data())[1]
    return Tarama

def Tarama_15():
    Tarama = (Query().set_markets('turkey').select('name', 'change','close','volume','Perf.W').where(Column('Perf.W') < 15, Column('relative_volume_10d_calc') > 1.3, Column('close').crosses_above('Ichimoku.CLine'), Column('Stoch.RSI.K').crosses_above(Column('Stoch.RSI.D'))).get_scanner_data())[1]
    return Tarama

def Tarama_16():
    Tarama = (Query().set_markets('turkey').select('name', 'change','close','volume','Perf.W').where(Column('Perf.W') < 15, Column('EMA5').crosses_above('EMA50')).get_scanner_data())[1]
    return Tarama

def Tarama_17():
    Tarama = (Query().set_markets('turkey').select('name', 'change','close','volume','Perf.W').where(Column('relative_volume_10d_calc') > 1.3, Column('Perf.W') < 15, Column('MACD.macd') < 0, Column('MACD.macd').crosses_above(Column('MACD.signal'))).get_scanner_data())[1]
    return Tarama

def Tarama_18():
    Tarama = (Query().set_markets('turkey').select('name', 'change','close','volume','Perf.W').where(Column('open') < Column('EMA200'), Column('close').crosses_above(Column('EMA200'))).get_scanner_data())[1]
    return Tarama

def Tarama_19():
    Tarama = (Query().set_markets('turkey').select('name', 'change','close','volume','Perf.W').where(Column('Perf.W') < 20, Column('close').crosses_above(Column('SMA200')), Column('VWAP') <Column('close'), Column('VWMA') <Column('close')).get_scanner_data())[1]
    return Tarama

def Tarama_20():
    Tarama = (Query().set_markets('turkey').select('name', 'change','close','volume','Perf.W').where(Column('close').crosses_above(Column('SMA50')), Column('Stoch.RSI.K').crosses_above(Column('Stoch.RSI.D')), Column('Stoch.RSI.D') <20).get_scanner_data())[1]
    return Tarama

def Tarama_21():
    Tarama = (Query().set_markets('turkey').select('name', 'change','close','volume','Perf.W').where(Column('close').crosses_above(Column('BB.lower')), Column('Stoch.RSI.K').crosses_above(Column('Stoch.RSI.D')), Column('Stoch.RSI.D') < 20).get_scanner_data())[1]
    return Tarama

def Tarama_22():
    Tarama = (Query().set_markets('turkey').select('name', 'change','close','volume','Perf.W').where(Column('P.SAR') < Column('close'), Column('EMA10').crosses_above(Column('EMA20'))).get_scanner_data())[1]
    return Tarama

def Tarama_23():
    Tarama = (Query().set_markets('turkey').select('name', 'change','close','volume','Perf.W').where(Column('close') > (Column('BB.lower')), Column('low') <= (Column('BB.lower')), Column('Stoch.RSI.K') >= Column('Stoch.RSI.D')).get_scanner_data())[1]
    return Tarama

def Tarama_24():
    Tarama = (Query().set_markets('turkey').select('name', 'change','close','volume','Perf.W').where(Column('ADX+DI').crosses_above(Column('ADX-DI')), Column('relative_volume_10d_calc') > 1.3, Column('MACD.macd') < Column('MACD.signal'), Column('ChaikinMoneyFlow') < 0, Column('Stoch.RSI.K') > Column('Stoch.RSI.D')).get_scanner_data())[1]
    return Tarama

def Tarama_25():
    Tarama = (Query().set_markets('turkey').select('name', 'change','close','volume','Perf.W').where(Column('Perf.W') < 15, Column('relative_volume_10d_calc') > 1.5, Column('EMA5') < Column('close'), Column('EMA20') < Column('EMA5'), Column('EMA50') < Column('EMA20'), Column('MACD.macd') > Column('MACD.signal'), Column('P.SAR').crosses_below(Column('close')), Column('CCI20') >= 90.0).get_scanner_data())[1]
    return Tarama

def Tarama_26():
    Tarama = (Query().set_markets('turkey').select('name', 'change','close','volume','Perf.W').where(Column('Perf.W') < 15, Column('RSI').between(30,55), Column('MACD.macd').crosses_above(Column('MACD.signal')), Column('MACD.signal') < 0.0).get_scanner_data())[1]
    return Tarama

def Tarama_27():
    Tarama = (Query().set_markets('turkey').select('name', 'change','close','volume','Perf.W').where(Column('Perf.W') < 15, Column('ATR') < 0.2, Column('MACD.macd').crosses_above(Column('MACD.signal'))).get_scanner_data())[1]
    return Tarama

def Tarama_28():
    Tarama = (Query().set_markets('turkey').select('name', 'change','close','volume','Perf.W').where(Column('close').crosses_above(Column('SMA50')), Column('Stoch.RSI.K').crosses_above(Column('Stoch.RSI.D')), Column('Stoch.RSI.D') < 40.0).get_scanner_data())[1]
    return Tarama

def Tarama_29():
    Tarama = (Query().set_markets('turkey').select('name', 'change','close','volume','Perf.W').where(Column('Perf.W') < 15.0, Column('HullMA9').crosses_above(Column('SMA20')), Column('Stoch.RSI.K') > Column('Stoch.RSI.D'), Column('Stoch.RSI.D') < 50.0).get_scanner_data())[1]
    return Tarama

def Tarama_30():
    Tarama = (Query().set_markets('turkey').select('name', 'change','close','volume','Perf.W').where(Column('Perf.W') < 15.0, Column('relative_volume_10d_calc')>1.0, Column('close') > Column('open'), Column('RSI').between(45,60), Column('RSI7') < 70, Column('ChaikinMoneyFlow').between(-0.2,0.3), Column('HullMA9') < Column('close'), Column('Stoch.RSI.K') >= Column('Stoch.RSI.D'), Column('Ichimoku.CLine').crosses_below(Column('close'))).get_scanner_data())[1]
    return Tarama

def Tarama_31():
    Tarama = (Query().set_markets('turkey').select('name', 'change','close','volume','Perf.W').where(Column('Perf.W') < 15.0, Column('relative_volume_10d_calc')>1.0, Column('close') >= Column('SMA5'), Column('SMA10') >Column('SMA20'), Column('MACD.macd').crosses_above(Column('MACD.signal'))).get_scanner_data())[1]
    return Tarama

def Tarama_32():
    Tarama = (Query().set_markets('turkey').select('name', 'change','close','volume','Perf.W').where(Column('Perf.W') < 15.0, Column('relative_volume_10d_calc')>1.0, Column('close') > Column('EMA5'), Column('close') > Column('EMA10'), Column('close') > Column('EMA20'), Column('close') > Column('EMA30'), Column('close') > Column('EMA50'), Column('close') > Column('EMA100'), Column('close') > Column('EMA200'), Column('market_cap_basic') <1E7).get_scanner_data())[1]
    return Tarama

def Tarama_33():
    Tarama = (Query().set_markets('turkey').select('name', 'change','close','volume','Perf.W').where(Column('Perf.W') < 15.0, Column('relative_volume_10d_calc')>1.0, Column('MACD.macd').crosses_above(Column('MACD.signal')), Column('Stoch.RSI.K').crosses_above(Column('Stoch.RSI.D'))).get_scanner_data())[1]
    return Tarama

def Tarama_34():
    Tarama = (Query().set_markets('turkey').select('name', 'change','close','volume','Perf.W').where(Column('Perf.W') < 15.0, Column('relative_volume_10d_calc')>1.0, Column('volume') > 5E6, Column('close') > Column('open'), Column('RSI').between(40,65), Column('RSI7').between(40,65), Column('SMA5') > Column('SMA100'), Column('HullMA9') > Column('low'), Column('Stoch.RSI.K') > (Column('Stoch.RSI.D'))).get_scanner_data())[1]
    return Tarama

def Tarama_35():
    Tarama = (Query().set_markets('turkey').select('name', 'change','close','volume','Perf.W').where(Column('close').crosses_above('HullMA9'), Column('ATR').between(0,10), Column('SMA20').crosses_below('close')).get_scanner_data())[1]
    return Tarama

def Tarama_36():
    Tarama = (Query().set_markets('turkey').select('name', 'change','close','volume','Perf.W').where(Column('RSI').between(50,65), Column('Perf.W')< 50, Column('ADX') > 20, Column('CCI20').crosses_above(-100), Column('relative_volume_10d_calc')>1.0).get_scanner_data())[1]
    return Tarama

def Tarama_37():
    Tarama = (Query().set_markets('turkey').select('name', 'change','close','volume','Perf.W').where(Column('RSI') > 55.0, Column('EMA5') < Column('close'), Column('EMA20') < Column('SMA5'), Column('EMA50') < Column('SMA20'), Column('CCI20').crosses_above(100), Column('Value.Traded') > 1E7).get_scanner_data())[1]
    return Tarama

def Tarama_38():
    Tarama = (Query().set_markets('turkey').select('name', 'change','close','volume','Perf.W').where(Column('RSI')>55.0, Column('ATR')>1.0, Column('ADX') >= 19.0, Column('Mom') >= 0.0, Column('EMA5') < Column('close'), Column('EMA10') < Column('close'), Column('EMA20') < Column('close'), Column('EMA50') < Column('close'), Column('EMA100') < Column('close'), Column('EMA200') < Column('close'), Column('Stoch.K')>=50.0, Column('MoneyFlow') >= 40.0, Column('ChaikinMoneyFlow')>=-0.7, Column('Ichimoku.BLine').crosses_below(Column('close'))).get_scanner_data())[1]
    return Tarama

def Tarama_39():
    Tarama = (Query().set_markets('turkey').select('name', 'change','close','volume','Perf.W').where(Column('RSI5')>Column('RSI9'), Column('HullMA9') < Column('close'), Column('MoneyFlow') >= 50.0, Column('EMA5').crosses_above(Column('SMA10')), Column('MACD.macd') > Column('MACD.signal'), Column('Ichimoku.CLine') < Column('close'), Column('Ichimoku.BLine|1W') < Column('close'), Column('relative_volume_10d_calc')>1.0).get_scanner_data())[1]
    return Tarama

def Tarama_40():
    Tarama = (Query().set_markets('turkey').select('name', 'change','close','volume','Perf.W').where(Column('RSI')>55, Column('CCI20').crosses_above(100), Column('EMA5') < Column('close'), Column('EMA20') < Column('EMA5'), Column('EMA50') < Column('EMA20'), Column('VWAP') <Column('close'), Column('Perf.W').between(0,15), Column('relative_volume_10d_calc|1W')>1.0, Column('Ichimoku.CLine') < (Column('close'))).get_scanner_data())[1]
    return Tarama

def Tarama_41():
    Tarama = (Query().set_markets('turkey').select('name', 'change','close','volume','Perf.W',).where(Column('Perf.W') < 10, Column('change') < 9.5, Column('close').crosses_above(Column('EMA20')), Column('EMA20') >= Column('EMA50'), Column('relative_volume_10d_calc|1W')>1.7).get_scanner_data())[1]
    return Tarama

def Tarama_42():
    Tarama = (Query().set_markets('turkey').select('name', 'change','close','volume','Perf.W',).where(Column('Perf.W') < 10, Column('change') < 9.5, Column('ADX') > 20, Column('CCI20').crosses_above(100), Column('relative_volume_10d_calc')>1.5).get_scanner_data())[1]
    return Tarama

def Tarama_43():
    Tarama = (Query().set_markets('turkey').select('name', 'change','close','volume','Perf.W',).where(Column('Perf.W') < 10, Column('change') < 9.5, Column('RSI7').crosses_above(Column('RSI')), Column('Stoch.RSI.K').crosses_above(Column('Stoch.RSI.D')), Column('relative_volume_10d_calc')>1.5).get_scanner_data())[1]
    return Tarama

def Tarama_44():
    Tarama = (Query().set_markets('turkey').select('name', 'change','close','volume','Perf.W').where(Column('Perf.W') < 10.0, Column('change') < 9.5, Column('relative_volume_10d_calc')>1.3, Column('MACD.macd').crosses_above(Column('MACD.signal')), Column('Stoch.RSI.K').crosses_above(Column('Stoch.RSI.D'))).get_scanner_data())[1]
    return Tarama

def Tarama_45():
    Tarama = (Query().set_markets('turkey').select('name', 'change','close','volume','Perf.W').where(Column('Perf.W') < 10.0, Column('change') < 9.5, Column('relative_volume_10d_calc')>1.5, Column('MACD.macd').crosses_above(0), Column('MACD.macd') > (Column('MACD.signal'))).get_scanner_data())[1]
    return Tarama

def Tarama_46():
    Tarama = (Query().set_markets('turkey').select('name', 'change','close','volume','Perf.W').where(Column('Perf.W') < 10.0, Column('change') < 9.5, Column('relative_volume_10d_calc')>1.0, Column('P.SAR') < Column('close'), Column('EMA10').crosses_above(Column('EMA20'))).get_scanner_data())[1]
    return Tarama

def Tarama_47():
    Tarama = (Query().set_markets('turkey').select('name', 'change','close','volume','Perf.W').where(Column('Perf.W').between(0,10), Column('change').between(0,5), Column('relative_volume_10d_calc')>1.0, Column('W.R').between(-100,-50)).get_scanner_data())[1]
    return Tarama

def Tarama_48():
    Tarama = (Query().set_markets('turkey').select('name', 'change','close','volume','Perf.W').where(Column('Perf.W') < 10, Column('change') <9.5, Column('relative_volume_10d_calc')>1.0, Column('EMA5') < Column('close'), Column('EMA20') < Column('EMA5'), Column('MACD.macd') > Column('MACD.signal'), Column('P.SAR').crosses_below(Column('close')), Column('CCI20') >= 90).get_scanner_data())[1]
    return Tarama

def Tarama_49():
    Tarama = (Query().set_markets('turkey').select('name', 'change','close','volume','Perf.W').where(Column('Perf.W') < 10.0, Column('relative_volume_10d_calc') > 1.3, Column('ADX') > 20, Column('ADX+DI') > Column('ADX-DI'), Column('Aroon.Up') > 99, Column('Aroon.Up') > Column('Aroon.Down'), Column('HullMA9') < Column('close'), Column('Ichimoku.BLine') < Column('Ichimoku.CLine')).get_scanner_data())[1]
    return Tarama

def Tarama_50():
    Tarama = (Query().set_markets('turkey').select('name', 'change','close','volume','Perf.W').where(Column('Perf.W') < 15.0, Column('relative_volume_10d_calc') > 1.0, Column('ADX').between(20,60), Column('RSI').between(50,65), Column('Stoch.RSI.K').crosses_above(Column('Stoch.RSI.D'))).get_scanner_data())[1]
    return Tarama


# --- PDF VE GRAFİK FONKSİYONLARI ---
def save_mini_chart(symbol, df):
    if df is None or len(df) < 30: return None
    plot_df = df.tail(30).copy()
    plot_df.index = pd.to_datetime(plot_df.index)
    file_path = f"chart_{symbol}.png"
    try:
        mpf.plot(plot_df, type='candle', style='charles', volume=False, 
                 savefig=file_path, figsize=(1.5, 1.2), dpi=50, warn_too_much_data=1000)
        return file_path
    except:
        return None

def generate_pdf(final_df):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, f"BIST 50 Kriter Gece Tarayici Raporu", ln=True, align='C')
    pdf.cell(0, 8, f"Tarih: {datetime.datetime.now().strftime('%d.%m.%Y')}", ln=True, align='C')
    pdf.ln(3)

    if final_df.empty:
        pdf.set_font("Arial", "", 12)
        pdf.cell(0, 10, "Bugun 50 kriterin hicbirine uyan hisse bulunamadi.", ln=True, align='C')
    else:
        # Tablo Başlıkları
        pdf.set_font("Arial", "B", 8)
        pdf.set_fill_color(200, 220, 255)
        pdf.cell(15, 6, "", border=1) # Grafik yeri
        pdf.cell(18, 6, "Hisse", border=1, fill=True, align='C')
        pdf.cell(18, 6, "Fiyat", border=1, fill=True, align='C')
        pdf.cell(18, 6, "Gunluk %", border=1, fill=True, align='C')
        pdf.cell(18, 6, "Haftalik %", border=1, fill=True, align='C')
        pdf.cell(12, 6, "Sayi", border=1, fill=True, align='C')
        pdf.cell(91, 6, "Girdigi Taramalar", border=1, fill=True, align='C')
        pdf.ln()

        # Tablo Satırları
        pdf.set_font("Arial", "", 7)
        for index, row in final_df.iterrows():
            symbol = row['name']
            close = row['close']
            change = row['change']
            perf_w = row['Perf.W']
            sayi = row['Tarama Sayısı']
            taramalar = row['Taramalar']
            
            # Sadece listeye giren hisselerin grafiklerini çek (Çok hızlı olur)
            try:
                ticker = yf.Ticker(f"{symbol}.IS")
                df = ticker.history(period="60d", interval="1d")
                chart_path = save_mini_chart(symbol, df)
            except:
                chart_path = None

            if chart_path and os.path.exists(chart_path):
                pdf.image(chart_path, x=10, w=15) 
            else:
                pdf.set_x(10)
                pdf.cell(15, 6, "", border=1)
            
            pdf.set_x(25)
            pdf.cell(18, 6, str(symbol), border=1)
            pdf.cell(18, 6, str(close), border=1)
            
            # Renklendirme: Pozitif yeşil, Negatif kırmızı (Basit font renklendirmesi)
            pdf.cell(18, 6, f"%{change}", border=1)
            pdf.cell(18, 6, f"%{perf_w}", border=1)
            pdf.cell(12, 6, str(sayi), border=1, align='C')
            
            # Tarama isimleri çok uzun olabileceği için küçük fontla multicolor yapalım
            x_pos = pdf.get_x()
            y_pos = pdf.get_y()
            pdf.multi_cell(91, 3, str(taramalar), border=1)
            
            # multi_cell satır sonuna geldikten sonra bir sonraki satırın başlangıç Y'sini güncelle
            if pdf.get_y() > y_pos + 6: 
                pass # Doğal akışa bırak
            
            if chart_path and os.path.exists(chart_path): 
                os.remove(chart_path)

    pdf.output("BIST_Raporu.pdf")

async def send_telegram():
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    with open("BIST_Raporu.pdf", "rb") as file:
        await bot.send_document(chat_id=TELEGRAM_CHAT_ID, document=file, caption=f"🤖 BIST 50 Kriter Otomatik Tarama Raporu - {datetime.datetime.now().strftime('%d.%m.%Y')}")

# --- ANA ÇALIŞTIRICI FONKSİYON ---
def main():
    start_time = time.time()
    print("Tradingview Screener ile 50 Tarama Baslatiliyor...")
    
    tarama_functions = [
        Tarama_1, Tarama_2, Tarama_3, Tarama_4, Tarama_5, Tarama_6, Tarama_7, Tarama_8,
        Tarama_9, Tarama_10, Tarama_11, Tarama_12, Tarama_13, Tarama_14, Tarama_15,
        Tarama_16, Tarama_17, Tarama_18, Tarama_19, Tarama_20, Tarama_21, Tarama_22,
        Tarama_23, Tarama_24, Tarama_25, Tarama_26, Tarama_27, Tarama_28, Tarama_29,
        Tarama_30, Tarama_31, Tarama_32, Tarama_33, Tarama_34, Tarama_35, Tarama_36,
        Tarama_37, Tarama_38, Tarama_39, Tarama_40, Tarama_41, Tarama_42, Tarama_43,
        Tarama_44, Tarama_45, Tarama_46, Tarama_47, Tarama_48, Tarama_49, Tarama_50,
    ]
    
    tarama_list = []
    for i, func in enumerate(tarama_functions):
        try:
            print(f"[{i+1}/50] Tarama isleniyor...")
            df = func()
            if not df.empty:
                df['Taramalar'] = f"T{i+1}"
                tarama_list.append(df)
            time.sleep(0.5) # Tradingview ban yemekten korunmak için
        except Exception as e:
            print(f"Tarama {i+1} hata verdi: {e}")

    if not tarama_list:
        print("Hicbir taramada hisse bulunamadi.")
        combined_df_2 = pd.DataFrame()
    else:
        print("Taramalar birlestiriliyor ve siralaniyor...")
        combined_df = pd.concat(tarama_list, ignore_index=True)
        
        # Sizin yazdiginiz mukemmel birlestirme algoritmasi
        combined_df = combined_df.groupby(['ticker', 'name', 'change', 'close', 'volume', 'Perf.W'], as_index=False).agg({'Taramalar': ','.join})
        combined_df['close'] = round(combined_df['close'] ,2)
        combined_df['Perf.W'] = round(combined_df['Perf.W'] ,2)
        combined_df['Tarama Sayısı'] = combined_df['Taramalar'].str.count('T')
        combined_df['Taramalar'] = combined_df['Taramalar'].str.replace('Tarama', 'T')
        combined_df['change'] = round(combined_df['change'] ,2)
        combined_df_2 = combined_df.sort_values(by='Tarama Sayısı', ascending=False).reset_index(drop=True)

    print("PDF olusturuluyor...")
    generate_pdf(combined_df_2)
    
    print("Telegram'a gonderiliyor...")
    asyncio.run(send_telegram())
    
    print(f"Islem tamamlandi! Toplam sure: {int(time.time() - start_time)} saniye.")

if __name__ == "__main__":
    main()
