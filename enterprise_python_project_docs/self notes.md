### run.py
This file is the main entry point of running the app. without this we will have to do `uvicorn app.main:app`

but with this we do `python run.py --env prod` 

this is done to specify the environment app has to run on by passing it as a flag which cant be done in case of uvicorn. 

### pyproject.toml
