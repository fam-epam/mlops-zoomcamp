import sys
from batch import read_data, get_output_path

year = int(sys.argv[1])
month = int(sys.argv[2])

input_file = get_output_path(year, month)
df = read_data(input_file)

predictions_sum = float(f"{df['predicted_duration'].sum():.2f}")
print(f"{predictions_sum}")

assert predictions_sum == 36.28
