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

# --- SENİN VERDİĞİN KODDAN ALINAN 4 ANA TARAMA ---
# 1. Trend ve Momentum (Ema'lar hizalı, CCI 100 üstü, RSI 55 üstü - Tarama 4'ün mantığı)
def Tarama_Trend():
    return (Query().set_markets('turkey')
                .select('name', 'change', 'close', 'relative_volume_10d_calc')
                .where(
                    Column('RSI')>55,
                    Column('EMA5') < Column('close'),
                    Column('EMA20') < Column('EMA5'),
                    Column('EMA50') < Column('EMA20'),
                    Column('CCI20') > 100,
                    Column('relative_volume_10d_calc')>1.3
                    )
        .get_scanner_data())[1]

# 2. Dip Avcıları (Bollinger alt bandından dönen, Stokastik RSI 20 altında al veren - Tarama 21'in mantığı)
def Tarama_Dip():
    return (Query().set_markets('turkey')
                .select('name', 'change', 'close', 'relative_volume_10d_calc')
                .where(
                    Column('close').crosses_above(Column('BB.lower')),
                    Column('Stoch.RSI.K').crosses_above(Column('Stoch.RSI.D')),
                    Column('Stoch.RSI.D') < 20
                    )
        .get_scanner_data())[1]

# 3. Hacimli Hareketler / Akıllı Para (Bollinger üstünde, hacmi 10M üzeri, göreceli hacim 1.7 - Tarama 5'in mantığı)
def Tarama_Hacim():
    return (Query().set_markets('turkey')
                .select('name', 'change', 'close', 'relative_volume_10d_calc')
                .where(
                    Column('volume') > 10E6,
                    Column('average_volume_10d_calc') > 10E6,
                    Column('relative_volume_10d_calc')>1.7,
                    Column('BB.upper') < Column('close'),
                    Column('MACD.macd') > Column('MACD.signal')
                    )
        .get_scanner_data())[1]

# 4. Kırılımlar (SMA20'yi yukarı kesen, RSI 50-55 arası, haftalık performansı kontrolü - Tarama 14'ün mantığı)
def Tarama_Kirilim():
    return (Query().set_markets('turkey')
                .select('name', 'change', 'close', 'relative_volume_10d_calc')
                .where(
                    Column('Perf.W') < 15,
                    Column('close') > Column('open'),
                    Column('close').crosses_above('SMA20'),
                    Column('RSI').between(50,55)
                    )
        .get_scanner_data())[1]


class BistScanner:
    def __init__(self):
        self.results = {
            "Trend ve Momentum": [],
            "Dip Avcilari (Oversold)": [],
            "Hacimli Hareketler (Akilli Para)": [],
            "Kirilimlar (Breakout)": []
        }

    # ESKİ YÖNTEM: 500 hisseyi tek tek çekip indikatör hesaplıyorduk (Yavaş ve hatalıydı)
    # YENİ YÖNTEM: Senin verdiğin Query mantığıyla TradingView'dan doğrudan filtrelenmiş veriyi alıyoruz
    def run_tv_screener(self):
        print("Tradingview Screener uzerinden 4 Kategori taraniyor...")
        
        try:
            df_trend = Tarama_Trend()
            for _, row in df_trend.iterrows():
                self.results["Trend ve Momentum"].append({
                    "Sembol": row['name'], "Fiyat": f"{row['close']:.2f}",
                    "Degisim": f"%{row['change']:.2f}", "Hacim": f"{row['relative_volume_10d_calc']:.1f}x"
                })
        except: pass

        try:
            df_dip = Tarama_Dip()
            for _, row in df_dip.iterrows():
                self.results["Dip Avcilari (Oversold)"].append({
                    "Sembol": row['name'], "Fiyat": f"{row['close']:.2f}",
                    "Degisim": f"%{row['change']:.2f}", "Hacim": f"{row['relative_volume_10d_calc']:.1f}x"
                })
        except: pass

        try:
            df_hacim = Tarama_Hacim()
            for _, row in df_hacim.iterrows():
                self.results["Hacimli Hareketler (Akilli Para)"].append({
                    "Sembol": row['name'], "Fiyat": f"{row['close']:.2f}",
                    "Degisim": f"%{row['change']:.2f}", "Hacim": f"{row['relative_volume_10d_calc']:.1f}x"
                })
        except: pass

        try:
            df_kirilim = Tarama_Kirilim()
            for _, row in df_kirilim.iterrows():
                self.results["Kirilimlar (Breakout)"].append({
                    "Sembol": row['name'], "Fiyat": f"{row['close']:.2f}",
                    "Degisim": f"%{row['change']:.2f}", "Hacim": f"{row['relative_volume_10d_calc']:.1f}x"
                })
        except: pass

    # Sadece taramaya giren hisselerin grafiğini çiziyoruz (Çok hızlı)
    def save_mini_chart(self, symbol):
        try:
            ticker = yf.Ticker(f"{symbol}.IS")
            df = ticker.history(period="60d", interval="1d")
            if df.empty: return None
            
            df.columns = [col.lower() for col in df.columns]
            plot_df = df.tail(30).copy()
            plot_df.index = pd.to_datetime(plot_df.index)
            
            file_path = f"chart_{symbol}.png"
            mpf.plot(plot_df, type='candle', style='charles', volume=False, 
                     savefig=file_path, figsize=(1.5, 1.2), dpi=50, warn_too_much_data=1000)
            return file_path
        except:
            return None

    # ESKİ GÜZEL PDF MİMARİMİZ (Kategoriler + Mini Grafikler)
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
                    chart_path = self.save_mini_chart(symbol)
                    
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
        await bot.send_document(chat_id=TELEGRAM_CHAT_ID, document=file, caption=f"🤖 BIST Gunluk Otomatik Tarama Raporu - {datetime.datetime.now().strftime('%d.%m.%Y')}")

def main():
    start_time = time.time()
    
    scanner = BistScanner()
    
    # Tarama yap (Tradingview üzerinden saniyeler sürer)
    scanner.run_tv_screener()

    # PDF oluştur (Sadece çıkan hisselerin grafikleri çekilir)
    print("PDF olusturuluyor...")
    scanner.generate_pdf()
    
    print("Telegram'a gonderiliyor...")
    asyncio.run(send_telegram())
    
    print(f"Islem tamamlandi! Toplam sure: {int(time.time() - start_time)} saniye.")

if __name__ == "__main__":
    main()
