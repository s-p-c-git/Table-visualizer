# Table-visualizer 📑
Streamlit app to visualize charts/graphs from the given Table
# Goal 🥅
## Deploy a streamlit app with OpenAI integration to visualize tables.
### For this task we will be integrating OpenAI API with streamlit app.
### Then with out prompt we'll generate visualization of table data uploaded by the users.

## Environment Setup - Things needed to run Project ☑️
<br> Python </br> 
<br> OpenAI </br>
<br> Pandas </br>
<br> streamlit </br>
<br> seaborn </br>
<br> Matplotlib </br>

## Python application directory structure 📁
```
Table-visualizer/
|____ LICENSE
|____ Table_visualizer.py
|____ README.md
|____ requirements.txt

```

### LICENSE - Apache2.0
### Table_visualizer.py - Main application code.
### requirements.txt - Requirements file which has all the dependencies.


## Project approach 📈

The Table_visualizer.py code is developed in a way that, once user uploads the .csv file in the streamlit front-end page, it will analyse
the data, convert it to dataframe and creates a code to display graphs/charts based on the data. Since our objective to integrate the OpenAI and most of the models works well with text generation and text completion. We leverage it to generate code for our case and execute it to display visualization.


### Assumptions :

The user will uploads a data file (preferrably csv for this task) in the streamlit user interface, and the openAI model will slice it upto 30 rows and creates a dataframe out of it and feed it to our prompt, which will analyse and generate a visualization code to display graphs/charts. 


## Code workflow 🧮

**generate_visualization_code** function will take our prompt as input and generates the required code in the format, we specified.
Model _'text-davinci-003'_ is used with _temperature_ value of 0.75 and _max_tokens=1000_. In our case mostly tokens will be in the range of 500-600, Since I
have restricted the input dataframe size upto 30 rows to avoid exceeding model token limit (and of course free-trial limit...)
```
def generate_visualization_code(prompt):
    # Use OpenAI's API to generate Python code for visualization
    response = openai.Completion.create(
        engine='text-davinci-003', 
        prompt=prompt,
        temperature=0.75, #0.75 gives pretty much consistent values.
        max_tokens=1000,   #restricting max tokens to 600.
        n=1,
        stop=None
    )
```
The **main()** function has the attributes that constructs streamlit frontend and displays the dataset. It stores the output from OpenAI response as string in 
**executable_visualization_code** variable. To execute the code, we are splitting as list of lines and iterating over a for loop to apply exec() function. 
The below code will try execute each lines and ignores any exception errors mentioned below.

```
executable_visualization_code=generate_visualization_code(prompt)

        list_of_codes=executable_visualization_code.splitlines()
         for code in list_of_codes:
            try :
                exec(code)
            except (SyntaxError, ValueError, IndentationError):
                continue 
```
## Note: The error part is inevitable with the openAI model, we can sense drift from the responses made by the model sometimes.


## Prompt :
       """ Perform the following actions:
        1) Generate a python code to visualize the dataframe.
        2) Consider all necessary libraries and dataframe is imported, just generate only visualization code.
        3)The visualization plot should reveal exact information and relation between columns and rows.
        4)Output should only have code for 5 suitable plots and it should be readymade to deploy in streamlit app without any indentation errors and in below format
        5) Plot graphs between categorical vs numerical column or numerical vs numerical. 
        output code format:
        st.subheader(Subplot name)
        fig(plot number), axis(plot number)=plt.subplots()
        sns.(suitable plot)(data=df,x=(suitable row),y=(suitable column),hue=(suitable column))
        plt.xticks(rotation=20,fontweight='light',fontsize=5)
        axis_no.set_xlabel(suitable x axis name)
        axis_no.set_ylabel(suitable y axis name)
        st.pyplot(fig(plot number))


        dataframe:
        ```{df}```

        """

### This is the prompt I have used for the model to generate the visualization code. We are instructing model to assume all the necessary modules are immported so now model only gives us the code in the format we mentioned for upto 5 charts/graphs.


# Workflow :
## 1) User uploads csv file 📂

![image](https://github.com/Mogith-P-N/Table-visualizer/assets/113936190/c11e109d-872d-4f15-b743-a1fcd1c2bbf6)

## 2) Preview of uploaded Table 📇

![graphs](https://github.com/Mogith-P-N/Table-visualizer/assets/113936190/7951863f-4dba-4b01-a023-d53426873153)


## 3) Sample Graphs/chart 📊

![image](https://github.com/Mogith-P-N/Table-visualizer/assets/113936190/a1b9c56e-53a2-4ecd-84b3-2fcbb720d472)

![image](https://github.com/Mogith-P-N/Table-visualizer/assets/113936190/723da5bf-c236-489f-8821-07be619555d4)




## Limitations 🚪

1) The model is limited to input token of 4096, so the code is written in a way it will slice the table and randomly picks 30 rows for the analysis. But the more the data, more the visualization will be appealing and model can actually produce great results with higher amount of data.

2) Input file format - For the timebeing now the file user can be upload for the analysis should be csv.

3) Visualization output - I have now prompted the model to produce maximum of 5 graphs for display. This is again due to the output token constraint of the openAI API.

4) Model response inconsistencies - The executable code generated from the model might have "TypeError", "IndentationError", "SyntaxError", this is due to we are executing the string file and even though we defined a particular structure, still model tends to throw some randomness and that results in incomplete output or error ( Mostly refreshing the page or trying again will work).

5) Free trial API credits limitation - Since the openAi free trial only accounts for $5 credits, we may exhaust the credit limits in few days, that's the main reason for restricting the model to ingest and slice only part of data and max of 5 charts as output.

We can tweak around and remove below .sample function from our dataframe to process all the data for better results. 

```
df=file_csv.sample(n=30)
```


## Future ideas 💡 :


