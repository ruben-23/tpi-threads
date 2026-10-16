import datetime
import pprint

def parse_timestamp(line):
    # Presupunem că timestamp-ul este la începutul liniei și are lungimea de 19 caractere
    timestamp_str = line[:19]
    dt = datetime.datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')
    return dt.timestamp()

def read_log_file(filename):
    entries = []
    with open(filename, 'r') as f:
        for line in f:
            timestamp = parse_timestamp(line)
            entries.append((timestamp, line))
    return entries


def merge_logs(entries1, entries2):
    combined_entries = entries1 + entries2
    pprint.pprint(combined_entries)
    combined_entries.sort(key=lambda x: x[0])  # Sortează după timestamp
    return combined_entries


def write_merged_log(entries, output_filename):
    with open(output_filename, 'w') as f:
        for entry in entries:
            f.write(entry[1])


def main():
    log_file1 = 'log1.txt'
    log_file2 = 'log2.txt'
    output_file = 'merged_log.txt'

    entries1 = read_log_file(log_file1)
    entries2 = read_log_file(log_file2)

    merged_entries = merge_logs(entries1, entries2)
    write_merged_log(merged_entries, output_file)

    print(f"Fișierele '{log_file1}' și '{log_file2}' au fost combinate în '{output_file}'.")

if __name__ == '__main__':
    main()

