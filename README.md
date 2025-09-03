Asteriqx StarAX AI Data Catalog - Transforming Data Governance through Artificial Intelligence

A practical Streamlit application that demonstrates AI-enhanced data governance capabilities including automated data cataloging, PII detection, and data quality assessment.

📋 Overview
This Streamlit application provides a Minimum Viable Product (MVP) for AI-powered data governance. It allows you to either connect to real databases or generate sample data to demonstrate:
Automated Data Cataloging: Scan and document data assets
PII Detection: Identify sensitive personally identifiable information using pattern matching
Data Quality Assessment: Evaluate completeness, uniqueness, and consistency
AI-Powered Documentation: Generate descriptive metadata using OpenAI's API
Interactive Exploration: Browse and analyze data through an intuitive UI

✨ Features
🔍 Metadata Extraction: Analyzes database schemas and sample data
🛡️ PII Detection: Identifies sensitive data using regex patterns
📊 Data Quality Scoring: Provides metrics for completeness, uniqueness, and consistency
🤖 AI-Generated Descriptions: Creates natural language descriptions using OpenAI (optional)
📁 Multiple Database Support: Works with PostgreSQL, MySQL, SQLite, Snowflake, and BigQuery
🎲 Sample Data Generation: No database required for testing
📤 Export Functionality: Download catalog results as JSON
🎨 User-Friendly Interface: Clean, intuitive Streamlit UI
🚀 Quick Start

Prerequisites
Python 3.7+
pip (Python package manager)
Installation

Clone or download the application files:
data_catalog_app.py (main application file)

Install required dependencies:

bash
pip install streamlit pandas sqlalchemy openai
Run the application:

bash
streamlit run data_catalog_app.py

Using Sample Data (No Database Required)
The application includes a sample data mode that generates realistic demo data:
-Open the sidebar and adjust sample data options
-Click "Generate Sample Data Catalog"
-Explore all features without database connection

Connecting to a Real Database (Optional)
-In the sidebar, select your database type
-Enter connection details
-Provide an OpenAI API key for AI-generated descriptions (optional)
-Select tables to analyze
-Click "Generate Data Catalog"

🔧 Configuration
Database Connections
The application supports multiple database systems:

1 PostgreSQL: postgresql+psycopg2://user:password@host:port/database
2 MySQL: mysql+pymysql://user:password@host:port/database
3 SQLite: sqlite:///path/to/database.db
4 Snowflake: snowflake://user:password@host/database
5 BigQuery: bigquery://project/dataset

OpenAI Integration (Optional)
For AI-generated descriptions, provide an OpenAI API key in the sidebar. Without it, the app will use placeholder descriptions.

🧩 How It Works
Connection: 
-Establish connection to database or generate sample data
-Metadata Extraction: Scan table schemas and sample data
-PII Detection: Use regex patterns to identify sensitive information
-Quality Assessment: Calculate completeness, uniqueness, and consistency metrics
-AI Analysis: Generate descriptions using OpenAI's GPT model (if configured)
-Visualization: Display results in an interactive dashboard
-Export: Download catalog as JSON document

📊 Output Metrics
The application provides several data quality metrics:
-Completeness: Percentage of non-null values
-Uniqueness: Ratio of distinct values to total records
-Consistency: Measure of data conformity to expected patterns
-Overall Score: Weighted combination of all metrics

🛡️ PII Detection
The tool identifies several types of Personally Identifiable Information using pattern matching:
-Email addresses
-Phone numbers
-Social Security numbers
-Credit card information
-Physical addresses
-Personal names
-Dates of birth
-User identifiers

🎯 Use Cases
Data Discovery: Quickly understand unfamiliar databases
Compliance Preparation: Identify sensitive data for GDPR, CCPA, or other regulations
Data Quality Assessment: Evaluate the health of your data assets
Documentation: Automate initial data catalog creation
Demonstration: Showcase AI capabilities for data governance

📁 Project Structure
text
data_catalog_app.py          # Main Streamlit application
The application is self-contained in a single file for easy execution.

🔮 Potential Enhancements
This MVP could be extended with:
- Additional database connectors
- More sophisticated PII detection algorithms
- Historical tracking of data quality metrics
- Integration with existing data catalogs
- User authentication and authorization
- Scheduled scanning capabilities

🤝 Contributing
This is a demonstration application. Feel free to:
Fork the repository (if available)
Create a feature branch
Commit your changes
Push to the branch
Open a Pull Request

📝 License
This project is provided for demonstration purposes. Please ensure you have appropriate rights and licenses for any databases you connect to and for using OpenAI's API.

🙏 Acknowledgments
Built with Streamlit
Uses OpenAI API for optional AI features
Sample data generation for demonstration purposes

⚠️ Important Notes
This is an MVP demonstration tool, not a production system
Database credentials are handled in memory but not securely stored
For production use, additional security measures would be required
The PII detection uses pattern matching and may have false positives/negatives



