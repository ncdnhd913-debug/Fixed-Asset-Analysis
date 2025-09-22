import streamlit as st
import pandas as pd

# 제목 설정
st.title("📊 고정자산 분석 보고서")
st.markdown("---")

# 1. 사이드바 생성
st.sidebar.header("파일 업로드 및 필터링")

# 파일 업로더 생성 (사이드바에 위치)
uploaded_file = st.sidebar.file_uploader("고정자산 명세서 파일(.xlsx, .xls)을 업로드하세요", type=["xlsx", "xls"])

df = pd.DataFrame()

# 2. 파일 업로드 시 데이터 처리
if uploaded_file:
    try:
        # 엑셀 파일 읽기 (컬럼명을 직접 지정하여 J열과 AB열만 읽어옴)
        # 엑셀 컬럼은 0부터 시작하므로 J열은 9번째, AB열은 27번째 인덱스입니다.
        df = pd.read_excel(uploaded_file, usecols="J,AB", engine='openpyxl')
        
        # 컬럼명 정리 및 변경 (read_excel로 가져온 컬럼명을 변경)
        df.columns = ['취득가액', '장부가액']
        
        # '자산계정', '자산명' 등 추가 정보가 필요하므로 전체 파일 다시 읽기
        df_full = pd.read_excel(uploaded_file, engine='openpyxl')
        df_full.columns = df_full.columns.str.strip().str.replace(' ', '')
        
        # 필수 컬럼 확인 (자산계정, 자산명)
        required_columns = ['자산계정', '자산명']
        if not all(col in df_full.columns for col in required_columns):
            st.error("⚠️ 업로드된 파일에 '자산계정' 또는 '자산명' 컬럼이 누락되었습니다.")
            st.info("엑셀 파일의 컬럼명을 확인하고 수정해주세요.")
            df = pd.DataFrame()
        else:
            # 필요한 데이터만 가져와서 병합
            df_full['취득가액'] = df['취득가액']
            df_full['장부가액'] = df['장부가액']
            df = df_full
            
            # ✨ 수정된 부분: 숫자 컬럼을 명시적으로 숫자 타입으로 변환
            df['취득가액'] = pd.to_numeric(df['취득가액'], errors='coerce')
            df['장부가액'] = pd.to_numeric(df['장부가액'], errors='coerce')
            
            # 자산계정 및 자산명 공란 제거
            df = df.dropna(subset=['자산계정', '자산명'])
            
            # '자산계정' 컬럼을 문자열로 변환
            df['자산계정'] = df['자산계정'].astype(str)
            
    except Exception as e:
        st.error(f"파일을 읽는 도중 오류가 발생했습니다: {e}")

# 3. 데이터가 존재할 때만 드롭다운 메뉴 및 데이터프레임 표시
if not df.empty:
    
    # '자산계정' 컬럼의 고유값들을 가져옴
    asset_accounts = sorted(df['자산계정'].unique())
