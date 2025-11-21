import streamlit as st
from services.group_service import GroupService
from datetime import date


def render_group_panel(user_id: str):
    st.header("Groups & Shared Expenses")
    svc = GroupService()

    with st.expander("Create group"):
        name = st.text_input("Group name")
        desc = st.text_area("Description")
        if st.button("Create Group"):
            if not name:
                st.error("Name required")
            else:
                g = svc.create_group(owner_id=user_id, name=name, description=desc)
                if isinstance(g, dict) and g.get('error') == 'no_client':
                    st.error(g.get('message'))
                elif g:
                    st.success("Group created")
                else:
                    st.error("Failed to create group. See logs or check Supabase configuration.")

    with st.expander("Add expense to group"):
        groups = svc.repo.list_groups_for_user(user_id)
        group_options = {g['id']: g['name'] for g in groups}
        if not group_options:
            st.info("No groups found. Create a group first.")
            return
        group_id = st.selectbox("Group", options=list(group_options.keys()), format_func=lambda k: group_options[k])
        payer = st.text_input("Payer user id", value=user_id)
        amount = st.number_input("Amount", min_value=0.01, format="%.2f")
        desc = st.text_input("Description")
        dt = st.date_input("Date", value=date.today())
        split_mode = st.selectbox("Split mode", ['equal', 'custom'])
        members = svc.list_group_members(group_id)
        shares = []
        if split_mode == 'equal':
            if members:
                share = round(amount / len(members), 2)
                for u in members:
                    shares.append({'user_id': u, 'share_amount': share})
        else:
            st.write("Enter share for each member")
            for u in members:
                v = st.number_input(f"Share for {u}", min_value=0.0, format="%.2f")
                shares.append({'user_id': u, 'share_amount': float(v)})

        if st.button("Save Expense"):
            created = svc.add_expense(group_id=group_id, payer_id=payer, amount=amount, date_obj=dt, description=desc, shares=shares)
            if created:
                st.success("Expense added")
            else:
                st.error("Failed to add expense")

    with st.expander("Group balances"):
        groups = svc.repo.list_groups_for_user(user_id)
        if not groups:
            st.info("No groups to show balances for")
            return
        gid = st.selectbox("Choose group", options=[g['id'] for g in groups], format_func=lambda k: next((g['name'] for g in groups if g['id'] == k), k))
        balances = svc.compute_group_balances(gid)
        if not balances:
            st.info("No expenses recorded yet")
        else:
            for uid, bal in balances.items():
                st.write(f"User {uid}: {'₹' + format(bal, '.2f')}" )
