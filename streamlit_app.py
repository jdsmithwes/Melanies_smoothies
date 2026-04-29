# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests

# Snowflake credentials are loaded from Streamlit secrets.
cnx = st.connection("snowflake")
session = cnx.session()

# ❌ MOVED UP - my_dataframe was used in multiselect before it was defined
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write("""Choose the fruits you want in your custom Smoothie!""")

name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:', name_on_order)

ingredients_list = st.multiselect('Choose up to 5 ingredients:', my_dataframe, max_selections=5)

if ingredients_list:
    ingredients_string = ''  # ❌ was ' ' (space), should be empty string
    
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        
        st.subheader(fruit_chosen + ' Nutrition Information')  # ❌ missing space before 'Nutrition'
        smoothiefroot_response = requests.get(f"https://my.smoothiefroot.com/api/fruit/{fruit_chosen}")
        sf_df = st.dataframe(smoothiefroot_response.json(), width='stretch')  # ❌ deprecated use_container_width

    time_to_insert = st.button("Submit Order")  # ❌ moved inside if block, and outside the for loop

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
                        values ('""" + ingredients_string.strip() + """','""" + name_on_order + """')"""  # ❌ had extra double-quote before closing ')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
        st.write(my_insert_stmt)
        st.stop()

    