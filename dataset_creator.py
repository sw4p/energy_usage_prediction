import csv
import os
import json

class Metadata:
	def __init__(self, file_name):
		self.file_name = file_name
		self.class_files = []


	def insert_label(self, class_file_name, class_label):
		file_dict = {
			"path": class_file_name,
			"category": "split",
			"label": { "type": "label", "label": class_label }
		}
		self.class_files.append(file_dict)

	def export(self):
		main_dict = {
				"version": 1,
				"files": self.class_files
			}
		json_object = json.dumps(main_dict, indent=4)

		with open(self.file_name, 'w') as outfile:
			outfile.write(json_object)




def parse_timestamp(timestamp):
	T_position = timestamp.find('T')
	plus_position = timestamp.find('+')
	date = timestamp[:T_position].replace(' ', '')
	time = timestamp[T_position+1:plus_position]
	day_light_saving = time[-4]
	return date, time, day_light_saving

# date, time, day_light_saving = parse_timestamp('2022-03-27T22:01:03+01:00')
# print('date - ' + date)
# print('time - ' + time)
# print('day_light_saving - ' + day_light_saving)

def format_time(time):
	formatted_time = time[:-3].replace(':', '')
	return formatted_time

# print(format_time(time))

def create_new_file(file_name_with_path):
	file = open(file_name_with_path, 'w')
	csv_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
	print("file created - " + file_name_with_path)
	return file, csv_writer

def close_file(file):
	if file.closed:
		return
	file.close()
	print("file closed - " + file.name)

def rename_file(prev_name, new_name):
	print("renaming " + prev_name + " to " + new_name)
	os.rename(prev_name, new_name)
	return



def main():
	path = 'electricity_dataset/'
	file_count = 0
	update_date_time = 1
	total_energy_day = 0.0
	label_time_stamp = "02:00:00"
	last_file_name = "no_file"
	class_labels = Metadata("metadata.json")

	with open("modified/Electricity_01_01_2022_copy.csv") as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		line_count = 0
		for row in csv_reader:
			date, time, day_light_saving = parse_timestamp(row[0])
			# Change time format to EI accepted format
			if update_date_time:
				row[0] = format_time(time)

			# Take decision based on timestamp
			if (time == "00:00:00"):
				file, csv_writer = create_new_file(path+date+'.csv')
				csv_writer.writerow(['timestamp', 'consumption(kWh)'])
				total_energy_day = 0.0
				# csv_writer.writerow(row)
				# line_count += 1
			# elif (last_file_name != "no_file") and (time == label_time_stamp):
				# new_file_name = path+row[1]+'.csv'
				# rename_file(last_file_name, new_file_name)
				# class_labels.insert_label(last_file_name, row[1])
			elif (time == "23:30:00"):
				csv_writer.writerow(row)
				line_count += 1
				file_count += 1
				total_energy_day += float(row[1])
				class_labels.insert_label(last_file_name, str(total_energy_day))

				# last_file_name = file.name
				close_file(file)
				continue

			csv_writer.writerow(row)
			total_energy_day += float(row[1])
			line_count += 1

		class_labels.export()
		print(f'Processed {line_count} lines.')
		print(f'Created {file_count} files.')

main()