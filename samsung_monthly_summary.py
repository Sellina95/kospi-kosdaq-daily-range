import yfinance as yf

# 삼성전자 티커 (Yahoo Finance 기준: 005930.KS)
ticker = "005930.KS"

# 최근 1개월 데이터 불러오기 (일 단위)
df = yf.download(ticker, period="1mo", interval="1d")

# 요약 계산
avg_close = df["Close"].mean()
high_price = df["High"].max()
low_price = df["Low"].min()

print("📊 삼성전자 최근 1개월 요약")
print(f" - 평균 종가: {avg_close:.2f} KRW")
print(f" - 최고가: {high_price:.2f} KRW")
print(f" - 최저가: {low_price:.2f} KRW")
