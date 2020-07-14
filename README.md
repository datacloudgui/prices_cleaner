# prices_cleaner
Script to clean prices data obtained by scraping

NOTE: If you use this file alone (without the scraper and load stage), change the line 29 in the code to: df.to_csv('clean_'+filename).
This is required because this file is commonly used from a pipeline program.

# Required

A sample file is provided in this repository

You need to have one csv file to clean with the following columns:

- categoria: The category of the article scrapped.
- producto: The name of the product in category.
- dd_mm_yy: Date of the scraped data this column contain the price of the product in that day.
- link: Link to the product in the retail site.
- Image: Link to the product image in the retail site.

# Usage

Execute the file calling the .csv file and the date of the data:

```python
python3 prices_cleaner.py camaras_2020_07_05_articles.csv 05_07_20
```
# Process

The code execute the following actions:

- Import csv file as a pandas dataframe.
- Verify and delete NaN values.
- Add an unique ID based on link column.
- Drop duplicated values.
- Clean and convert the price column to a number.
- Save the clean file.

# Contributing

If you want any advice to this code fell free to fork and make a pull request.