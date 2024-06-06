from grongier.pex import BusinessService

from iris_fhir.msg import PatientRequest, Patient

from dataclass_csv import DataclassReader

import csv
import os

class FhirCSVService(BusinessService):

    def on_init(self):
        if not hasattr(self, "path"):
            self.path = "/irisdev/app/misc/in"

    def get_adapter_type():
        # This is mandatory to schedule the service
        # By default, the service will be scheduled every 5 seconds
        return "Ens.InboundAdapter"

    def on_process_input(self, message_input):
        # check if a CSV file is present in /tmp/in/*
        # if yes, read it and send each line as a FormationRequest
        # if no, do nothing
        self.log_info("Processing input")

        # check if the directory exists
        if not os.path.exists(self.path):
            self.log_info("No input directory")
            return
        
        # check if the directory is empty
        if not os.listdir(self.path):
            self.log_info("Input directory is empty")
            return
        
        # check if the directory contains a CSV file
        csv_files = [f for f in os.listdir(self.path) if f.endswith(".csv")]
        if not csv_files:
            self.log_info("No CSV file in input directory")
            return
        
        # read the CSV file
        csv_file = csv_files[0]
        self.log_info(f"Reading {csv_file}")

        with open(os.path.join(self.path, csv_file), "r") as file:
            reader = DataclassReader(file, Patient, delimiter=";")
            for row in reader:
                self.send_request_sync(
                        "Python.CsvToFhir", 
                        PatientRequest(patient=row)
                    )


        # move the file to /tmp/in/processed
        os.rename(
            os.path.join(self.path, csv_file), 
            os.path.join(
                os.path.join('/irisdev/app/misc','out'), csv_file
                )
            )