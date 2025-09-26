import pandas as pd

def latest_high_low_from_naver_day(code: str):
    url = f"https://finance.naver.com/item/sise_day.naver?code={code}"

    # ✅ EUC-KR 인코딩 지정
    tables = pd.read_html(url, header=0, encoding="euc-kr")
    df = tables[0].dropna(how="all").dropna(subset=["날짜", "고가", "저가"]).reset_index(drop=True)

    # 숫자 데이터 정리
    for col in ["시가", "고가", "저가", "종가", "전일비", "거래량"]:
        if col in df.columns:
            df[col] = (df[col].astype(str).str.replace(",", "", regex=False).str.strip()
                       .replace("", pd.NA))
            df[col] = pd.to_numeric(df[col], errors="coerce")

    latest = df.iloc[0]
    return {
        "date": latest["날짜"],
        "open": float(latest.get("시가", float("nan"))),
        "high": float(latest.get("고가", float("nan"))),
        "low":  float(latest.get("저가", float("nan"))),
        "close": float(latest.get("종가", float("nan")))
    }

KOSPI_PROXY = "069500"   # KODEX 200
KOSDAQ_PROXY = "229200"  # KODEX 코스닥150

kospi_today = latest_high_low_from_naver_day(KOSPI_PROXY)
kosdaq_today = latest_high_low_from_naver_day(KOSDAQ_PROXY)

print("📊 오늘(최근 영업일) KOSPI(프록시: KODEX200 069500)")
print(f" - 날짜: {kospi_today['date']}")
print(f" - 시가/고가/저가/종가: {kospi_today['open']:.2f} / {kospi_today['high']:.2f} / {kospi_today['low']:.2f} / {kospi_today['close']:.2f}")

print("\n📊 오늘(최근 영업일) KOSDAQ(프록시: KODEX 코스닥150 229200)")
print(f" - 날짜: {kosdaq_today['date']}")
print(f" - 시가/고가/저가/종가: {kosdaq_today['open']:.2f} / {kosdaq_today['high']:.2f} / {kosdaq_today['low']:.2f} / {kosdaq_today['close']:.2f}")
