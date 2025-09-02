import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import re
import json

# Page configuration
st.set_page_config(
    page_title="AI Data Catalog - Sample Data",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state variables
if 'catalog_generated' not in st.session_state:
    st.session_state.catalog_generated = False
if 'tables_info' not in st.session_state:
    st.session_state.tables_info = {}

# App title and description
st.title("🤖 AI-Powered Data Catalog Assistant")
st.markdown("""
This tool demonstrates an AI-powered data catalog using generated sample data. 
You can explore all features without needing a real database connection.
""")

# Sidebar for configuration
with st.sidebar:
    st.header("Sample Data Options")
    
    num_tables = st.slider("Number of sample tables", 1, 5, 3)
    table_size = st.slider("Rows per table", 100, 2000, 500)
    
    st.divider()
    
    st.header("OpenAI Configuration (Optional)")
    openai_key = st.text_input("OpenAI API Key", type="password")
    st.caption("Required for AI-generated descriptions. Leave empty to use placeholder text.")
    
    st.divider()
    
    st.header("Analysis Options")
    pii_detection = st.checkbox("Enable PII Detection", value=True)
    data_quality_checks = st.checkbox("Enable Data Quality Checks", value=True)

# Function to generate sample customer data
def generate_customer_data(rows):
    data = {
        'customer_id': range(1, rows + 1),
        'first_name': [random.choice(['John', 'Jane', 'Robert', 'Emily', 'Michael', 'Sarah', 'David', 'Lisa', 'James', 'Jennifer']) 
                       for _ in range(rows)],
        'last_name': [random.choice(['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez']) 
                      for _ in range(rows)],
        'email': [f"user{i}@example.com" for i in range(1, rows + 1)],
        'phone': [f"({random.randint(200, 999)})-{random.randint(200, 999)}-{random.randint(1000, 9999)}" for _ in range(rows)],
        'address': [f"{random.randint(100, 9999)} {random.choice(['Main', 'Oak', 'Maple', 'Cedar', 'Pine'])} St" for _ in range(rows)],
        'city': [random.choice(['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Philadelphia', 'San Antonio', 'San Diego', 'Dallas', 'San Jose']) 
                 for _ in range(rows)],
        'state': [random.choice(['CA', 'TX', 'FL', 'NY', 'PA', 'IL', 'OH', 'GA', 'NC', 'MI']) for _ in range(rows)],
        'zip_code': [str(random.randint(10000, 99999)) for _ in range(rows)],
        'join_date': [datetime.now() - timedelta(days=random.randint(1, 1000)) for _ in range(rows)],
        'status': [random.choice(['Active', 'Inactive', 'Pending']) for _ in range(rows)],
        'segment': [random.choice(['Premium', 'Standard', 'Basic']) for _ in range(rows)],
        'credit_score': [random.randint(300, 850) for _ in range(rows)]
    }
    
    # Introduce some missing values for realism
    for i in range(rows // 20):
        data['phone'][random.randint(0, rows-1)] = None
        data['address'][random.randint(0, rows-1)] = None
    
    return pd.DataFrame(data)

# Function to generate sample sales data
def generate_sales_data(rows):
    data = {
        'order_id': range(1000, 1000 + rows),
        'customer_id': [random.randint(1, 500) for _ in range(rows)],
        'product_id': [random.randint(1, 50) for _ in range(rows)],
        'order_date': [datetime.now() - timedelta(days=random.randint(1, 365)) for _ in range(rows)],
        'ship_date': [datetime.now() - timedelta(days=random.randint(1, 364)) for _ in range(rows)],
        'quantity': [random.randint(1, 10) for _ in range(rows)],
        'unit_price': [round(random.uniform(10, 500), 2) for _ in range(rows)],
        'discount': [round(random.uniform(0, 0.3), 2) for _ in range(rows)],
        'tax_amount': [round(random.uniform(1, 50), 2) for _ in range(rows)],
        'total_amount': [0] * rows,  # Will be calculated
        'payment_method': [random.choice(['Credit Card', 'PayPal', 'Bank Transfer', 'Cash']) for _ in range(rows)],
        'order_status': [random.choice(['Completed', 'Processing', 'Shipped', 'Cancelled']) for _ in range(rows)]
    }
    
    # Calculate total amount
    for i in range(rows):
        data['total_amount'][i] = round(
            data['quantity'][i] * data['unit_price'][i] * (1 - data['discount'][i]) + data['tax_amount'][i], 2
        )
    
    # Introduce some missing values for realism
    for i in range(rows // 25):
        data['ship_date'][random.randint(0, rows-1)] = None
        data['discount'][random.randint(0, rows-1)] = None
    
    return pd.DataFrame(data)

# Function to generate sample product data
def generate_product_data(rows):
    categories = ['Electronics', 'Clothing', 'Home & Kitchen', 'Books', 'Sports & Outdoors', 
                  'Beauty', 'Toys', 'Food', 'Health', 'Automotive']
    
    data = {
        'product_id': range(1, rows + 1),
        'product_name': [f"Product {chr(65 + i % 26)}{i}" for i in range(rows)],
        'category': [random.choice(categories) for _ in range(rows)],
        'subcategory': [f"Subcategory {random.randint(1, 5)}" for _ in range(rows)],
        'brand': [random.choice(['BrandA', 'BrandB', 'BrandC', 'BrandD', 'BrandE']) for _ in range(rows)],
        'supplier_id': [random.randint(1, 20) for _ in range(rows)],
        'cost_price': [round(random.uniform(5, 300), 2) for _ in range(rows)],
        'retail_price': [round(random.uniform(10, 500), 2) for _ in range(rows)],
        'weight': [round(random.uniform(0.1, 20), 2) for _ in range(rows)],
        'rating': [round(random.uniform(1, 5), 1) for _ in range(rows)],
        'stock_quantity': [random.randint(0, 1000) for _ in range(rows)],
        'is_active': [random.choice([True, False]) for _ in range(rows)],
        'date_added': [datetime.now() - timedelta(days=random.randint(1, 1000)) for _ in range(rows)]
    }
    
    # Introduce some missing values for realism
    for i in range(rows // 15):
        data['weight'][random.randint(0, rows-1)] = None
        data['rating'][random.randint(0, rows-1)] = None
    
    return pd.DataFrame(data)

# Function to detect PII in column names
def detect_pii(column_name):
    pii_patterns = {
        'email': r'email|e_mail|mail',
        'phone': r'phone|mobile|telephone|contact_number',
        'ssn': r'ssn|social_security|socialsecurity',
        'credit_card': r'creditcard|credit_card|cardnumber',
        'address': r'address|street|city|state|zipcode|postal',
        'name': r'name|firstname|lastname|fullname|username',
        'dob': r'dob|birthdate|date_of_birth',
        'user_id': r'userid|user_id|customerid|customer_id',
    }
    
    detected_pii = []
    for pii_type, pattern in pii_patterns.items():
        if re.search(pattern, column_name, re.IGNORECASE):
            detected_pii.append(pii_type)
    
    return detected_pii

# Function to generate AI description using OpenAI (or placeholder if no key)
def generate_ai_description(table_name, columns, sample_data, openai_key):
    if not openai_key:
        # Return a placeholder description if no API key is provided
        placeholder_descriptions = {
            'customers': "This table contains customer demographic and contact information. It serves as the master record for customer data and is used across marketing, sales, and customer service functions.",
            'sales': "This table records transactional data including orders, payments, and shipments. It is central to revenue reporting and analysis of business performance.",
            'products': "This table contains product information including pricing, categorization, and inventory data. It supports product management, pricing analysis, and inventory planning."
        }
        
        table_key = table_name.lower()
        for key in placeholder_descriptions:
            if key in table_key:
                return placeholder_descriptions[key]
        
        return f"This table appears to contain {table_name.replace('_', ' ')} data based on columns like {', '.join(columns[:3])}."
    
    # If we had a real OpenAI key, we would use the API here
    # For this sample, we'll just return a placeholder
    return f"AI-generated description for {table_name} would appear here with a valid OpenAI API key."

# Function to analyze data quality
def analyze_data_quality(df):
    quality_metrics = {}
    
    # Completeness
    completeness = (1 - df.isnull().sum() / len(df)) * 100
    quality_metrics['completeness'] = completeness.mean()
    
    # Uniqueness
    uniqueness = {}
    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]) or pd.api.types.is_object_dtype(df[col]):
            uniqueness[col] = df[col].nunique() / len(df) * 100
    if uniqueness:
        quality_metrics['uniqueness'] = sum(uniqueness.values()) / len(uniqueness)
    else:
        quality_metrics['uniqueness'] = 0
    
    # Consistency (basic check for value ranges)
    consistency_score = 0
    numeric_cols = df.select_dtypes(include=['number']).columns
    if len(numeric_cols) > 0:
        for col in numeric_cols:
            if df[col].max() > 0:  # Simple check for reasonable values
                consistency_score += 100
        quality_metrics['consistency'] = consistency_score / len(numeric_cols)
    else:
        quality_metrics['consistency'] = 0
    
    # Overall score (weighted average)
    overall_score = (
        quality_metrics['completeness'] * 0.4 +
        quality_metrics['uniqueness'] * 0.3 +
        quality_metrics['consistency'] * 0.3
    )
    
    quality_metrics['overall_score'] = overall_score
    
    return quality_metrics

# Generate sample data based on user selection
def generate_sample_data():
    tables = {}
    
    if num_tables >= 1:
        tables['customers'] = generate_customer_data(table_size)
    if num_tables >= 2:
        tables['sales'] = generate_sales_data(table_size)
    if num_tables >= 3:
        tables['products'] = generate_product_data(min(50, table_size))
    if num_tables >= 4:
        tables['employees'] = generate_customer_data(min(100, table_size)).rename(columns={'customer_id': 'employee_id'})
    if num_tables >= 5:
        tables['suppliers'] = generate_product_data(min(30, table_size)).rename(columns={'product_id': 'supplier_id'})
    
    return tables

# Button to generate the data catalog
if st.button("Generate Sample Data Catalog", type="primary"):
    with st.spinner("Generating sample data and analyzing..."):
        # Generate sample data
        sample_tables = generate_sample_data()
        
        # Analyze each table
        st.session_state.tables_info = {}
        
        for table_name, table_data in sample_tables.items():
            # Get column information
            column_names = table_data.columns.tolist()
            
            # Detect PII
            pii_columns = {}
            for col in column_names:
                pii_types = detect_pii(col)
                if pii_types:
                    pii_columns[col] = pii_types
            
            # Generate AI description
            ai_description = generate_ai_description(
                table_name, column_names, table_data.head(5), openai_key
            )
            
            # Analyze data quality if enabled
            quality_metrics = {}
            if data_quality_checks:
                quality_metrics = analyze_data_quality(table_data)
            
            # Store table information
            st.session_state.tables_info[table_name] = {
                'columns': column_names,
                'pii_columns': pii_columns,
                'ai_description': ai_description,
                'quality_metrics': quality_metrics,
                'sample_data': table_data
            }
        
        st.session_state.catalog_generated = True
        st.success("Data catalog generated successfully!")

# Display results if catalog has been generated
if st.session_state.catalog_generated and st.session_state.tables_info:
    st.header("📋 Data Catalog Results")
    
    for table_name, table_info in st.session_state.tables_info.items():
        with st.expander(f"Table: {table_name}", expanded=True):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.subheader("Columns")
                columns_df = pd.DataFrame({
                    'Column Name': table_info['columns'],
                    'PII Types': [', '.join(table_info['pii_columns'].get(col, [])) for col in table_info['columns']]
                })
                st.dataframe(columns_df, use_container_width=True)
                
                if table_info['ai_description']:
                    st.subheader("AI Description")
                    st.info(table_info['ai_description'])
            
            with col2:
                if table_info['quality_metrics']:
                    st.subheader("Data Quality Score")
                    overall_score = table_info['quality_metrics']['overall_score']
                    
                    # Display score with color coding
                    if overall_score >= 80:
                        score_color = "green"
                    elif overall_score >= 60:
                        score_color = "orange"
                    else:
                        score_color = "red"
                    
                    st.markdown(f"""
                    <div style="text-align: center;">
                        <h1 style="color: {score_color};">{overall_score:.1f}/100</h1>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Quality metrics
                    st.metric("Completeness", f"{table_info['quality_metrics']['completeness']:.1f}%")
                    st.metric("Uniqueness", f"{table_info['quality_metrics']['uniqueness']:.1f}%")
                    st.metric("Consistency", f"{table_info['quality_metrics']['consistency']:.1f}%")
                
                if table_info['pii_columns']:
                    st.subheader("PII Detection")
                    for col, pii_types in table_info['pii_columns'].items():
                        st.warning(f"**{col}**: {', '.join(pii_types)}")
            
            # Show sample data
            if table_info['sample_data'] is not None:
                st.subheader("Sample Data (First 10 Rows)")
                st.dataframe(table_info['sample_data'].head(10), use_container_width=True)
    
    # Export option
    st.divider()
    st.subheader("Export Catalog")
    
    # Convert to JSON for download
    catalog_json = json.dumps(st.session_state.tables_info, indent=2, default=str)
    
    st.download_button(
        label="Download Catalog as JSON",
        data=catalog_json,
        file_name=f"data_catalog_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
        mime="application/json"
    )
else:
    # Placeholder content before analysis
    st.info("Click the 'Generate Sample Data Catalog' button to create a demo data catalog")
    
    # Example output preview
    st.subheader("Example Output Preview")
    example_col1, example_col2, example_col3 = st.columns(3)
    
    with example_col1:
        st.markdown("**PII Detection**")
        st.warning("**email**: email")
        st.warning("**phone_number**: phone")
        st.warning("**first_name**: name")
    
    with example_col2:
        st.markdown("**Data Quality Score**")
        st.metric("Overall Score", "87.5/100")
        st.metric("Completeness", "92.3%")
        st.metric("Uniqueness", "85.1%")
        st.metric("Consistency", "83.7%")
    
    with example_col3:
        st.markdown("**AI Description**")
        st.info("The 'customer_data' table contains core information about our customers including contact details, demographic information, and account status. This table serves as the master record for customer information.")

# Add some explanation about the sample
st.divider()
st.subheader("About This Sample")
st.markdown("""
This demonstration generates realistic sample data to showcase the AI Data Catalog capabilities:

1. **Customers Table**: Contains customer demographic and contact information
2. **Sales Table**: Includes transactional data with order details and payments
3. **Products Table**: Holds product information, pricing, and inventory data

The application analyzes this data to:
- Detect potentially sensitive PII (Personally Identifiable Information)
- Generate descriptive summaries of each table
- Calculate data quality metrics (completeness, uniqueness, consistency)
- Provide a sample of the data for review

You can customize the amount of data generated and toggle different analysis features using the sidebar options.
""")