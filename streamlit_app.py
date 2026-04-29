# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests

# Snowflake credentials are loaded from Streamlit secrets.
cnx = st.connection("snowflake")
session = cnx.session()

# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothie!
    """
)
name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on you Smoothie will be:',name_on_order)

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

ingredients_list = st.multiselect('Choose up to 5 ingredients:', my_dataframe, max_selections=5)

if ingredients_list:
    ingredients_string = ' '
    
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '


    time_to_insert = st.button("Submit Order")


    
    
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
                        values ('""" + ingredients_string + """','"""+name_on_order+ """"')"""

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")

    st.write(my_insert_stmt)
    st.stop()

    #New section to display smoothiefroot nutrition information

    smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
    st.text(smoothiefroot_response.json())
