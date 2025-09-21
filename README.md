# Sales Insights Multi-Agent

## Overview

This project demonstrates a multi-agent system designed for sophisticated data analysis and is built using sample code and patterns from [Google ADK Python Data Science multi-agent example](https://github.com/google/adk-samples/tree/main/python/agents/data-science#data-science-with-multiple-agents). It integrates several specialized agents to handle different aspects of the data pipeline, from data retrieval to advanced analytics and machine learning. The system is built to interact with BigQuery, perform complex data manipulations, generate data visualizations and execute machine learning tasks using BigQuery ML (BQML). The agent can generate text response as well as visuals, including plots and graphs for data analysis and exploration.


## Agent Details
The key features of the Data Science Multi-Agent include:

| Feature | Description |
| --- | --- |
| **Interaction Type:** | Conversational |
| **Complexity:**  | Advanced |
| **Agent Type:**  | Multi Agent |
| **Components:**  | Tools, AgentTools, Session Memory, RAG |
| **Vertical:**  | All (Applicable across industries needing advanced data analysis) |


### Architecture
![Data Science Architecture](data-science-architecture.png)

### Key Features

*   **Multi-Agent Architecture:** Utilizes a top-level agent that orchestrates sub-agents, each specialized in a specific task.
*   **Database Interaction (NL2SQL):** Employs a Database Agent to interact with BigQuery using natural language queries, translating them into SQL.
*   **Data Science Analysis (NL2Py):** Includes a Data Science Agent that performs data analysis and visualization using Python, based on natural language instructions.
*   **Machine Learning (BQML):** Features a BQML Agent that leverages BigQuery ML for training and evaluating machine learning models.
*   **Code Interpreter Integration:** Supports the use of a Code Interpreter extension in Vertex AI for executing Python code, enabling complex data analysis and manipulation.
*   **ADK Web GUI:** Offers a user-friendly GUI interface for interacting with the agents.
*   **Testability:** Includes a comprehensive test suite for ensuring the reliability of the agents.

### Visualization Examples

![Graph Showing Total Sales Per Product In USA](https://i.imgur.com/kFbBFtS.png)

![Training Forecasting Model Using BQML](https://i.imgur.com/VsvSxE7.png)

## Setup and Installation

### Prerequisites

*   **Google Cloud Account:** You need a Google Cloud account with BigQuery enabled.
*   **Python 3.12+:** Ensure you have Python 3.12 or a later version installed.
*   **uv:** Install uv by following the instructions on the official uv website: [https://docs.astral.sh/uv/getting-started/installation/](https://docs.astral.sh/uv/getting-started/installation/)
*   **Git:** Ensure you have git installed. If not, you can download it from [https://git-scm.com/](https://git-scm.com/) and follow the [installation guide](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git).



### Project Setup with uv

1.  **Clone the Repository:**

    ```bash
    git clone https://github.com/wovensoul/sales-insights-agent
    cd .\sales-analytics\
    ```

2.  **Install Dependencies with uv:**

    ```bash
    uv sync
    ```

    This command reads the `pyproject.toml` file and installs all the necessary
    dependencies into a virtual environment managed by uv. On the first run,
    this command will also create a new virtual environment. By default, the
    virtual environment will be created in a `.venv` directory inside
    `adk-samples/python/agents/data-science`. If you already have a virtual
    environment created, or you want to use a different location, you can use
    the `--active` flag for `uv` commands, and/or change the
    `UV_PROJECT_ENVIRONMENT` environment variable. See
    [How to customize uv's virtual environment location](https://pydevtools.com/handbook/how-to/how-to-customize-uvs-virtual-environment-location/)
    for more details.

2.  **Activate the uv Shell:**

    If you are using the `uv` default virtual environment, you now need
    to activate the environment.

    ```bash
    source .venv/bin/activate
    ```

4.  **Set up Environment Variables:**
    Rename the file ".env.example" to ".env"
    Fill the below values:

    ```bash
    # Choose Model Backend: 0 -> ML Dev, 1 -> Vertex
    GOOGLE_GENAI_USE_VERTEXAI=1

    # ML Dev backend config. Fill if using Ml Dev backend.
    GOOGLE_API_KEY='YOUR_VALUE_HERE'

    # Vertex backend config
    GOOGLE_CLOUD_PROJECT='YOUR_VALUE_HERE'
    GOOGLE_CLOUD_LOCATION='YOUR_VALUE_HERE'
    ```

    Follow the following steps to set up the remaining environment variables.

5.  **BigQuery Setup:**
    These steps will load the sample data provided in this repository to BigQuery.
    For our sample use case, we are working on the Cosmetics & Skincare Product Sales data from Kaggle:

    _Atharva Soundankar. Cosmetics & Skincare Product Sales Data. https://www.kaggle.com/datasets/atharvasoundankar/cosmetics-and-skincare-product-sales-data-2022, 2022. Kaggle._

    To generate train.csv and test.csv for BigQuery, insert `YOUR_DATA_SET` in `utils/data/` and run:
    ```bash
    python3 data_science/data_preprocessing.py `YOUR_DATA_SET`.csv
    ```

    *   First, set the BigQuery project IDs in the `.env` file. This can be the
        same GCP Project you use for `GOOGLE_CLOUD_PROJECT`, but you can use
        other BigQuery projects as well, as long as you have access permissions
        to that project.
        *   In some cases you may want to separate the BigQuery compute consumption from
            BigQuery data storage. You can set `BQ_DATA_PROJECT_ID` to the project you use
            for data storage, and `BQ_COMPUTE_PROJECT_ID` to the project you want
            to use for compute.
        *   Otherwise, you can set both `BQ_DATA_PROJECT_ID` and
            `BQ_COMPUTE_PROJECT_ID` to the same project id.

        If you have an existing BigQuery table you wish to
        connect, specify the `BQ_DATASET_ID` in the `.env` file as well.
        Make sure you leave `BQ_DATASET_ID='cosmetics_store_sales'` if you
        wish to use the sample data.

        Alternatively, you can set the variables from your terminal:

        ```bash
        export BQ_DATA_PROJECT_ID='YOUR-BQ-DATA-PROJECT-ID'
        export BQ_COMPUTE_PROJECT_ID='YOUR-BQ-COMPUTE-PROJECT-ID'
        export BQ_DATASET_ID='YOUR-DATASET-ID' # leave as 'cosmetics_store_sales' if using sample data
        ```

        You can skip the upload steps if you are using your own data. We recommend not adding any production critical datasets to this sample agent.
        If you wish to use the sample data, continue with the next step.

    *   You will find the datasets inside 'data-science/data_science/utils/data/'.
        Make sure you are still in the working directory (`agents/data-science`). To load the test and train tables into BigQuery, run the following commands:
        ```bash
        python3 data_science/utils/create_bq_table.py
        ```


6.  **BQML Setup:**
    The BQML Agent uses the Vertex AI RAG Engine to query the full BigQuery ML Reference Guide.

    Before running the setup, ensure your project ID is added in .env file: `"GOOGLE_CLOUD_PROJECT"`.
    Leave the corpus name empty in the .env file: `BQML_RAG_CORPUS_NAME = ''`. The corpus name will be added automatically once it's created.

    To set up the RAG Corpus for your project, run the methods `create_RAG_corpus()` and `ingest_files()` in
    `data-science/data_science/utils/reference_guide_RAG.py` by running the below command from the working directory:

    ```bash
    python3 data_science/utils/reference_guide_RAG.py
    ```


7.  **Other Environment Variables:**

    *   `NL2SQL_METHOD`: (Optional) Either `BASELINE` or `CHASE`. Sets the method for SQL Generation. Baseline uses Gemini off-the-shelf, whereas CHASE uses [CHASE-SQL](https://arxiv.org/abs/2410.01943)
    *   `CODE_INTERPRETER_EXTENSION_NAME`: (Optional) The full resource name of
        a pre-existing Code Interpreter extension in Vertex AI. If not provided,
        a new extension will be created. (e.g.,
        `projects/<YOUR_PROJECT_ID>/locations/<YOUR_LOCATION>/extensions/<YOUR_EXTENSION_ID>`).
        Check the logs/terminal for the ID of the newly created Code Interpreter
        Extension and provide the value in your environment variables to avoid
        creating multiple extensions.

    From the terminal:

    ```bash
    export CODE_INTERPRETER_EXTENSION_NAME='projects/<YOUR_PROJECT_ID>/locations/us-central1/extensions/<YOUR_EXTENSION_ID>'
    ```

## Running the Agent

You can run the agent using the ADK command in your terminal.
from the working directory:

1.  Run agent in CLI:

    ```bash
    uv run adk run data_science
    ```

2.  Run agent with ADK Web UI:
    ```bash
    uv run adk web
    ```
    Select the data_science from the dropdown



### Example Agent Interaction

Here's a quick example of how a user might interact with the Data Science Multi-Agent System:

> ´**User:** Hi, What data do you have access to?

> **Agent:**  I have access to two tables: `train` and `test`. Both tables contain cosmetics sales data with the following columns: `sales_person`, `country`, `product`, `date`, `amount_usd`, and `box_shipped`.

> **User:** I need more details on the train table. What countries exist? 

> **Agent:** Result: The distinct countries in your database are: Australia, Canada, India, New Zealand, UK, and USA.

>Explanation: I queried the sales-analytics-adk.cosmetic_store_sales.train table to retrieve all unique values from the Country column.

> **User:** Please generate a plot with total sales per country.

> **Agent:**  Result: A bar plot has been generated showing the total sales per country. The x-axis represents the country, and the y-axis represents the total sales.

> Explanation:
> 1. The database agent was first called to retrieve the total sales per country from the train table.
> 2. The data science agent was then called to generate a bar plot visualizing the results. The plot displays each country on the x-axis and its corresponding total sales on the y-axis.

> **User:** What kinds of forecasting models can I train in BQML?

> **Agent:** You can train several types of forecasting models in BQML, including ARIMA, Exponential Smoothing, and Temporal Fusion Transformer (TFT) models. Would you like to proceed with training a forecasting model?

> **User:** Yes

> **Agent:** Okay, before proceeding, let's confirm the project and dataset ID for BQML. We'll be using the `PROJECT_ID` project and the `forecasting_sticker_sales` dataset. Does that sound right?

> **User:** Yes

> **Agent:** The BQML supports `ARIMA_PLUS`, `ARIMA_PLUS_XREG`.

>To proceed, I need to know which model you'd like to use. I also need to know the following:

>*   The name of the column that provides the time points (e.g., 'date').
>*   The name of the column that contains the data to forecast (e.g., 'num_sold').
>*   Do you want to fit and forecast multiple time series using a single query? If so, what are the ID columns? (e.g., `country`, `store`, `product`)


### Clean up

You can clean up this agent sample by:
- Deleting the [Cloud Run Services](https://console.cloud.google.com/run).
- Deleting the [Cloud SQL instance](https://console.cloud.google.com/sql/instances).


## Disclaimer

This agent sample is provided for illustrative purposes only and is not intended for production use. It serves as a basic example of an agent and a foundational starting point for individuals or teams to develop their own agents.

This sample has not been rigorously tested, may contain bugs or limitations, and does not include features or optimizations typically required for a production environment (e.g., robust error handling, security measures, scalability, performance considerations, comprehensive logging, or advanced configuration options).

Users are solely responsible for any further development, testing, security hardening, and deployment of agents based on this sample. We recommend thorough review, testing, and the implementation of appropriate safeguards before using any derived agent in a live or critical system.
