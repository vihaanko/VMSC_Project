import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('Cleaned_Company_Visits.csv')

sectors = pd.concat([df['business_sector_1'], df['business_sector_2'].dropna()])

sector_counts = sectors.value_counts()

top_sectors = sector_counts.head(10)

plt.figure(figsize=(8, 8))
plt.pie(top_sectors, labels=top_sectors.index, autopct='%1.1f%%', startangle=140)
plt.title('Most Popular Company Sectors')
plt.axis('equal')
plt.tight_layout()
plt.show()
