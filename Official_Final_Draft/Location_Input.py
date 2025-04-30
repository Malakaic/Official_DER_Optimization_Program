import csv
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import requests
import config


class Location(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

    def create_location_section(self, frame):
        """Creates a location section for data inputs."""
        location_frame = ttk.LabelFrame(frame, text="Location")
        location_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        # Toggle between "City, State, Country" and "Latitude, Longitude"
        self.input_mode = tk.StringVar(value="address")  # Default to "address" mode

        mode_frame = ttk.Frame(location_frame)
        mode_frame.grid(row=0, column=0, columnspan=4, pady=5)
        ttk.Radiobutton(mode_frame, text="City, State, Country", variable=self.input_mode, value="address", command=self.update_input_mode).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(mode_frame, text="Latitude, Longitude", variable=self.input_mode, value="coordinates", command=self.update_input_mode).pack(side=tk.LEFT, padx=5)

        # Address input fields
        self.address_frame = ttk.Frame(location_frame)
        self.address_frame.grid(row=1, column=0, columnspan=4, sticky="nsew", pady=5)

        tk.Label(self.address_frame, text="City:").grid(row=0, column=0, padx=5)
        self.city_entry = tk.Entry(self.address_frame)
        self.city_entry.grid(row=0, column=1, padx=5)

        tk.Label(self.address_frame, text="State:").grid(row=0, column=2, padx=5)
        self.state_entry = tk.Entry(self.address_frame)
        self.state_entry.grid(row=0, column=3, padx=5)

        tk.Label(self.address_frame, text="Country:").grid(row=1, column=0, padx=5)
        self.country_entry = tk.Entry(self.address_frame)
        self.country_entry.grid(row=1, column=1, padx=5)

        # Coordinates input fields
        self.coordinates_frame = ttk.Frame(location_frame)
        self.coordinates_frame.grid(row=2, column=0, columnspan=4, sticky="nsew", pady=5)
        self.coordinates_frame.grid_remove()  # Hide by default

        tk.Label(self.coordinates_frame, text="Latitude:").grid(row=0, column=0, padx=5)
        self.latitude_entry = tk.Entry(self.coordinates_frame)
        self.latitude_entry.grid(row=0, column=1, padx=5)

        tk.Label(self.coordinates_frame, text="Longitude:").grid(row=0, column=2, padx=5)
        self.longitude_entry = tk.Entry(self.coordinates_frame)
        self.longitude_entry.grid(row=0, column=3, padx=5)

        # Ensure the frame expands properly
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        location_frame.grid_rowconfigure(0, weight=1)
        location_frame.grid_rowconfigure(1, weight=1)
        location_frame.grid_rowconfigure(2, weight=1)

    def update_input_mode(self):
        """Update the input fields based on the selected mode."""
        if self.input_mode.get() == "address":
            self.address_frame.grid()
            self.coordinates_frame.grid_remove()
        elif self.input_mode.get() == "coordinates":
            self.coordinates_frame.grid()
            self.address_frame.grid_remove()

