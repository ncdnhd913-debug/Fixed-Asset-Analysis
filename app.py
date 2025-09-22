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
        # 엑셀 파일 읽기
        df = pd.read_excel(uploaded_file, engine='openpyxl')
        
        # 컬럼명 정리 (불필요한 공백 제거 등)
        df.columns = df.columns.str.strip()
        
        # '자산계정' 컬럼이 있는지 확인
        if '자산계정' not in df.columns:
            st.error("업로드된 파일에 '자산계정' 컬럼이 없습니다. 올바른 파일을 업로드해주세요.")
            df = pd.DataFrame() # 데이터프레임 초기화
    except Exception as e:
        st.error(f"파일을 읽는 도중 오류가 발생했습니다: {e}")

# 3. 데이터가 존재할 때만 드롭다운 메뉴 및 데이터프레임 표시
if not df.empty:
    
    # '자산계정' 컬럼의 고유값들을 가져옴
    asset_accounts = sorted(df['자산계정'].unique())
    
    # 전체를 볼 수 있는 옵션 추가
    all_option = "전체"
    options_with_all = [all_option] + list(asset_accounts)
    
    # 드롭다운 메뉴 생성 (사이드바에 위치)
    selected_account = st.sidebar.selectbox("자산 계정을 선택하세요", options_with_all)
    
    # 선택된 계정에 따라 데이터 필터링
    if selected_account == all_option:
        filtered_df = df
    else:
        filtered_df = df[df['자산계정'] == selected_account]
    
    st.subheader(f"고정자산 명세서 - {selected_account} ({len(filtered_df)}건)")
    st.dataframe(filtered_df, use_container_width=True)

    st.markdown("---")
    
    # 고정자산 총계 정보 표시
    total_acquisition_cost = filtered_df['취득가액'].sum()
    total_book_value = filtered_df['장부가액'].sum()

    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="총 취득가액", value=f"{total_acquisition_cost:,.0f} 원")
    with col2:
        st.metric(label="총 장부가액", value=f"{total_book_value:,.0f} 원")
    
else:
    st.info("왼쪽 사이드바에서 엑셀 파일을 업로드해 주세요.")
