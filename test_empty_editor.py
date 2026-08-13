import streamlit as st
import pandas as pd

cols = ['id', 'date', 'type', 'amount', 'currency', 'account_name', 'destination_account_name', 'category_name', 'description', 'status', 'is_recurring']
df = pd.DataFrame(columns=cols)

print(df[cols])
