# -*- coding: utf-8 -*-
"""
Created on Tue Jul  4 16:42:14 2023

@author: mogit
"""

import pandas as pd
import streamlit as st
import openai
import matplotlib.pyplot as plt
import seaborn as sns
import os


openai.api_key = os.environ["OPENAI_API_KEY"]


def generate_visualization_code(prompt):
    # Use OpenAI's API to generate Python code for visualization
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=prompt,
        temperature=0.75,
        max_tokens=500,
        n=1,
        stop=None
    )

    # Extract the generated code from OpenAI's response
    visualization_code = response.choices[0].text.strip()

    return visualization_code

def main():
    #page setup 
    st.set_page_config(page_title="Table visualization", layout="wide")
    st.title("Table visualization")
    file=st.file_uploader("Kindly upload CSV file of the data you want to visualize", type='csv')
    if file is not None:
        file_csv=pd.read_csv(file)
        df=file_csv.sample(n=30)
        # Display the uploaded DataFrame
        st.subheader("Uploaded DataFrame")
        st.write(df)
        
        prompt=f"""
        Perform the following actions:
        1) Generate a python code to visualize the dataframe.
        2) Consider all necessary libraries and dataframe is imported, just generate only visualization code.
        3)The visualization plot should reveal exact information and relation between columns and rows.
        4)Output should only have code for 2 suitable plots and it should be readymade to deploy in streamlit app without any indentation errors and in below format
        5) Plot graphs between categorical vs numerical column or numerical vs numerical only. 
        output code format:
        st.subheader(Subplot name)
        fig(plot number), axis(plot number)=plt.subplots()
        sns.(suitable plot)(data=df,x=(suitable row),y=(suitable column),hue=(suitable column))
        plt.xticks(rotation=20,fontweight='light',fontsize='small')
        axis_no.set_xlabel(suitable x axis name)
        axis_no.set_ylabel(suitable y axis name)
        st.pyplot(fig(plot number))


        dataframe:
        ```{df[0:25]}```
        """
        executable_visualization_code=generate_visualization_code(prompt)
           
        list_of_codes=executable_visualization_code.splitlines()
        for code in list_of_codes:
              exec(code)
    


if __name__ == "__main__":
    main()


