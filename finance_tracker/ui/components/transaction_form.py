import streamlit as st
from services.transaction_service import TransactionService
from datetime import datetime


def render_transaction_form():
    st.title("Add Transaction")
    user_id = st.session_state.get('user_id')
    predicted_cat = None
    with st.form(key='txn_form'):
        amount = st.number_input('Amount', min_value=0.01, format='%f')
        date = st.date_input('Date', value=datetime.now().date())
        category = st.text_input('Category (leave empty to auto-categorize)')
        ttype = st.selectbox('Type', ['expense', 'income'])
        description = st.text_area('Description')
        col1, col2 = st.columns([1, 1])
        with col1:
            predict_btn = st.form_submit_button('Predict Category')
        with col2:
            save_btn = st.form_submit_button('Save')

        if predict_btn:
            if not description:
                st.error('Provide a description to predict category')
            else:
                try:
                    from ai_modules.transaction_classifier import TransactionClassifier
                    clf = TransactionClassifier(model_dir='ai_modules/models')
                    predicted_cat = clf.predict(description) or 'Uncategorized'
                    st.info(f'Predicted category: {predicted_cat}')
                except Exception:
                    st.warning('Classifier not available or model not trained')

        if save_btn:
            # If user didn't provide category, try classifier prediction on-the-fly
            final_category = category if category else None
            svc = TransactionService()
            res = svc.add_transaction(user_id, float(amount), date.isoformat(), final_category, ttype, description)
            if res:
                st.success('Transaction saved')
            else:
                st.error('Failed to save transaction')
