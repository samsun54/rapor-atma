import os
import time
import datetime
import pandas as pd
import yfinance as yf
from tradingview_screener import Query  # <-- DOĞRU İSİM BURASI
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

# --- TRADINGVIEW SCREENER İLE TÜM HİSSELERİ ÇEKME ---
def tum_bist_hisselerini_cek():
    print("Tradingview Screener üzerinden BIST hisseleri çekiliyor...")
    try:
        screener = Query()
        # 'turkey' ekranındaki tüm hisseleri çeker
        df = screener.get_screeners_table(screener_name='turkey', columns=['name', 'close'])
        
        # Fiyatı 0'dan büyük olanları filtrele (İşlem görmeyenleri ekleme)
        df = df.dropna(subset=['close'])
        df = df[df['close'] > 0]
        
        hisseler = df['name'].tolist()
        print(f"Toplam {len(hisseler)} geçerli hisse bulundu.")
        return hisseler
    except Exception as e:
        print(f"Screener Hatası: {e}")
        return []

class BistScanner:
    def __init__(self, hisse_listesi):
        self.hisse_listesi = hisse_listesi
        self.results = {
            "Trend ve Momentum": [],
            "Dip Avcilari (Oversold)": [],
            "Hacimli Hareketler (Akilli Para)": [],
            "Kirilimlar (Breakout)": []
        }

    def get_data(self, symbol):
        try:
            ticker = yf.Ticker(f"{symbol}.IS")
            df = ticker.history(period="250d", interval="1d")
            
            if df.empty:
                return None
                
            df.columns = [col.lower() for col in df.columns]
            return df
        except Exception as e:
            return None

    def calculate_indicators(self, df):
        if df is None or df.empty: return None
        
        df['SMA_20'] = df['close'].rolling(window=20).mean()
        df['SMA_50'] = df['close'].rolling(window=50).mean()
        
        delta = df['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))
        
        df['BB_Mid'] = df['close'].rolling(window=20).mean()
        bb_std = df['close'].rolling(window=20).std()
        df['BB_Upper'] = df['BB_Mid'] + (bb_std * 2)
        df['BB_Lower'] = df['BB_Mid'] - (bb_std * 2)
        
        df['Vol_MA_20'] = df['volume'].rolling(window=20).mean()
        
        return df

    def scan_stock(self, symbol):
        df = self.get_data(symbol)
        df = self.calculate_indicators(df)
        if df is None or len(df) < 50: return

        last = df.iloc[-1] 
        prev = df.iloc[-2]
        
        if pd.isna(last['SMA_20']) or pd.isna(last['RSI']): return

        price = last['close']
        change = ((price - prev['close']) / prev['close']) * 100
        volume_ratio = last['volume'] / last['Vol_MA_20'] if last['Vol_MA_20'] > 0 else 0

        info = {
            "Sembol": symbol,
            "Fiyat": f"{price:.2f}",
            "Degisim": f"%{change:.2f}",
            "Hacim": f"{volume_ratio:.1f}x"
        }

        if last['close'] > last['SMA_20'] > last['SMA_50'] and 50 < last['RSI'] < 70:
            self.results["Trend ve Momentum"].append(info)

        if last['RSI'] < 30 or last['low'] <= last['BB_Lower']:
            self.results["Dip Avcilari (Oversold)"].append(info)

        if volume_ratio > 2.5 and change > 0:
            self.results["Hacimli Hareketler (Akilli Para)"].append(info)

        if last['close'] > last['BB_Upper'] and prev['close'] <= prev['BB_Upper']:
            self.results["Kirilimlar (Breakout)"].append(info)

    def save_mini_chart(self, symbol, df):
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

    def generate_pdf(self):
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, f"BIST Gece Tarayici Raporu - {datetime.datetime.now().strftime('%d.%m.%Y')}", ln=True, align='C')
        pdf.ln(5)

        toplam_hisse = sum(len(v) for v in self.results.values())
        
        if toplam_hisse == 0:
            pdf.set_font("Arial", "", 12)
            pdf.cell(0, 10, "Bugun tarama kriterlerine uyan hicbir hisse bulunamadi.", ln=True, align='C')
        else:
            for category, stocks in self.results.items():
                if not stocks: continue
                
                pdf.set_font("Arial", "B", 12)
                pdf.set_fill_color(200, 220, 255)
                pdf.cell(0, 8, f"{category} ({len(stocks)} Hisse)", ln=True, fill=True)
                
                for stock in stocks:
                    symbol = stock["Sembol"]
                    df = self.calculate_indicators(self.get_data(symbol))
                    chart_path = self.save_mini_chart(symbol, df)
                    
                    pdf.set_font("Arial", "", 9)
                    if chart_path and os.path.exists(chart_path):
                        pdf.image(chart_path, x=10, w=15) 
                        pdf.set_x(28)
                    else:
                        pdf.set_x(10)
                    
                    pdf.cell(25, 6, stock["Sembol"], border=1)
                    pdf.cell(25, 6, stock["Fiyat"], border=1)
                    pdf.cell(25, 6, stock["Degisim"], border=1)
                    pdf.cell(25, 6, stock["Hacim"], border=1)
                    pdf.ln()
                    
                    if chart_path and os.path.exists(chart_path): 
                        os.remove(chart_path)

        pdf.output("BIST_Raporu.pdf")

async def send_telegram():
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    with open("BIST_Raporu.pdf", "rb") as file:
        await bot.send_document(chat_id=TELEGRAM_CHAT_ID, document=file, caption=f"BIST Gunluk Otomatik Tarama Raporu - {datetime.datetime.now().strftime('%d.%m.%Y')}")

def main():
    start_time = time.time()
    
    BIST_HISSELERI = tum_bist_hisselerini_cek()
    if not BIST_HISSELERI:
        print("Hisse listesi bos! Islem iptal edildi.")
        return

    scanner = BistScanner(BIST_HISSELERI)
    
    for i, hisse in enumerate(BIST_HISSELERI):
        print(f"Taranıyor: [{i+1}/{len(BIST_HISSELERI)}] {hisse}")
        scanner.scan_stock(hisse)
        time.sleep(0.5) 

    print("PDF olusturuluyor...")
    scanner.generate_pdf()
    
    print("Telegram'a gonderiliyor...")
    asyncio.run(send_telegram())
    
    print(f"Islem tamamlandi! Toplam sure: {int(time.time() - start_time)} saniye.")

if __name__ == "__main__":
    main()
