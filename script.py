import json

def parse_log_entry(log_entry):
    # Split the log entry by spaces
    log_parts = log_entry.split()

    # Check if the log entry contains the required fields
    if len(log_parts) >= 12:
        log_data = {
            'ip': log_parts[0],      # Extract IP address from the first element
            'status': log_parts[8],  # Extract status code from the ninth element
            'user_agent': ' '.join(log_parts[11:]),  # Extract user agent from the remaining elements
            'date': log_parts[3][1:] + ' ' + log_parts[4][:-1]  # Extract date and time, removing brackets and colon
        }
        return log_data
    else:
        return None

def parse_apache_log(log_file):
    parsed_logs = []  # Store parsed log entries
    ip_counts = {}  # Track counts of response codes by IP
    first_request_dates = {}  # Track the first request date for each IP
    last_request_dates = {}  # Track the last request date for each IP
    user_agents = {}  # Track user agents for each IP

    with open(log_file, 'r') as file:
        logs = file.readlines()

    for log in logs:
        log_data = parse_log_entry(log)
        if log_data:
            parsed_logs.append(log_data)
            ip = log_data['ip']
            response_code = log_data['status']
            user_agent = log_data['user_agent']
            date = log_data['date']

            if ip in ip_counts:
                if response_code in ip_counts[ip]:
                    ip_counts[ip][response_code] += 1
                else:
                    ip_counts[ip][response_code] = 1
                    
                ip_counts[ip]['total_requests'] += 1
                last_request_dates[ip] = date
                if user_agent not in user_agents[ip]:
                    user_agents[ip].append(user_agent)
            else:
                # Initialize counts and other data for the IP address
                ip_counts[ip] = {response_code: 1, 'total_requests': 1}
                first_request_dates[ip] = date
                last_request_dates[ip] = date
                user_agents[ip] = [user_agent]
    return parsed_logs, ip_counts, first_request_dates, last_request_dates, user_agents

def save_json_file(data, file_path):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

log_file_path = 'fichiers/access.log'  # Path to the Apache log file
# Call the function to parse the log file
parsed_logs, ip_counts, first_request_dates, last_request_dates, user_agents = parse_apache_log(log_file_path)

ip_data = []
for ip, counts in ip_counts.items():
    # Create an IP address entry with the required information
    ip_entry = {
        'ip': ip,
        'counts': counts,
        'first_request_date': first_request_dates[ip],
        'last_request_date': last_request_dates[ip],
        'user_agents': user_agents[ip]
    }

    ip_data.append(ip_entry)

output_file_path = 'fichiers/output.json'  # Path to the output JSON file

# Save the data to a JSON file
save_json_file(ip_data, output_file_path)
