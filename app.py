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
        
        # ✨ 수정된 부분: 컬럼명에서 공백 제거 (strip()보다 강력)
        df.columns = df.columns.str.strip().str.replace(' ', '')
        
        # '자산계정', '자산명' 등 필수 컬럼명 정의
        required_columns = ['자산계정', '자산명', '취득가액', '장부가액']
        
        # 실제 데이터프레임의 컬럼명 목록
        df_columns = list(df.columns)
        
        # 누락된 필수 컬럼 찾기
        missing_columns = [col for col in required_columns if col not in df_columns]
        
        # 누락된 컬럼이 있으면 오류 메시지 출력
        if missing_columns:
            st.error(f"⚠️ 업로드된 파일에 다음 필수 컬럼이 누락되었습니다: {', '.join(missing_columns)}")
            st.info("엑셀 파일의 컬럼명을 확인하고 수정해주세요.")
            df = pd.DataFrame() # 데이터프레임 초기화
        else:
            # 필수 컬럼이 모두 있을 경우 데이터 처리 계속 진행
            # '자산계정'과 '자산명' 컬럼의 공란 및 누락 데이터 제거
            df = df.dropna(subset=['자산계정', '자산명'])
            
            # '자산계정' 컬럼을 문자열로 변환
            df['자산계정'] = df['자산계정'].astype(str)
            
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

    ## 고정자산 총계 정보
    total_acquisition_cost = filtered_df['취득가액'].sum()
    total_book_value = filtered_df['장부가액'].sum()

    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="총 취득가액", value=f"{total_acquisition_cost:,.0f} 원")
    with col2:
        st.metric(label="총 장부가액", value=f"{total_book_value:,.0f} 원")

    st.markdown("---")

    ## 자산계정별 장부가액 합계
    st.subheader("계정별 장부가액 합계")
    
    # 자산계정별 장부가액 합계 계산
    account_summary = df.groupby('자산계정')['장부가액'].sum().reset_index()
    account_summary.columns = ['자산계정', '장부가액 합계']

    # 자산계정별 합계 데이터프레임 표시
    st.dataframe(account_summary, use_container_width=True)
        
else:
    st.info("왼쪽 사이드바에서 엑셀 파일을 업로드해 주세요.")
