import csv
import os

from tool import init_path


class CSVWriter():
    def __init__(self, args, interval=1):
        self.args = args
        self.interval = interval
        self.log_name = self.get_output_path()
        self.prev_step = 0
        self.file_handle = open(self.log_name, 'w', newline='')
        self.fieldnames = None
        self.csv_writer = None

    def add(self, data, step=None):
        if self.fieldnames is None:
            self.fieldnames = sorted(data.keys())
        if self.csv_writer is None:
            self.csv_writer = csv.DictWriter(
                self.file_handle, fieldnames=self.fieldnames)
            self.csv_writer.writeheader()

        self.csv_writer.writerow(data)

        if step is not None and step > self.prev_step + self.interval:
            self.file_handle.close()
            self.file_handle = open(self.log_name, 'a', newline='')
            self.csv_writer = csv.DictWriter(
                self.file_handle, fieldnames=self.fieldnames)

        if step is not None:
            self.prev_step = step

    def close(self):
        self.file_handle.close()

    def get_output_path(self):
        if self.args.output_dir is None:
            path = init_path.get_base_dir()
            path = os.path.abspath(path)
        else:
            path = os.path.abspath(self.args.output_dir)
        base_path = os.path.join(path, 'csv_log')
        if not os.path.exists(base_path):
            os.makedirs(base_path)

        log_name = os.path.join(
            base_path, self.args.task + '_' + self.args.time_id + '.csv')
        return log_name
