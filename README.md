# Table-visualizer
Streamlit app to visualize charts/graphs from the given Table
# Goal
## Deploy a streamlit app with OpenAI integration to visualize tables.
### For this task we will be integrating OpenAI API with streamlit app.
### Then with out prompt we'll generate visualization of table data uploaded by the users.

## Environment Setup - Things needed to run Project 
<br> Python </br>
<br> OpenAI </br>
<br> Pandas </br>
<br> streamlit </br>
<br> seaborn </br>
<br> Matplotlib </br>

## Python application directory structure
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


## Project approach :

The Table_visualizer.py code is developed in a way that, once user uploads the .csv file in the streamlit front-end page, it will analyse
the data, convert it to dataframe and creates a code to display graphs/charts based on the data. Since our objective to integrate the OpenAI and most of the models works well with text generation and text completion. We leverage it to generate code for our case and execute it to display visualization.


## Code workflow :

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
## Note: The error part is inevitable with the "text-davinci-model" as even though it is powerfull model, it drift away sometimes and send codes with indentation and type errors.

## 1) User uploads csv file.

![image](https://github.com/Mogith-P-N/Table-visualizer/assets/113936190/c11e109d-872d-4f15-b743-a1fcd1c2bbf6)

## 2) Preview of uploaded Table.

![image](https://github.com/Mogith-P-N/Table-visualizer/assets/113936190/2f5c982c-8a1b-4d85-84f6-a7a3638abf88)

## 3) Sample Graph/chart.

![image](https://github.com/Mogith-P-N/Table-visualizer/assets/113936190/542ad42e-bcdb-4f7d-9a18-60f93461e2e6)





