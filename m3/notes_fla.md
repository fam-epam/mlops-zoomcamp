DEF: an ML pipeline is a sequence of steps that are executed in order. It is also referred more generically as "Workflow Orchestration".

Usual steps:
    - Data ingestion (data download)
    - transforming data
    - feature engineering (creating new features as needed)
    - preparing data for ML (prepare the X matrix and y target)
    - hyperparameters tuning
    - train the final model
    - save the model in the model registry

Possible tools:
    General workflows:
        - Airflow
        - Prefect
        - Mage
    ML specific workflows:
        - Kubeflow pipelines
        - MLflow pipelines

# Working with Mage:
- install Mage

```
python3 -m venv venv
source venv/bin/activate

git clone https://github.com/mage-ai/mlops.git
touch ~/.gitconfig
cd mlops
./scripts/start.sh

```
- access Mage at `http://localhost:6789`  

3.1 Data preparation: ETL and feature engineering  
    3.1.1.  Ingestion  
        3.1.1.1.    Creating a new project  
            - click/call the "Command Center" and click on "Text Editor"  
            - <kbd>right-rlick </kbd>  on the root of the files tree and select `New Mage Project`  
            - register the new project by doing:  
                - Select `Settings` from the left menu  
                - Select `Settings` from the new shown menu  
                - click on the `Register Project` button at the top right of teh page  
                - find the newly created project section and set a `Name`, `Path`, and enable `Currently selected project`  
                - save the settings  
                - switch to the new project (top left of the page)  

        3.1.1.2.    Create a data preparation pipeline  
            - select `Pipelines` from the left menu  
            - click on the `New` button to create a new pipeline then choose the `Standard` type of pipeline  

        3.1.1.3.    Ingest data
            - click on the `All blocks` button (middle page section) to create a "Data Loader" block (`All blocks`-> `Data Loader` -> `Base template (generic)`)
            - click on the `Save and Add` button
            - fill out the code section with the right code for retrieving the data
            - click on the "play " (triangle) button to run the code
        3.1.1.4.    Transform data  
            - open the "Text Editor"
            - create some utility folder/files (e.g. utils/data_preparation/cleaning.py)

    3.1.2.  Data Preparation
    3.1.3.  Build training sets
    3.1.4.  Data validations using built-in testing framework