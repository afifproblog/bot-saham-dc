import os
import time
import logging
import requests
from datetime import datetime
from dotenv import load_dotenv
import pandas as pd
import ta
import yfinance as yf

# Bungkam log error bawaan yfinance agar terminal bersih
logging.getLogger("yfinance").setLevel(logging.CRITICAL)

# ==============================================================================
# 1. KONFIGURASI WEBHOOK DISCORD (OWNER BY ID DC: KRIMKEK)
# ==============================================================================
load_dotenv()
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

# ==============================================================================
# 2. DAFTAR MASTER SAHAM IDX AKTIF (SUDAH DIBERSIHKAN DARI DELISTED)
# ==============================================================================
def get_all_idx_tickers():
    daftar_kode = [
        "AALI", "ABDA", "ABMM", "ACES", "ACST", "ADCP", "ADES", "ADHI", "ADMF", "ADMR", "ADRO", "AGII", "AGRO", "AGRS",
        "AHAP", "AIMS", "AISA", "AKKU", "AKPI", "AKRA", "AKSI", "ALDO", "ALKA", "ALMI", "AMAR", "AMFG", "AMIN", "AMMN",
        "AMOR", "AMRT", "ANDI", "ANJT", "ANTM", "APEX", "APIC", "APII", "APLI", "APLN", "ARGO", "ARII", "ARNA", "ARTA",
        "ARTI", "ARTO", "ASBI", "ASDM", "ASGR", "ASHA", "ASII", "ASJT", "ASLC", "ASMI", "ASPI", "ASRI", "ASRM",
        "ASSA", "ATIC", "AUTO", "AVIA", "AWAN", "AYLS", "BABP", "BACA", "BAJA", "BALI", "BAPA", "BAPI", "BATA", "BAUT",
        "BAYU", "BBCA", "BBHI", "BBKP", "BBLD", "BBMD", "BBNI", "BBRI", "BBRM", "BBSS", "BBTN", "BBYB", "BCAP", "BCIC",
        "BCIP", "BDMN", "BEBS", "BEEF", "BEKS", "BELI", "BESS", "BEST", "BFIN", "BGTG", "BHAT", "BHIT", "BIKE", "BIMA",
        "BINA", "BIPI", "BIPP", "BIRD", "BISI", "BJBR", "BJTM", "BKDP", "BKSL", "BKSW", "BLTA", "BLTZ", "BLUE",
        "BMAS", "BMBL", "BMHS", "BMRI", "BMSR", "BMTR", "BNBA", "BNBR", "BNGA", "BNII", "BNLI", "BOBA", "BOGA", "BOLA",
        "BOLT", "BOSS", "BPFI", "BPII", "BPTR", "BRIS", "BRMS", "BRNA", "BRPT", "BSBK", "BSDE", "BSML", "BSSR", "BSWD",
        "BTEK", "BTON", "BTPN", "BTPS", "BUAH", "BUDI", "BUKA", "BULL", "BUMI", "BUVA", "BVIC", "BWPT", "BYAN",
        "CAKK", "CAMP", "CANI", "CARE", "CARS", "CASA", "CASH", "CASS", "CCSI", "CEKA", "CENT", "CFIN", "CGAS",
        "CINT", "CITA", "CITY", "CLAY", "CLEO", "CLPI", "CMNP", "CMNT", "CMPP", "CMRY", "CNKO", "CNMA", "COAL",
        "COCO", "CPIN", "CPRO", "CSAP", "CSIS", "CSMI", "CSRA", "CTBN", "CTRA", "CTTH", "CUAN", "CYBR", "DAAZ",
        "DART", "DATA", "DAYA", "DCII", "DEAL", "DEFI", "DEPO", "DEWA", "DGIK", "DGNS", "DIGI", "DILD", "DIVA",
        "DKFT", "DLTA", "DMAS", "DMMX", "DMND", "DNAR", "DNET", "DOID", "DOSS", "DPNS", "DPUM", "DRMA", "DSFI", "DSNG",
        "DSSA", "DUTI", "DVLA", "DWGL", "DYAN", "EAST", "ECII", "EDGE", "EKAD", "ELIT", "ELPI", "ELSA", "ELTY",
        "EMDE", "EMTK", "ENAK", "ENRG", "EPMT", "ERAA", "ERAL", "ERTX", "ESIP", "ESSA", "ESTA", "ESTI", "ETWA",
        "EURO", "EXCL", "FAPA", "FAST", "FASW", "FILM", "FIMP", "FIRE", "FISH", "FITT", "FLMC", "FMII", "FOOD", "FORU",
        "FPNI", "FWCT", "GDST", "GDYR", "GEMS", "GGRP", "GHON", "GIAA", "GJTL", "GLOB", "GLVA", "GMFI",
        "GMTD", "GOLD", "GOLF", "GOOD", "GOTO", "GPRA", "GPSO", "GRIA", "GRPH", "GRPM", "GSMF", "GTBO", "GTRA",
        "GTSI", "GULA", "GZCO", "HAIS", "HAJJ", "HALO", "HATM", "HDFA", "HDIT", "HEAL", "HELI", "HERO",
        "HEXA", "HITS", "HMSP", "HOKI", "HOMI", "HOPE", "HRME", "HRTA", "HRUM", "HYGN", "IATA",
        "IBFN", "IBOS", "IBST", "ICBP", "ICON", "IDEA", "IDPR", "IFII", "IFSH", "IGAR", "IKAI", "IKAN", "IKBI",
        "IKPM", "IMAS", "IMJS", "IMPC", "INAF", "INAI", "INCF", "INCO", "INDF", "INDO", "INDS", "INDX", "INDY",
        "INKP", "INPC", "INPP", "INPS", "INTD", "INTP", "IOTF", "IPAC", "IPCC", "IPCM", "IPPE", "IPTV", "IRRA",
        "ISAP", "ISAT", "ISSP", "ITIC", "ITMA", "ITMG", "JARR", "JAST", "JATI", "JAWA", "JAYA", "JECC", "JGLE", "JIHD",
        "JKON", "JMAS", "JPFA", "JRPT", "JSMR", "JSPT", "JTPE", "KAEF", "KARW", "KAYU", "KBAG", "KBLI", "KBLM", "KBLV",
        "KDSI", "KDTN", "KEEN", "KEJU", "KIAS", "KICI", "KIJA", "KINO", "KIOS", "KJEN", "KKGI", "KLAS", "KLBF", "KMDS",
        "KMTR", "KOCI", "KOIN", "KOKA", "KONI", "KOPI", "KOTA", "KPIG", "KRAS", "KREN", "KRYA", "KUAS",
        "LABA", "LAND", "LAPD", "LCKM", "LEAD", "LFLO", "LIFE", "LINK", "LION", "LIVE", "LMAX", "LMPI",
        "LMSH", "LOPI", "LPCK", "LPGI", "LPIN", "LPKR", "LPLI", "LPPF", "LPPS", "LRNA", "LSIP", "LTLS", "LUCK",
        "LUCY", "MAHA", "MAIN", "MAPA", "MAPB", "MAPI", "MARI", "MARK", "MAXI", "MAYA", "MBAP", "MBMA",
        "MBSS", "MBTO", "MCAS", "MCOL", "MCOR", "MDIA", "MDKA", "MDKI", "MDLN", "MDRN", "MEDC", "MEGA", "MENN",
        "MERI", "MERK", "MGLV", "MGNA", "MGRO", "MICE", "MIDI", "MIKA", "MINA", "MIRA", "MITI", "MKAP", "MKNT",
        "MKPI", "MKTR", "MLBI", "MLIA", "MLPL", "MLPT", "MMIX", "MMLP", "MNCN", "MOLI", "MORA", "MPIX", "MPMX",
        "MPOW", "MPPA", "MPRO", "MRAT", "MREI", "MSIE", "MSIN", "MSKY", "MTDL", "MTEL", "MTFN", "MTLA", "MTMH",
        "MTPS", "MTSM", "MTWI", "MUTU", "MYOH", "MYOR", "MYTX", "NAIK", "NANO", "NASA", "NASI", "NATO", "NAYZ",
        "NCKL", "NEST", "NETV", "NFCX", "NICE", "NICK", "NICL", "NIKL", "NINE", "NIRO", "NISP", "NOBU",
        "NPGF", "NRCA", "NSSS", "NTBK", "NZIA", "OASA", "OBMD", "OILS", "OKAS", "OLIV", "OMED", "OMRE", "OPMS",
        "PADA", "PADI", "PALM", "PAMG", "PANI", "PANR", "PANS", "PBID", "PBRX", "PBSA", "PCAR", "PDES", "PEGE",
        "PEHA", "PGAS", "PGEO", "PGLI", "PGUN", "PICO", "PJAA", "PKPK", "PLIN", "PMJS", "PMMP", "PNBN", "PNBS",
        "PNGO", "PNIN", "PNLF", "POLA", "POLI", "POLL", "POLU", "POLY", "PORT", "POWR", "PPGL", "PPRE", "PPRO",
        "PRDA", "PRIM", "PSAB", "PSDN", "PSGO", "PSKT", "PSSI", "PTBA", "PTDU", "PTIS", "PTMP", "PTPP", "PTPS",
        "PTRO", "PTSN", "PTSP", "PUDP", "PURA", "PURI", "PWON", "PYFA", "PZZA", "RAAM", "RAFI", "RAJA", "RALS",
        "RANC", "RBMS", "RCCC", "RDTX", "REAL", "RELF", "RELI", "RGAS", "RICY", "RIGS", "RISE", "RMKE", "RMKO",
        "RODA", "RONY", "ROTI", "RSCH", "RSGK", "RUIS", "RUNS", "SAFE", "SAME", "SAMF", "SAPX", "SATU", "SBAT",
        "SBMA", "SCCO", "SCMA", "SCNP", "SDMU", "SDPC", "SDRA", "SEMA", "SFAN", "SGER", "SGRO", "SHID", "SHIP",
        "SICO", "SILO", "SIMP", "SINI", "SIPD", "SKBM", "SKLT", "SKRN", "SLIS", "SMAR", "SMBR", "SMCB", "SMDM",
        "SMDR", "SMGA", "SMGR", "SMIL", "SMKL", "SMKM", "SMMA", "SMMT", "SMRA", "SMSM", "SNLK", "SOFA", "SOHO",
        "SONA", "SOSS", "SOTS", "SPMA", "SPRE", "SPTO", "SRTG", "SSIA", "SSMS", "SSTM", "STAR", "STAA", "STRK",
        "SULI", "SUPR", "SURE", "SWAT", "TALF", "TAMA", "TAMU", "TAPG", "TARA", "TAXI", "TAYS", "TBIG", "TBLA",
        "TBMS", "TCID", "TCPI", "TEBE", "TFAS", "TFCO", "TGKA", "TGRA", "TGUK", "TIFA", "TINS", "TIRA", "TIRT",
        "TKIM", "TLDN", "TLKM", "TMAS", "TMPO", "TNCA", "TOBA", "TOOL", "TOSK", "TOTO", "TOWR", "TOYS", "TPMA",
        "TPIA", "TRGU", "TRIM", "TRIN", "TRIS", "TRJA", "TRON", "TRST", "TRUE", "TRUK", "TRUS", "TSPC", "TUGU",
        "TYRE", "UANG", "UCID", "UDNG", "UFOE", "ULTJ", "UNIC", "UNIQ", "UNTR", "UNVR", "URBN", "UVCR", "VAST",
        "VERN", "VICI", "VICO", "VINS", "VIVA", "VKTR", "VOKS", "VRNA", "WAPO", "WEGE", "WEHA", "WGSH", "WICO",
        "WIDI", "WIFI", "WIIM", "WINS", "WIRG", "WMPP", "WOOD", "WOWS", "WSBP", "WTON", "YELO", "YPAS", "YULE",
        "ZATA", "ZBRA", "ZINC", "ZONE"
    ]
    tickers = [f"{kode}.JK" for kode in daftar_kode]
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Berhasil memuat {len(tickers)} emiten aktif BEI.")
    return tickers

# ==============================================================================
# 3. PENGIRIM NOTIFIKASI DISCORD (EMBED)
# ==============================================================================
def send_discord_alert(emiten, kategori, price, rsi, vol_ratio, turnover_rp, stoch_k, ma20):
    if not DISCORD_WEBHOOK_URL:
        print("[ERROR] DISCORD_WEBHOOK_URL tidak ditemukan di .env")
        return

    turnover_miliar = turnover_rp / 1_000_000_000
    embed_data = {
        "title": f"🚨 [SWING RADAR ALERT] - {emiten}",
        "description": "Pantulan teknikal terdeteksi: Akumulasi sehat (Volume aman 1.4x - 1.7x).",
        "color": 3066993,
        "fields": [
            {"name": "Kategori", "value": kategori, "inline": True},
            {"name": "Harga Terakhir", "value": f"Rp{int(price):,}", "inline": True},
            {"name": "RSI (14)", "value": f"{rsi:.2f} (Area Pantul)", "inline": True},
            {"name": "Lonjakan Volume", "value": f"{vol_ratio:.2f}x (Range 1.4x-1.7x)", "inline": True},
            {"name": "Nilai Transaksi", "value": f"Rp{turnover_miliar:.1f} Miliar", "inline": True},
            {"name": "Stochastic %K", "value": f"{stoch_k:.2f}", "inline": True},
            {"name": "Posisi MA 20", "value": f"Rp{int(ma20):,}", "inline": True},
            {"name": "Trading Plan", "value": "Validasi Orderbook & Broksum akumulasi. Target swing minimal 4 hari bursa.", "inline": False}
        ],
        "footer": {"text": f"IDX Swing Radar • {datetime.now().strftime('%d-%m-%Y %H:%M')}"}
    }
    try:
        requests.post(DISCORD_WEBHOOK_URL, json={"embeds": [embed_data]}, timeout=10)
    except Exception as e:
        print(f"Gagal kirim notif {emiten}: {e}")

def send_empty_radar_alert(total_screened):
    if not DISCORD_WEBHOOK_URL:
        print("[ERROR] DISCORD_WEBHOOK_URL tidak ditemukan di .env")
        return

    now_str = datetime.now().strftime("%d-%m-%Y %H:%M")
    embed_data = {
        "title": "📡 [SWING RADAR SCANNER] - STANDBY MODE",
        "description": f"Pemindaian teknikal terhadap **{total_screened} saham aktif BEI** selesai.",
        "color": 15844367,  # Emas / Amber
        "fields": [
            {
                "name": "📊 Hasil Screening Hari Ini",
                "value": "```diff\n- Tidak ditemukan saham potensial per hari ini.\n```",
                "inline": False
            },
            {
                "name": "🔍 Kriteria Screening",
                "value": "• Volume: **1.40x - 1.70x** rata-rata 20 hari\n• RSI (14): **30.0 - 45.0** (Pantulan Bawah)\n• Likuiditas: Turnover rata-rata **> Rp2 Miliar**\n• Harga: **> Rp100**",
                "inline": False
            },
            {
                "name": "💡 Rekomendasi",
                "value": "Kondisi market belum membentuk setup akumulasi ideal. Pertahankan alokasi cash & tunggu penutupan bursa berikutnya.",
                "inline": False
            }
        ],
        "footer": {"text": f"IDX Swing Radar • {now_str}"}
    }
    try:
        requests.post(DISCORD_WEBHOOK_URL, json={"embeds": [embed_data]}, timeout=10)
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Fallback embed (0 saham) berhasil dikirim ke Discord.")
    except Exception as e:
        print(f"Gagal kirim fallback notif: {e}")

# ==============================================================================
# 4. ENGINE FILTER & PEMINDAIAN
# ==============================================================================
def scan_market():
    tickers = get_all_idx_tickers()
    total = len(tickers)
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Memulai pemindaian teknikal {total} saham IDX...")
    hasil_lolos = 0

    for idx, ticker in enumerate(tickers, start=1):
        try:
            df = yf.download(ticker, period="60d", interval="1d", progress=False)
            if df.empty or len(df) < 25:
                continue

            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)

            df["RSI"] = ta.momentum.RSIIndicator(df["Close"], window=14).rsi()
            df["VOL_MA20"] = ta.trend.SMAIndicator(df["Volume"], window=20).sma_indicator()
            df["MA20"] = ta.trend.SMAIndicator(df["Close"], window=20).sma_indicator()
            
            stoch = ta.momentum.StochasticOscillator(df["High"], df["Low"], df["Close"], window=14, smooth_window=3)
            df["STOCH_K"] = stoch.stoch()

            last = df.iloc[-1]
            close_price = last["Close"]
            current_vol = last["Volume"]
            avg_vol20 = last["VOL_MA20"]
            current_rsi = last["RSI"]
            current_stoch_k = last["STOCH_K"]
            ma20 = last["MA20"]

            if pd.isna(avg_vol20) or avg_vol20 == 0:
                continue

            avg_turnover_rp = avg_vol20 * close_price

            # Filter likuiditas & harga non-gurem
            if close_price <= 100 or avg_turnover_rp < 2_000_000_000:
                continue

            if avg_turnover_rp >= 30_000_000_000:
                kategori = "🔵 Tier 1 / Bluechip"
            elif avg_turnover_rp >= 10_000_000_000:
                kategori = "🟢 Tier 2 / Second Liner"
            else:
                kategori = "🟡 Tier 3 / Third Liner Likuid"

            vol_ratio = current_vol / avg_vol20

            # Kriteria: Volume 1.4x - 1.7x & RSI 30 - 45
            is_volume_valid = 1.40 <= vol_ratio <= 1.70
            is_rsi_valid = 30.0 <= current_rsi <= 45.0

            if is_volume_valid and is_rsi_valid:
                clean_name = ticker.replace(".JK", "")
                print(f"[{idx}/{total}] -> LOLOS: {clean_name} | {kategori} | RSI: {current_rsi:.1f} | Vol: {vol_ratio:.2f}x")
                send_discord_alert(clean_name, kategori, close_price, current_rsi, vol_ratio, avg_turnover_rp, current_stoch_k, ma20)
                hasil_lolos += 1

            time.sleep(0.04)

        except Exception:
            continue

    print(f"[{datetime.now().strftime('%H:%M:%S')}] Pemindaian selesai! Ditemukan {hasil_lolos} saham potensial.")

    # FALLBACK: Kirim embed informatif jika tidak ada saham yang lolos kriteria
    if hasil_lolos == 0:
        send_empty_radar_alert(total)

if __name__ == "__main__":
    scan_market()
