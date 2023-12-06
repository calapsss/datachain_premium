import streamlit as st

from app_pages.backend.sqlchain_backend import SQLChain

def create_page():
    st.markdown("<h2 style='text-align: center;padding-top: 0rem;'>Natural Language SQL Querying</h2>", unsafe_allow_html=True)
    def query_page():
        # Replace the Django form with Streamlit's input functions
        query = st.text_input('Enter your query')\
        # get list of sql tables
        tables = get_table_list()
        #drop down option to select table
        table = st.selectbox('Select table', tables)
        per_page = 10
        columns, rows = [], []

        if query and table:
            # Prompt to query with sqlchain
            sqlchain = SQLChain()
            connection = sqlchain.connect()
            query = sqlchain.create_query(query, table, "gpt-3.5-turbo-1106")

            with connection.cursor() as cursor:
                try:
                    cursor.execute(query)
                    rows = cursor.fetchall()
                    columns = [col[0] for col in cursor.description]
                except Exception as e:  # Be more specific with exception handling
                    rows = []
                    # Handle the exception or display it in the template

            # Replace the Django pagination with a simple slicing operation
            page = st.number_input('Enter page number', min_value=1, value=1)
            start = (page - 1) * per_page
            end = start + per_page
            rows = rows[start:end]
            #column names into row
            rows.insert(0, columns)
            if st.button('Table View'):
                st.table(rows)

            if st.button('Text View'):
                # Replace the Django template rendering with Streamlit's display functions
                st.write('Columns:', columns)
                st.write('Rows:', rows)

    def get_table_list():
        # Fetch the list of tables using SQLChain
        sqlchain = SQLChain()
        connection = sqlchain.connect()
        query = "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"
        
        with connection.cursor() as cursor:
            cursor.execute(query)
            tables = cursor.fetchall()
        
        return [table[0] for table in tables]
    
    query_page()
