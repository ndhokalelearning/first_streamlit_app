import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My parents have new Diner')

streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑 🍞 Hard-Boiled Free-Range Egg')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
#streamlit.dataframe(my_fruit_list)
streamlit.dataframe(fruits_to_show)

# create function
def get_fruityvice_data (this_fruit_choice) :
  fruityvice_response = fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normalized
  

# new section to display api response
streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
      streamlit.error('select a fruit to get info')
  else:
    #fruityvice_response = fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
    #fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    #streamlit.dataframe(fruityvice_normalized)
    back_from_function = get_fruityvice_data(fruit_choice)
    streamlit.dataframe(back_from_function)
except URLError as e:
  steramlit.error()
  

streamlit.header("Fruit load list contains:")
# snowfalek related functions
def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("SELECT * from fruit_load_list")
    return my_cur.fetchall()

# Add a button to load a fruit
if streamlit.button('get fruit load list') :
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_rows = get_fruit_load_list()
  streamlit.dataframe(my_data_rows)
  

#don't run any more code !!!
streamlit.stop()

# Let's put a pick list here so they can pick the fruit they want to include 
fruit_selected_2 = streamlit.multiselect("Pick a fruit:", list(my_fruit_list.index))
fruit_to_show_2 = my_fruit_list.loc[fruit_selected_2]
streamlit.text("thanks for adding:")
streamlit.dataframe(fruit_to_show_2)

add_my_fruit = streamlit.text_input("Add another fruit to fruit list")
streamlit.write("Thanks for adding fruit to list",add_my_fruit)
my_cur.execute("insert into FRUIT_LOAD_LIST values ('from streamlit')")

