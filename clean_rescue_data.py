#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# In[43]:


sheet_id = "14XQR8Wcde-xX6O9Sh104Z5AsW8hWXF9keHhjFvqE-mo"

adoptables_gid = "915530316"
adopted_gid = "990528153"

adoptables_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={adoptables_gid}"
adopted_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={adopted_gid}"

current_dogs = pd.read_csv(adoptables_url)
adopted_dogs = pd.read_csv(adopted_url)

current_dogs.columns = current_dogs.columns.str.strip().str.title()
adopted_dogs.columns = adopted_dogs.columns.str.strip().str.title()

current_dogs["Status"] = "Available"
adopted_dogs["Status"] = "Adopted"

df = pd.concat(
    [current_dogs, adopted_dogs],
    ignore_index=True,
    sort=False
)
print(df.columns)


# In[68]:


#Column cleanup
df.drop(columns=["Column 1","Column 2","Column 3","Column 4","[Document Studio] Share Status #M4D6Cc6P","Response Edit Url","Response Id"], errors="ignore", inplace=True)

df["Timestamp"] = pd.to_datetime(
    df["Timestamp"],
    errors="coerce"
)
print(df.head())


# In[47]:


#Normalize capitalization
df["Intake From"] = (
    df["Intake From"]
    .str.strip()
    .str.title()
)


# In[48]:


#Create map for intake locations
intake_map = {
    "Bell": "Bell County",
    "Bell County": "Bell County",
    "Bell county": "Bell County",

    "Knox": "Knox County",
    "Knox County": "Knox County",

    "Lancaster": "Garrard County",
    "Eva": "Owner Surrender",

    "Rescue": "Transfer From Rescue",
    "Surrender": "Owner Surrender",
    "Stray": "Stray"
}

df["Intake From"] = df["Intake From"].replace(intake_map)


# In[49]:


#Convert weights to numbers
df["Weight"] = (
    df["Weight"]
    .astype(str)
    .str.lower()
    .str.replace("lbs", "", regex=False)
    .str.replace("unknown", "", regex=False)
    .str.replace("?", "", regex=False)
)

df["Weight"] = pd.to_numeric(
    df["Weight"],
    errors="coerce"
)


# In[50]:


#Map dog friendly values
dog_map = {
    "Yes": "Yes",
    "No": "No",
    "Unsure": "Unknown",
    "Selective": "Selective"
}

df["Dog Friendly"] = (
    df["Dog Friendly"]
    .str.title()
    .replace(dog_map)
)


# In[51]:


#Map kid friendly values
kid_map = {
    "Yes": "Yes",
    "No": "No",
    "Unsure": "Unknown"
}

df["Kid Friendly"] = (
    df["Kid Friendly"]
    .str.title()
    .replace(kid_map)
)


# In[72]:


#standardize color entries
import re

def clean_color(color):
    if pd.isna(color):
        return "Unknown"

    color = str(color).strip().lower()

    # fix typos
    color = color.replace("whtie", "white")
    color = color.replace("grey", "gray")

    # normalize separators
    color = re.sub(r"\s*/\s*", ",", color)
    color = re.sub(r"\s+and\s+", ",", color)
    color = re.sub(r"\s*,\s*", ",", color)

    # handle values like "black white" or "tan white"
    color = re.sub(r"\s+", ",", color)

    parts = [p.strip().title() for p in color.split(",") if p.strip()]

    # remove duplicates
    parts = sorted(set(parts))

    if len(parts) >= 3:
        return "Tricolor"

    if len(parts) == 0:
        return "Unknown"

    return " And ".join(parts)

df["Color"] = df["Color"].apply(clean_color)


# In[63]:


#Create color categories
def color_category(color):
    if pd.isna(color):
        return "Unknown"
    elif color == "Tricolor":
        return "Tricolor"
    elif "Brindle" in color:
        return "Brindle"
    elif "Black" in color:
        return "Black"
    elif "Brown" in color:
        return "Brown"
    elif "Tan" in color:
        return "Tan"
    elif "White" in color:
        return "White"
    elif "Gray" in color:
        return "Gray"
    elif "Blue" in color:
        return "Blue"
    else:
        return color

df["Color Category"] = df["Color"].apply(color_category)


# In[64]:


#standardize age values
import re

def clean_age(age):
    if pd.isna(age):
        return None

    age = str(age).strip().lower()

    # Handle ranges like "4-5"
    if "-" in age:
        nums = re.findall(r"\d+", age)
        if len(nums) == 2:
            return (float(nums[0]) + float(nums[1])) / 2

    # Handle months
    if "month" in age:
        nums = re.findall(r"\d+", age)
        if nums:
            return round(float(nums[0]) / 12, 2)

    # Handle years
    if "year" in age:
        nums = re.findall(r"\d+", age)
        if nums:
            return float(nums[0])

    # Plain numbers
    try:
        return float(age)
    except:
        return None

df["Age"] = df["Age"].apply(clean_age)


# In[65]:


#Clean and categorize breeds
df["Breed"] = (
    df["Breed"]
    .str.strip()
    .str.lower()
)

breed_map = {
    "pit mix": "Pit Mix",
    "pit mix ": "Pit Mix",
    "pit bull terrier": "Pit Bull Terrier",
    "pit/boxer mix": "Pit Boxer Mix",
    "stafford terrier mix": "Staffordshire Terrier Mix",
    "bully mix": "Bully Mix",
    "mix breed": "Mixed Breed",
    "bird dog": "Bird Dog",
    "beagle mix": "Beagle Mix",
    "boxer mix": "Boxer Mix",
    "border collie": "Border Collie",
    "border collie mix": "Border Collie Mix",
    "collie mix": "Collie Mix",
    "hound mix": "Hound Mix",
    "shepherd mix": "Shepherd Mix",
    "anatolian mix": "Anatolian Mix",
    "australian shepherd pit mix": "Australian Shepherd Pit Mix"
}

df["Breed"] = (
    df["Breed"]
    .replace(breed_map)
    .str.title()
)

def primary_breed(breed):
    if pd.isna(breed):
        return "Unknown"

    breed = breed.lower()

    if "pit" in breed:
        return "Pit Bull"
    elif "border collie" in breed:
        return "Border Collie"
    elif "collie" in breed:
        return "Collie"
    elif "shepherd" in breed:
        return "Shepherd"
    elif "anatolian" in breed:
        return "Anatolian"
    elif "hound" in breed:
        return "Hound"
    elif "boxer" in breed:
        return "Boxer"
    elif "beagle" in breed:
        return "Beagle"
    elif "bully" in breed:
        return "Bully"
    elif "bird dog" in breed:
        return "Bird Dog"
    else:
        return "Other"

df["Primary Breed"] = df["Breed"].apply(primary_breed)

breed_group_map = {
    "Pit Bull": "Terrier",
    "Bully": "Terrier",
    "Boxer": "Working",
    "Shepherd": "Herding",
    "Border Collie": "Herding",
    "Collie": "Herding",
    "Anatolian": "Working",
    "Hound": "Hound",
    "Beagle": "Hound",
    "Bird Dog": "Sporting",
    "Other": "Other"
}

df["Breed Group"] = (
    df["Primary Breed"]
    .map(breed_group_map)
)


# In[56]:


#Clean names
df["Name"] = (
    df["Name"]
    .str.strip()
    .str.title()
)


# In[66]:


#Clean Intake To values
df["Intake To"] = (
    df["Intake To"]
    .astype(str)
    .str.strip()
    .str.title()
)

intake_to_map = {
    "Barn": "Barn",
    "Foster Ky": "Foster KY",
    "Foster Ny": "Foster NY",
    "Foster": "Foster",
    "Boarding/Vet": "Boarding/Vet",

    "Adopted": "Adopted",
    "Aopted": "Adopted"
}

df["Intake To"] = df["Intake To"].replace(intake_to_map)

def intake_to_category(value):
    if pd.isna(value):
        return "Unknown"

    value = value.strip().lower()

    if "foster" in value:
        return "Foster"
    elif "adopted" in value or value == "aopted":
        return "Adopted"
    elif "barn" in value:
        return "Barn"
    elif "boarding" in value or "vet" in value:
        return "Boarding/Vet"
    else:
        return "Other"

df["Intake To Category"] = df["Intake To"].apply(intake_to_category)


# In[73]:


#Calculate tenure for unadopted dogs
import numpy as np

today = pd.Timestamp.today()

# Create as a float column with missing values
df["Days In Rescue"] = np.nan

mask = df["Status"] == "Available"

df.loc[mask, "Days In Rescue"] = (
    today - df.loc[mask, "Timestamp"]
).dt.days.astype(float)


# In[74]:


#Create intake month column
df["Intake Month"] = df["Timestamp"].dt.to_period("M").astype(str)


# In[75]:


#Create age group column
def age_group(age):
    if pd.isna(age):
        return "Unknown"
    elif age < 1:
        return "Puppy"
    elif age < 3:
        return "Young Adult"
    elif age < 8:
        return "Adult"
    else:
        return "Senior"

df["Age Group"] = df["Age"].apply(age_group)


# In[77]:


#Create weight group column
def weight_group(weight):
    if pd.isna(weight):
        return "Unknown"
    elif weight < 25:
        return "Small"
    elif weight < 50:
        return "Medium"
    elif weight < 75:
        return "Large"
    else:
        return "XL"

df["Weight Group"] = df["Weight"].apply(weight_group)


# In[78]:


#Create intake source type column
def intake_source_type(source):
    source = str(source).lower()

    if "county" in source:
        return "County Shelter"
    elif "surrender" in source:
        return "Owner Surrender"
    elif "stray" in source:
        return "Stray"
    elif "rescue" in source:
        return "Rescue Transfer"
    elif "vet" in source:
        return "Veterinary"
    else:
        return "Other"

df["Intake Source Type"] = df["Intake From"].apply(intake_source_type)


# In[80]:


#Create data completeness scores
important_cols = [
    "Breed",
    "Age",
    "Weight",
    "Color",
    "Sex",
    "Petfinder Link"
]

df["Data Completeness %"] = (
    df[important_cols]
    .notna()
    .mean(axis=1)
    * 100
)


# In[82]:


#Create LOS bucket column
def los_bucket(days):
    if pd.isna(days):
        return "Historical"
    elif days <= 30:
        return "0–30 Days"
    elif days <= 90:
        return "31–90 Days"
    elif days <= 180:
        return "91–180 Days"
    else:
        return "180+ Days"

df["LOS Bucket"] = df["Days In Rescue"].apply(los_bucket)


# In[83]:


#Create Unique Dog IDs
df = df.reset_index(drop=True)

df["Dog ID"] = "DOG-" + (df.index + 1).astype(str).str.zfill(4)


# In[86]:


df.to_csv("cleaned_rescue_data.csv", index=False)

print("Export complete!")
print(f"{len(df)} records exported.")

