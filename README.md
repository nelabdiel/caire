# CAIRE (Categorized AI Review Engine)

CAIRE is a web-based application designed to help you organize, cluster, and review AI use cases efficiently. By categorizing AI projects based on their descriptions and titles, CAIRE provides a comprehensive and user-friendly interface to explore and analyze similar projects.

## Features

- **CSV Upload**: Easily upload a CSV file containing your AI project data.
- **Project Categorization**: Automatically categorize projects based on their descriptions and titles using advanced clustering algorithms.
- **Levenshtein Similarity**: Identify and highlight projects with similar titles using the Levenshtein distance algorithm.
- **Dynamic Visualization**: View projects in a user-friendly interface, with font sizes indicating the size of the project clusters.
- **Detailed Project Insights**: Click on individual projects to see detailed descriptions and find related projects.

## Usage

### Step-by-Step Instructions

1. **Navigate to the landing page.**

   ![Landing Page](./static/Screenshot1.png)

2. **Upload your CSV file.**

   ![Upload CSV](./static/Screenshot2.png)

3. **Select the columns containing the project titles and descriptions.**

   ![Select Columns](./static/Screenshot3.png)

4. **View the categorized projects in the list.**

   ![Project List](./static/Screenshot4.png)

5. **Click on a project title to see its detailed description and view related projects.**

   ![Project Details](./static/Screenshot5.png)


Additional Details:
- To test it I used the raw data from the previous AI Inventory Use Case found in: https://github.com/thoppe/Federal-AI-inventory-analysis-2023

Pending:
- Adding environments
- Possibly containarizing it
- Adding other ways to cluster and find similarities
- Extending to excel files
