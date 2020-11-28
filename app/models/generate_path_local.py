database_name = "capstone_test"
user = "postgres"
pw = "gun125"
database_path = f"postgresql://{user}:{pw}@localhost:5432/{database_name}"
print(database_path)
