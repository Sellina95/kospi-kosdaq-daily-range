import pandas as pd

def latest_high_low_from_naver_day(code: str):
    """
    네이버 종목 '일별시세' 표(시가/고가/저가 포함)를 읽어서
    가장 최근(첫 번째 유효 행)의 고가/저가를 반환.
    code: 네이버 종목코드 (예: 069500 KODEX 200, 229200 KODEX 코스닥150)
    """
    url = f"https://finance.naver.com/item/sise_day.naver?code={code}"
    # 네이버 표를 그대로 읽어오기 (여러 테이블 중 첫 번째가 가격표)
    tables = pd.read_html(url, header=0)  # 첫 행을 헤더로
    df = tables[0].dropna(how="all")      # 빈 행 제거

    # 일부 페이지는 공백 행이 섞일 수 있어 유효한 첫 행을 찾자
    # 유효 행: '날짜'가 문자열이고 '고가','저가'가 숫자로 파싱 가능한 행
    df = df.dropna(subset=["날짜", "고가", "저가"])
    df = df.reset_index(drop=True)

    # 숫자 컬럼 정리(쉼표 제거)
    for col in ["시가", "고가", "저가", "종가", "전일비", "거래량"]:
        if col in df.columns:
            df[col] = (
                df[col]
                .astype(str)
                .str.replace(",", "", regex=False)
                .str.strip()
                .replace("", pd.NA)
            )
            df[col] = pd.to_numeric(df[col], errors="coerce")

    latest = df.iloc[0]  # 표의 최상단이 가장 최근 날짜
    return {
        "date": latest["날짜"],
        "open": float(latest.get("시가", float("nan"))),
        "high": float(latest.get("고가", float("nan"))),
        "low":  float(latest.get("저가", float("nan"))),
        "close": float(latest.get("종가", float("nan")))
    }

# 코스피 / 코스닥 프록시 ETF 코드
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
