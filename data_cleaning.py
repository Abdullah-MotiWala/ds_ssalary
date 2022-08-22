import pandas as pd

df = pd.read_csv('glass_door.csv')

# Salary Parsing//
# State Field only
# Age of company

# Salary parsing
df = df[df["Salary Estimate"] != '-1']
# Extracting exact nums from salary
salaries = df["Salary Estimate"].apply(lambda x: x.split('(')[0])
salaries = salaries.apply(lambda x: x.split('/')[0])
salaries = salaries.apply(lambda x: x.split("$")[1])
salaries = salaries.apply(lambda x: x.replace(",", ""))
df["Salary Estimate"] = salaries

# cleaning the ratings
df = df[df["Rating"] != -1]

# Extrating State from location
df["Location"] = df["Location"].apply(lambda x: x.split(',')[0])
print(df["Location"])

# cleaning size of company and getting min and max size of company
df = df[df["Size"] != '-1']
df = df[df["Size"] != "Unknown"]
df["Size"] = df["Size"].apply(lambda x: x.replace("+", "1"))
df["Size"] = df["Size"].apply(lambda x: x.replace("Employees", ""))
df["min_size"] = df["Size"].apply(lambda x: x.split(" ")[0])
df["max_size"] = df["Size"].apply(
    lambda x: x.split("to ")[1] if "to" in x else x)
print(df["Size"])


# cleaning founded
df["Founded"] = df["Founded"].apply(lambda x: x if x.isnumeric() else -1)
df = df[df["Founded"] != -1]
print(df["Founded"])


# cleaning industry
df = df[df["Industry"] != -1]

# cleanging sector
df = df[df["Sector"] != -1]

# cleaning revenue
df = df[df["Revenue"] != -1]
df = df[df["Revenue"] != "Unknown"]
df = df[df["Revenue"] != "Unknown / Non-Applicable"]

revenues = df["Revenue"].apply(lambda x:x.replace("Less than", "1 to"))
revenues = revenues.apply(lambda x: x.split("(")[0])
revenues = revenues.apply(lambda x: x.replace("+", "0.01"))
revenues = revenues.apply(lambda x: x.replace("$", ""))
# getting min and max revenue from range and if range is not available so min and max are same values
revenues = revenues.apply(lambda x: x.split(" "))

df["min_revenue"] = revenues.apply(lambda x: x[0])
df["max_revenue"] = revenues.apply(lambda x: x[2] if (len(x) > 3) else x[0])
# revenue currency
df["revenue_currency"] = revenues.apply(lambda x: x[-2])
print(revenues)


df.columns

df_out = df.drop(["Unnamed: 0", "Revenue", "Size"], axis=1)

df_out.to_csv("salary_data_cleaned.csv", index=False)
