import pandas as pd
import joblib
import matplotlib.pyplot as plt
import customtkinter
import os
import shutil
import tkinter
from tkinter import filedialog, messagebox

class GraphingFunctions:
    def __init__(self, option_menu):
        self.option_menu = option_menu
        self.model_filename = 'voting_classifier_model.joblib'
        self.model = joblib.load(self.model_filename)

    def plot_bar_graph(self):
        data = {'A': 10, 'B': 15, 'C': 7}
        names = list(data.keys())
        values = list(data.values())

        plt.figure(figsize=(8, 5))
        plt.bar(names, values)
        plt.title('Bar Graph Example')
        plt.show()

    def plot_scatter_plot(self):
        x = [1, 2, 3, 4, 5]
        y = [5, 7, 8, 5, 3]

        plt.figure(figsize=(8, 5))
        plt.scatter(x, y)
        plt.title('Scatter Plot Example')
        plt.show()

    def plot_line_graph(self):
        x = [1, 2, 3, 4, 5]
        y = [2, 3, 5, 7, 11]

        plt.figure(figsize=(8, 5))
        plt.plot(x, y)
        plt.title('Line Graph Example')
        plt.show()

    def produce_visual(self):
        selected_option = self.option_menu.get()
        if selected_option == "Bar Graph":
            self.plot_bar_graph()
        elif selected_option == "Scatter Plot":
            self.plot_scatter_plot()
        elif selected_option == "Line Graph":
            self.plot_line_graph()
        else:
            print("Invalid option selected.")


    
import joblib
import pandas as pd

class FailurePredictor:
    def __init__(self, model_path):
        self.model_path = model_path
        self.model = self.load_model()

    def load_model(self):
        # Load the model using the model path specified in the initializer
        return joblib.load(self.model_path)

    def predict_failure_from_file(self, csv_file_path):
        # Load the CSV file with test data
        test_data = pd.read_csv(csv_file_path)

        # Use all columns as features (customize if necessary)
        x_test = test_data

        # Make predictions with the loaded model
        voted_preds = self.model.predict(x_test)

        # Convert predictions to readable format
        predictions_readable = ['Failure' if pred == 1 else 'Not Failure' for pred in voted_preds]

        # Create a DataFrame for the readable predictions
        predictions_df = pd.DataFrame(data=predictions_readable, columns=['Prediction'])
        predictions_df.index.name = 'Index'  # Optional: add an index name

        return predictions_df

    

    

import re
import csv
import tkinter.messagebox

# In CSVDataHandler (functions.py or wherever it is defined)
class CSVDataHandler:
    def __init__(self, csv_file_path):
        self.csv_file_path = csv_file_path

    def append_to_csv(self, entry_value):
        """Appends a CSV line to the file based on entry input."""
        try:
            # Process user input as CSV row
            user_input = entry_value.strip()
            if user_input:
                row = user_input.split(',')
                with open(self.csv_file_path, 'a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(row)
                print("Data appended successfully to CSV.")
            else:
                print("No input provided.")
        except Exception as e:
            print(f"Error appending to CSV: {e}")
            
    import os
from tkinter import filedialog, messagebox
import csv

class App(customtkinter.CTk):
    def __init__(self, model_path, csv_file_path):
        super().__init__()
        
        self.model_path = model_path
        self.csv_file_path = csv_file_path  # Always points to output.csv
        
        # UI setup
        self.sidebar_button_1 = customtkinter.CTkButton(
            self.sidebar_frame, 
            text="Upload CSV Data of Machine", 
            command=self.append_to_csv
        )
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        
    def file_to_csv(self):
        """Uploads and appends data from a selected CSV file to output.csv with format validation."""
        required_header = [
            "Power", "Rotational speed rpm", "Torque Nm", "Rotational speed rpm_2",
            "Air temperature K", "Tool wear min", "Air temperature K_2", "tool_wear_speed"
        ]
        
        try:
            # Open file dialog for selecting CSV file
            upload_csv_path = filedialog.askopenfilename(
                filetypes=[("CSV Files", "*.csv")],
                title="Select a CSV file to upload"
            )
            
            # Ensure a valid file is selected
            if upload_csv_path and os.path.isfile(upload_csv_path):
                print(f"Selected file: {upload_csv_path}")
                
                # Open the selected file and validate header
                with open(upload_csv_path, 'r') as upload_file:
                    reader = csv.reader(upload_file)
                    header = next(reader, None)
                    
                    if not header:
                        messagebox.showerror("Empty File", "The selected CSV file is empty.")
                        return
                    elif header != required_header:
                        messagebox.showerror(
                            "Invalid CSV Format",
                            "The CSV file header does not match the required format:\n" +
                            ", ".join(required_header)
                        )
                        return
                    
                    # Append rows if the header is valid
                    with open(self.csv_file_path, 'a', newline='') as output_file:
                        writer = csv.writer(output_file)
                        
                        # Write header only if output.csv is empty
                        output_file.seek(0, os.SEEK_END)
                        if output_file.tell() == 0:
                            writer.writerow(header)
                            print("Header written to output.csv")
                        
                        row_count = 0
                        for row in reader:
                            writer.writerow(row)
                            row_count += 1
                        
                        if row_count > 0:
                            print(f"{row_count} rows appended to output.csv from {upload_csv_path}.")
                            messagebox.showinfo("Success", f"{row_count} rows appended successfully from uploaded CSV file.")
                        else:
                            print("No data rows found to append.")
                            messagebox.showwarning("No Data", "The CSV file contains only the header, no data rows to append.")
                
                # Confirm file contents after writing
                with open(self.csv_file_path, 'r') as check_file:
                    print("\nContents of output.csv after writing:")
                    for line in check_file:
                        print(line.strip())
                    
            else:
                print("No valid file selected or file not found.")
                messagebox.showwarning("File Not Found", "Please select a valid CSV file.")
                
        except Exception as e:
            print(f"Error appending to CSV: {e}")
            messagebox.showerror("Error", f"An error occurred while appending to CSV: {e}")


class GeneralFunctions:
    def __init__(self):
        # Initialize any required attributes
        self.saved_csv_file_path = None  # To store the CSV file path for later use
        
        # Initialize the customtkinter appearance mode (optional default)
        customtkinter.set_appearance_mode("System")  # Default appearance mode
        customtkinter.set_widget_scaling(1.0)  # Default scaling

    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self):
        print("sidebar_button click")
        # Add logic to handle failure prediction here, if applicable.

    def upload_and_save_csv(self):
        # Open a file dialog to select a CSV file
        file_path = filedialog.askopenfilename(
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )

        if not file_path:
            return  # If no file was selected, exit the function

        # Define a directory to save the CSV file (user's home directory)
        save_directory = os.path.expanduser("~")

        # Create a new file path for saving
        filename = os.path.basename(file_path)
        new_file_path = os.path.join(save_directory, filename)

        try:
            # Copy the file to the new location
            shutil.copy(file_path, new_file_path)
            
            # Optionally display a message indicating success
            messagebox.showinfo("Success", f"File saved as {new_file_path}")

            # Call the function to predict failure based on the CSV data
            self.predict_failure_from_csv(new_file_path)

        except Exception as e:
            # Handle exceptions (e.g., file copy errors)
            messagebox.showerror("Error", f"An error occurred while saving the file: {e}")

        # Optionally save the new file path for later use
        self.saved_csv_file_path = new_file_path

    def predict_failure_from_csv(self, csv_file_path):
        # Placeholder function for future failure prediction logic
        print(f"Predicting failure from: {csv_file_path}")


# Usage
if __name__ == "__main__":
    model_filename = 'voting_classifier_model.joblib'
    test_data_file = '/home/abhirama/AdaptiveMFG/test.csv'  # Adjusted file path
    output_file_path = '/home/abhirama/AdaptiveMFG/predictions_output.csv'  # Specify the output path

    predictor = FailurePredictor(model_filename, test_data_file, output_file_path)
    predictor.predict()
