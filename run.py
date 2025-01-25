import multiprocessing
import subprocess
import sys
import os
import time

def run_backend():
    """Run the FastAPI backend server."""
    subprocess.run([sys.executable, "backend.py"])

def run_frontend():
    """Run the Streamlit frontend."""
    time.sleep(2)  # Small delay to ensure backend is up
    subprocess.run([sys.executable, "-m", "streamlit", "run", "frontend.py"])

def main():
    # Ensure we're in the correct directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)

    # Create multiprocessing processes
    backend_process = multiprocessing.Process(target=run_backend)
    frontend_process = multiprocessing.Process(target=run_frontend)

    try:
        # Start both processes
        backend_process.start()
        frontend_process.start()

        # Wait for processes to complete
        frontend_process.join()
    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        # Terminate any remaining processes
        backend_process.terminate()
        frontend_process.terminate()

if __name__ == "__main__":
    main()

# #second script
# import multiprocessing
# import subprocess
# import sys
# import os
# import time
# import requests

# def run_backend():
#     """Run the FastAPI backend server."""
#     try:
#         subprocess.run([sys.executable, "backend.py"])
#     except Exception as e:
#         print(f"Backend encountered an error: {e}")

# def run_frontend():
#     """Run the Streamlit frontend."""
#     # Wait for backend to start
#     for _ in range(10):  # Retry for ~10 seconds
#         try:
#             response = requests.get("http://127.0.0.1:8000")  # Assuming backend runs on 8000
#             if response.status_code == 200:
#                 break
#         except requests.ConnectionError:
#             time.sleep(1)  # Wait 1 second before retrying
#     else:
#         print("Backend did not start in time.")
#         return

#     try:
#         subprocess.run([sys.executable, "-m", "streamlit", "run", "frontend.py"])
#     except Exception as e:
#         print(f"Frontend encountered an error: {e}")

# def main():
#     script_dir = os.path.dirname(os.path.abspath(__file__))
#     os.chdir(script_dir)

#     backend_process = multiprocessing.Process(target=run_backend)
#     frontend_process = multiprocessing.Process(target=run_frontend)

#     try:
#         backend_process.start()
#         frontend_process.start()

#         frontend_process.join()
#     except KeyboardInterrupt:
#         print("\nShutting down...")
#     finally:
#         backend_process.terminate()
#         backend_process.join()  # Ensure cleanup
#         frontend_process.terminate()
#         frontend_process.join()  # Ensure cleanup

# if __name__ == "__main__":
#     main()



# import streamlit as st
# import pandas as pd
# import json

# # def json_to_dataframe(json_data):
# #     """
# #     Converts JSON data to a pandas DataFrame.
    
# #     :param json_data: JSON data as a string or dictionary.
# #     :return: DataFrame representing the JSON data.
# #     """
# #     try:
# #         if isinstance(json_data, str):
# #             # Try parsing JSON string
# #             json_data = json.loads(json_data)
        
# #         # Handle different JSON input formats
# #         if isinstance(json_data, list):
# #             # List of dictionaries
# #             return pd.DataFrame(json_data)
# #         elif isinstance(json_data, dict):
# #             # Single dictionary or nested structure
# #             return pd.DataFrame([json_data])
# #         else:
# #             raise ValueError("Invalid JSON format. Must be a list of dictionaries or a single dictionary.")
    
# #     except json.JSONDecodeError as e:
# #         st.error(f"JSON Parsing Error: {e}")
# #         return None

# def json_to_dataframe(json_data):
#     """
#     Converts the JSON data for leave management into a single pandas DataFrame.

#     :param json_data: JSON data as a string or dictionary.
#     :return: A pandas DataFrame with all modules, use cases, and sub-use cases flattened.
#     """
#     try:
#         if isinstance(json_data, str):
#             # Parse JSON string into dictionary
#             json_data = json.loads(json_data)

#         # Initialize an empty list to collect flattened data
#         flattened_data = []

#         # Extract module-level information
#         module_id = json_data.get("moduleId", "")
#         module_name = json_data.get("moduleName", "")

#         # Process use cases
#         for use_case in json_data.get("useCases", []):
#             use_case_id = use_case.get("useCaseId", "")
#             use_case_name = use_case.get("useCaseName", "")

#             # Process sub-use cases
#             for sub_use_case in use_case.get("subUseCases", []):
#                 sub_use_case_id = sub_use_case.get("subUseCaseId", "")
#                 sub_use_case_name = sub_use_case.get("subUseCaseName", "")
#                 description = sub_use_case.get("description", "")
#                 preconditions = " | ".join(sub_use_case.get("preconditions", []))
#                 postconditions = " | ".join(sub_use_case.get("postconditions", []))

#                 # Add a row of data for the sub-use case
#                 flattened_data.append({
#                     "Module ID": module_id,
#                     "Module Name": module_name,
#                     "Use Case ID": use_case_id,
#                     "Use Case Name": use_case_name,
#                     "Sub-Use Case ID": sub_use_case_id,
#                     "Sub-Use Case Name": sub_use_case_name,
#                     "Description": description,
#                     "Preconditions": preconditions,
#                     "Postconditions": postconditions,
#                 })

#         # Convert the collected data into a DataFrame
#         return pd.DataFrame(flattened_data)

#     except json.JSONDecodeError as e:
#         raise ValueError(f"JSON Parsing Error: {e}") from e
#     except Exception as e:
#         raise ValueError(f"An error occurred while processing the JSON: {e}") from e



# # df = json_to_dataframe(json_data)
# # df



# def to_lowercase(row):
#     """
#     Converts all string values in the row to lowercase.
#     """
#     return {key: (value.lower() if isinstance(value, str) else value) for key, value in row.items()}

# def expand_row(row):
#     """
#     Expand the selected row into a more detailed format.
#     You can customize this function based on your specific expansion needs.
#     """
#     expanded_content = json.dumps(row, indent=2)
    
#     # Save to a file
#     timestamp = pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")
#     filename = f"expanded_row_{timestamp}.json"
    
#     with open(filename, 'w') as f:
#         f.write(expanded_content)
    
#     return expanded_content, filename

# def main():
#     st.title("📊 JSON to Interactive DataFrame Editor")
    
#     # Initialize session state
#     if 'df' not in st.session_state:
#         st.session_state.df = None
#     if 'selected_row_index' not in st.session_state:
#         st.session_state.selected_row_index = None
    
#     # Sidebar for JSON Input
#     with st.sidebar:
#         st.header("JSON Data Input")
#         json_input = st.text_area("Enter JSON String:", 
#                                   height=200, 
#                                   placeholder="Paste your JSON here...")
    
#     # Convert JSON to DataFrame
#     if json_input:
#         try:
#             # Convert JSON to DataFrame
#             df = json_to_dataframe(json_input)
            
#             if df is not None:
#                 # Store DataFrame in session state
#                 st.session_state.df = df
#         except Exception as e:
#             st.error(f"Error processing JSON: {e}")
    
#     # Main Content Area
#     if st.session_state.df is not None:
#         df = st.session_state.df
        
#         # Add New Column Section
#         st.header("Add New Column")
#         new_column_name = st.text_input("Enter New Column Name")
        
#         if st.button("Add Column"):
#             if new_column_name and new_column_name not in df.columns:
#                 # Add the new column with empty values
#                 df[new_column_name] = ""
#                 st.success(f"Column '{new_column_name}' added successfully!")
#             elif new_column_name in df.columns:
#                 st.warning(f"Column '{new_column_name}' already exists!")
        
#         # Display Editable Table
#         st.header("📝 Editable DataFrame")
#         edited_df = st.data_editor(
#             df, 
#             num_rows="dynamic",  # Allow dynamic row addition
#             use_container_width=True,
#             key="data_editor"
#         )
        
#         # Update session state with any edits
#         if not edited_df.equals(df):
#             st.session_state.df = edited_df
        
#         # Row Selection
#         st.header("Select Row to Expand")
#         row_indices = list(edited_df.index)
#         selected_index = st.selectbox("Select Row Index:", options=row_indices)
        
#         # Store selected row index in session state
#         st.session_state.selected_row_index = selected_index
        
#         # Expand Row Button
#         if st.button("Expand Selected Row"):
#             try:
#                 # Get the selected row data
#                 selected_row = edited_df.loc[selected_index].to_dict()
                
#                 # Transform and expand the row
#                 transformed_row = to_lowercase(selected_row)
#                 expanded_content, filename = expand_row(transformed_row)
                
#                 # Display Expanded Row
#                 st.text_area(
#                     "Expanded Row JSON:", 
#                     value=expanded_content, 
#                     height=200
#                 )
                
#                 # Show filename where row was saved
#                 st.success(f"Row saved to {filename}")
            
#             except Exception as e:
#                 st.error(f"Error expanding row: {e}")
        
#         # Download CSV Button
#         st.header("Export Data")
#         csv = df.to_csv(index=False)
#         st.download_button(
#             label="Download CSV 📥",
#             data=csv,
#             file_name="updated_table.csv",
#             mime="text/csv"
#         )
        
#         # Export updated DataFrame as JSON String
#         json_output = df.to_json(orient="records", lines=False)
        
#         # Show JSON String on the interface
#         st.header("Exported JSON String")
#         st.text_area("Here is the updated JSON:", value=json_output, height=200)
        
#         # Download JSON Button
#         st.download_button(
#             label="Download JSON 📥",
#             data=json_output,
#             file_name="updated_table.json",
#             mime="application/json"
#         )
    
#     else:
#         # Welcome/Instruction Message
#         st.markdown("""        
#         ### 🚀 JSON to DataFrame Converter
        
#         **Instructions:**
#         1. Paste your JSON data in the sidebar
#         2. JSON can be:
#            - A list of dictionaries
#            - A single dictionary
#         3. Edit the table directly
#         4. Add columns or rows as needed
#         5. Download your updated CSV or JSON
        
#         **Example JSON:**
#         ```json
#         [
#             {"name": "Alice", "age": 30, "city": "New York"},
#             {"name": "Bob", "age": 25, "city": "San Francisco"}
#         ]
#         ```
#         """)

# if __name__ == "__main__":
#     main()



