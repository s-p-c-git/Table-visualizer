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

## File structure
```
Table-visualizer/
├─ LICENSE
├─ Table_visualizer.py
├─ README.md
├─ requirements.txt
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


The Python application directory structure should now look like the following:
```
quote_gen
|____ static
|____ templates
|____ app.py
|____ requirements.txt
|____ Dockerfile
```
```
quote_disp
|____ static
|____ templates
|____ app.py
|____ requirements.txt
|____ Dockerfile
```

Let's create a basic container in each of the directories
```
FROM python:3.8-slim-buster
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT [ "python" ]
CMD [ "app.py" ]
```

Let's see what each of these commands means -

<br> FROM python - gets a Python distribution from Docker Images </br>
<br> WORKDIR Changes the working directory </br>
<br> COPY Copies the content of Workdir into a new directory </br>

Build the Docker Images - 
```
cd quote_gen
```
```
docker build --tag quote-gen-service .
```
```
cd quote_disp
```
```
docker build --tag quote-disp-service .
```

Run Docker Container

With the Docker images created, let’s get the containers up and running
```
cd quote_gen
docker run --name quote-gen-container -p 84:84 quote-gen-service
```
```
cd quote_disp
docker run --name quote-disp-container -p 85:85 quote-disp-service
```

Let’s run docker container ls to get a list of containers created

Create Docker Network

```
docker network create quote-network
```
and running the followng command
```
docker network inspect quote-network
```

Let's add our containers to the quote-network

```
docker network connect quote-network quote-gen-container
docker network connect quote-network quote-disp-container
docker network inspect quote-network
```
You see the following output - 

```
[
    {
        "Name": "quote-network",
        "Id": "999c81eb87c4b687921ea474abd1e59875447a96d2477ae190dcccc40f882d8a",
        "Created": "2023-04-24T04:45:15.9081804Z",
        "Scope": "local",
        "Driver": "bridge",
        "EnableIPv6": false,
        "IPAM": {
            "Driver": "default",
            "Options": {},
            "Config": [
                {
                    "Subnet": "172.19.0.0/16",
                    "Gateway": "172.19.0.1"
                }
            ]
        },
        "Internal": false,
        "Attachable": false,
        "Ingress": false,
        "ConfigFrom": {
            "Network": ""
        },
        "ConfigOnly": false,
        "Containers": {
            "2636f9d91e5468029981d499fc7e0b46a204d8fc3b16e5e7e6e912651ce8dd4a": {
                "Name": "quote-disp-container",
                "EndpointID": "a4eb7320b1585b43a10499a73059e8f50fb8d5e33f9aee433b1b7e5e0b1dee85",
                "MacAddress": "02:42:ac:13:00:03",
                "IPv4Address": "172.19.0.3/16",
                "IPv6Address": ""
            },
            "557e1ff9f220704ad9f76d94ebe5d3c433dc20ed44798831af6f2bfe68176583": {
                "Name": "quote-gen-container",
                "EndpointID": "191f2b22ec8a92256d47b152a06eeaeead9f05a13799f48d43d9c5410daceebb",
                "MacAddress": "02:42:ac:13:00:02",
                "IPv4Address": "172.19.0.2/16",
                "IPv6Address": ""
            }
        },
        "Options": {},
        "Labels": {}
    }
]
```

Let's see if the dockers are communicating
```
StatusCode        : 200
StatusDescription : OK
Content           : <link rel="stylesheet" href="/static/css/style.css">
                    <title>Docker App Quote </title>
                    <div class="screen">
                      <div class="screen-image"></div>
                      <div class="screen-overlay"></div>
                      <div class="screen-...
RawContent        : HTTP/1.1 200 OK
                    Connection: close
                    Content-Length: 503
                    Content-Type: text/html; charset=utf-8
                    Date: Mon, 24 Apr 2023 04:51:36 GMT
                    Server: Werkzeug/2.2.3 Python/3.8.16

                    <link rel="stylesheet" hre...
Forms             : {}
Headers           : {[Connection, close], [Content-Length, 503], [Content-Type, text/html; charset=utf-8], [Date, Mon, 24 Apr  
                    2023 04:51:36 GMT]...}
Images            : {}
InputFields       : {}
Links             : {@{innerHTML=; innerText=; outerHTML=<A class=link href="https://youtube.com/@Hyperplexed"
                    target=_blank></A>; outerText=; tagName=A; class=link; href=https://youtube.com/@Hyperplexed;
                    target=_blank}}
ParsedHtml        : mshtml.HTMLDocumentClass
RawContentLength  : 503
```
They seem to be working!

Let's create a Docker Compose Manifest to orchestrate our services

```
version: "3.7"
services:
  web1:
    build: ./quote_gen
    container_name: gen
    ports:
      - "5000:5000"
  web2:
    build: ./quote_disp
    container_name: disp
    expose:
      - "5000"
    ports:
      - "5001:5000"
    depends_on:
      - web1
```

Let's understand the commands in our Compose YAML file -

version: - Compose file versions that run our Docker Compose

services: the components or services that run within the docker-compose manifest

Eg - Our website is a service, we can have a database service or a unit testing service, an application server, etc

Under service, we have our website - service name, build - looks for a docker image, context - specifies where to look

ports: -80:80

Run Docker Compose
