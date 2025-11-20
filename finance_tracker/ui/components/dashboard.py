import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from services.transaction_service import TransactionService
from services.budget_service import BudgetService


def render_dashboard():
    """Render main dashboard with charts and metrics."""
    st.title("📊 Financial Dashboard")

    transaction_service = TransactionService()
    budget_service = BudgetService()
    user_id = st.session_state.get('user_id')

    col1, col2, col3, col4 = st.columns(4)

    transactions = transaction_service.get_recent_transactions(user_id, limit=100)

    with col1:
        total_income = sum([t['amount'] for t in transactions if t.get('transaction_type') == 'income'])
        st.metric("Total Income", f"${total_income:,.2f}")

    with col2:
        total_expense = sum([t['amount'] for t in transactions if t.get('transaction_type') == 'expense'])
        st.metric("Total Expenses", f"${total_expense:,.2f}")

    with col3:
        net_savings = total_income - total_expense
        st.metric("Net Savings", f"${net_savings:,.2f}")

    with col4:
        budget_status = budget_service.get_budget_status(user_id)
        st.metric("Budget Status", f"{budget_status}%")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Spending by Category")
        category_data = transaction_service.get_category_breakdown(user_id)
        if category_data:
            fig = px.pie(category_data, values='amount', names='category', title="Expense Distribution")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No expense data to show yet.")

    with col2:
        st.subheader("Income vs Expenses (Monthly)")
        monthly_data = transaction_service.get_monthly_comparison(user_id)
        if monthly_data['month']:
            fig = go.Figure(data=[
                go.Bar(name='Income', x=monthly_data['month'], y=monthly_data['income']),
                go.Bar(name='Expenses', x=monthly_data['month'], y=monthly_data['expense'])
            ])
            fig.update_layout(barmode='group')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Not enough data for monthly comparison.")

    st.subheader("Recent Transactions")
    st.dataframe(transactions or [], use_container_width=True)
