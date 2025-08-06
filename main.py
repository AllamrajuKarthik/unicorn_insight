import pandas as pd

# Loading the Dataset
print("Loading dataset")

try:
    data_path = "unicorn_insight_dataset.csv"  
    df = pd.read_csv(data_path)
    print("Dataset loaded successfully.\n")
except FileNotFoundError:
    print(f"Error: File not found at path: {data_path}")
    exit()
except Exception as e:
    print(f"Unexpected error occurred while loading dataset: {e}")
    exit()

# Necessary cleanup
print("Cleaning data")

if 'Unnamed: 0' in df.columns:
    df.rename(columns={'Unnamed: 0': 'S.No'}, inplace=True)

# Converting 'Valuation ($B)' to float, The output column will be 'Valuation ($B)' so this is to convert the data to fit and make sense into that column 
if 'Valuation ($B)' in df.columns:
    df['Valuation ($B)'] = df['Valuation ($B)'].str.replace('$', '', regex=False)
    df['Valuation ($B)'] = df['Valuation ($B)'].str.replace('B', '', regex=False)
    df['Valuation ($B)'] = pd.to_numeric(df['Valuation ($B)'], errors='coerce')
else:
    print("Warning: 'Valuation ($B)' column not found!")
    exit()

# If the Valuation of a company is Nan then it'll be removed
df = df.dropna(subset=['Valuation ($B)'])

print("Cleanup complete.\n")

# Grouping data by Industry - 1st parameter and then user shall make the decision of which Industry he wants to view 
print("Analyzing industry-wise valuation")

# Create a DataFrame showing industry and total valuation
industry_grouped = df.groupby('Industry')['Valuation ($B)'].sum().reset_index()

# Sort industries by total valuation descending
industry_grouped_sorted = industry_grouped.sort_values(by='Valuation ($B)', ascending=False)

# Print available industries with index
print("List of Industries by Total Valuation:\n")
for i, row in industry_grouped_sorted.iterrows():
    idx = industry_grouped_sorted.index.get_loc(i) + 1
    industry_name = row['Industry']
    total_valuation = row['Valuation ($B)']
    print(f"{idx}. {industry_name} — ${total_valuation:.2f}B")

# User will pick an industry he wants to view
industry_list = industry_grouped_sorted['Industry'].tolist()

while True:
    print("\nPlease enter the number of the industry you want to explore:")
    user_input = input("Your choice: ")

    try:
        selected_index = int(user_input)
        if 1 <= selected_index <= len(industry_list):
            selected_industry = industry_list[selected_index - 1]
            print(f"\nYou selected: {selected_industry}")
            break
        else:
            print("Invalid number. Please select a number from the list above.")
    except ValueError:
        print("Invalid input. Please enter a valid number.")

# Display top companies in that industry
print(f"\nFetching top companies in '{selected_industry}' industry\n")

industry_df = df[df['Industry'] == selected_industry]
industry_df_sorted = industry_df.sort_values(by='Valuation ($B)', ascending=False)

columns_to_display = ['S.No', 'Company', 'Valuation ($B)', 'Country', 'City', 'Select Investors']

# Check if these columns are all in the dataframe
columns_available = [col for col in columns_to_display if col in industry_df_sorted.columns]

print(industry_df_sorted[columns_available].to_string(index=False))

# Exporting the data we gathered from here to a csv file for power BI Dashboard
output_path = f"filtered_{selected_industry.replace(' ', '_')}_unicorns.csv"
industry_df_sorted.to_csv(output_path, index =False)
print("\n Filtered data exported")


# Disclaimer, just some print statements to say that this application just assists the user and to urge the user to check for all the terms and conditions and tell him to make decisions based on more comprehensive data. 
print("\n Disclaimer:")
print("Investment decisions should not be based solely on valuation figures.")
print("This tool is built to assist in identifying high-value companies across industries,")
print("but proper due diligence, financial research, and risk assessment are always recommended.")
