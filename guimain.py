
import customtkinter
import os
import matplotlib.pyplot as plt
from tkinter import filedialog, messagebox
import csv
from functions import GraphingFunctions, FailurePredictor, CSVDataHandler, GeneralFunctions


customtkinter.set_appearance_mode("light")
customtkinter.set_default_color_theme("blue")


class App(customtkinter.CTk): 
    def __init__(self, model_path, csv_file_path):  
        super().__init__()
        
        self.failure_prediction = FailurePredictor(model_path)
        self.csv_handling = CSVDataHandler(csv_file_path)
        self.general_functions = GeneralFunctions()
        self.csv_file_path = 'output.csv'
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        
        
        self.title("AdaptiveMFG")
        self.geometry(f"{1600}x{1200}")
        
        self.sidebar_frame = customtkinter.CTkFrame(self, width = 140, corner_radius = 0)
        self.sidebar_frame.grid(row =0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight = 1)
        
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="AdaptiveMFG", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        self.sidebar_button_1 = customtkinter.CTkButton(
            self.sidebar_frame, 
            text="Upload CSV Data of Machine", 
            command=self.general_functions.upload_and_save_csv
        )
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)

        
        self.sidebar_button_2 = customtkinter.CTkButton(
            self.sidebar_frame,
            text="Failure Prediction",
            command=self.display_predictions
        )
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        
        self.output_area = customtkinter.CTkTextbox(self, width=250, height=400)  # Adjust height as needed
        self.output_area.grid(row=1, column=1, padx=(20, 0), pady=(10, 0), sticky="nsew")
        
        self.prediction_textbox = customtkinter.CTkTextbox(self, width=250)
        self.prediction_textbox.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
        
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Dark", "Light", "System"],
                                                                       command=self.general_functions.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w") 
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.general_functions.change_appearance_mode_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))
        
        self.entry = customtkinter.CTkEntry(self, placeholder_text="Enter CSV data...")
        self.entry.grid(row=3, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")
        
        self.main_button_1 = customtkinter.CTkButton(
            master=self, 
            text="Append to CSV", 
            fg_color="transparent", 
            border_width=2, 
            text_color=("gray10", "#DCE4EE"), 
            command=self.append_to_csv
        )
        self.main_button_1.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")
        
        self.textbox = customtkinter.CTkTextbox(self, width=250)
        self.textbox.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
        
        self.tabview = customtkinter.CTkTabview(self, width=300)
        self.tabview.grid(row=0, column=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.tabview.add("CTkTabview")
        self.tabview.add("Tab 2")
        self.tabview.add("Tab 3")
        self.tabview.tab("CTkTabview").grid_columnconfigure(0, weight=1)  # Configure grid of individual tabs
        self.tabview.tab("Tab 2").grid_columnconfigure(0, weight=1)
        
        self.optionmenu_1 = customtkinter.CTkOptionMenu(self.tabview.tab("CTkTabview"), dynamic_resizing=False,
                                                        values=["Bar Graph", "Scatter Plot", "Line Graph"])
        self.optionmenu_1.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        self.graphing_functions = GraphingFunctions(option_menu=self.optionmenu_1)
        self.graphing_functions.option_menu = self.optionmenu_1  
        
        self.string_input_button = customtkinter.CTkButton(self.tabview.tab("CTkTabview"), text="Produce Visual",
                                                           command=self.graphing_functions.produce_visual)
        self.string_input_button.grid(row=1, column=0, padx=20, pady=(20, 10))
        
        self.sidebar_button_1.configure(state="enabled", text="Upload CSV Data of Machine")
        self.sidebar_button_2.configure(state="enabled", text="Failure Prediction")
        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_optionemenu.set("100%")
        self.optionmenu_1.set("Bar Graph")
        
        self.textbox.insert("0.0", "AdaptiveMFG Overview\n\n" + """
AdaptiveMFG focuses on revolutionizing manufacturing with cutting-edge predictive maintenance solutions. Our prototype app is designed to address unplanned equipment failures by leveraging machine learning and real-time data analysis.

Key Features:
- User-Friendly Interface: Simplified navigation.
- Real-Time Data Processing: Quick detection of anomalies.
- Predictive Analytics: Forecasts failures to enable proactive maintenance.
- Data Visualization: Insights through visual data trends.

Goals:
1. Minimize Downtime: Reduce unexpected failures and costs.
2. Enhance Maintenance Efficiency: Transition to proactive maintenance.
3. Leverage Machine Learning: Provide accurate failure predictions.

Our mission is to optimize manufacturing efficiency and reduce downtime through advanced technology.
"""
)
    def display_predictions(self):
        """Fetch predictions from the uploaded CSV file and display them in the prediction textbox and output area."""
        # Use the predict_failure_from_file method of FailurePredictor
        predictions_df = self.failure_prediction.predict_failure_from_file(self.csv_file_path)

        # Clear previous content and display the predictions
        self.prediction_textbox.delete("0.0", "end")  
        self.output_area.delete("0.0", "end")  # Clear previous content in output area

        result_text = predictions_df.to_string(index=False)  # Convert DataFrame to string
        self.prediction_textbox.insert("0.0", result_text)
        self.output_area.insert("0.0", "Predictions successfully fetched.\n" + result_text)  # Display in output area

        
    def append_to_csv(self):
        """Append entry data to CSV using CSVDataHandler."""
        entry_value = self.entry.get()
        if entry_value.strip():  # Check if the entry is not empty
            self.csv_handling.append_to_csv(entry_value)
        else:
            print("No input provided to append to CSV.")
    
    

    def predictFailure(output_area):
        # Step 1: Load the Voting Classifier model
        model_filename = 'voting_classifier_model.joblib'
        try:
            voted_clf = joblib.load(model_filename)
            output_area.insert('end', "Model loaded successfully.\n")
        except FileNotFoundError:
            output_area.insert('end', f"Model file '{model_filename}' not found.\n")
            return
        except Exception as e:
            output_area.insert('end', f"Error loading model: {e}\n")
            return

        # Step 2: Open a file dialog to select the test CSV file
        root = Tk()
        root.withdraw()  # Hide the root window
        test_data_file = filedialog.askopenfilename(
            title="Select Test Data CSV File",
            filetypes=[("CSV Files", "*.csv")]
        )
        
        if not test_data_file:
            output_area.insert('end', "No file selected.\n")
            return

        try:
            # Step 3: Load the test data from the selected CSV file
            test_data = pd.read_csv(test_data_file)
            output_area.insert('end', f"Test data loaded from {test_data_file}.\n")
        except FileNotFoundError:
            output_area.insert('end', f"File '{test_data_file}' not found.\n")
            return
        except Exception as e:
            output_area.insert('end', f"Error loading test data: {e}\n")
            return

        # Step 4: Validate that the test data matches the required format
        required_columns = [
            "Power", "Rotational speed rpm", "Torque Nm", "Rotational speed rpm_2",
            "Air temperature K", "Tool wear min", "Air temperature K_2", "tool_wear_speed"
        ]
        
        if list(test_data.columns) != required_columns:
            output_area.insert('end', "Test data format is incorrect. Please provide a CSV with the following columns:\n")
            output_area.insert('end', ", ".join(required_columns) + "\n")
            return

        # Step 5: Prepare the features for prediction
        x_test = test_data  # Use all columns as features

        # Step 6: Make predictions with the Voting Classifier
        try:
            voted_preds = voted_clf.predict(x_test)
            output_area.insert('end', "Predictions generated successfully.\n")
        except Exception as e:
            output_area.insert('end', f"Error during prediction: {e}\n")
            return

        # Step 7: Convert predictions to readable format
        predictions_readable = ['Failure' if pred == 1 else 'Not Failure' for pred in voted_preds]

        # Step 8: Create a DataFrame for the readable predictions with index
        predictions_df = pd.DataFrame(data=predictions_readable, columns=['Prediction'])
        predictions_df.reset_index(inplace=True)
        predictions_df.rename(columns={'index': 'Index'}, inplace=True)

        # Debug print to verify DataFrame before saving
        output_area.insert('end', "Data to be saved:\n")
        output_area.insert('end', str(predictions_df.head()) + "\n")

        # Step 9: Export the predictions to a new CSV file
        output_file_path = '/home/abhirama/AdaptiveMFG/predictions_output.csv'
        try:
            predictions_df.to_csv(output_file_path, index=False)
            output_area.insert('end', f"Predictions saved to '{output_file_path}'\n")
        except Exception as e:
            output_area.insert('end', f"Error saving predictions: {e}\n")




if __name__ == "__main__":
    model_path = 'voting_classifier_model.joblib'  # Set the correct model path
    csv_file_path = 'output.csv'
    app = App(model_path, csv_file_path)
    
    app.mainloop()    





