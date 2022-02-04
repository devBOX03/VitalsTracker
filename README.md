# VitalsTracker

VitalTracker will store vitals reading info from wearable/medical devices for every 15 mins basis and will deliver aggreagted data using as per the user's requirements. Other than this VitalsTraker has a simulator which will simulate data for users in random to get some data for testing.

## Setup envoronment
 To setup environment we can create a new vitual environment or can use system environment.

## Instalation
Therre are few package that need to be installed to make this setup work. So, use below command to install them.
```bash
pip install -r requirements.txt
```

## How to Use the Project

### Start Server
* Now we'll start flask server to make API's available to be used.
```bash
python src/app.py
```
* Along with starting server, we'll initialize the CSV file for storage with empty value.
  > data/aggregated_vital_info.csv

### Simulate Data
* Data simulation will generate vitals info for diffrent users and then it'll process it.
* After processing it will aggreagte all the data by user and 15 mins time interval.
* Finally aggregated data will get store into previously initialized CSV file using POST API.

```bash
python src/vital_simulator.py
```

### Access Data
* To acess data use below GET API.
* Here minutes are in 15 mins slot basis. So, while adding minutes please make sure it falls in this pattern 15, 30, 35, 60 and so on.....
> http://localhost:3000/vitals_output?user_id=Joe&minutes=30

## Comments
It's a small pet project and I hope you like it as handson project. Please add comments if you want to suggest any changes or improvements.

## License
[MIT](https://choosealicense.com/licenses/mit/)
