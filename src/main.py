import os
import importlib
import inspect
from datetime import datetime
from compiler import parse_solidity
from extract_functions import extract_functions_from_ast
from ExploitExecuter import ContractScanner
from ExploitExecuter import AfterDetectionRunner
import argparse

def main():
    # Command-line arguments
    parser = argparse.ArgumentParser(description="Check a Solidity smart contract for vulnerabilities")
    wtt = parser.add_mutually_exclusive_group(required=False) ## what to test. can't test directory and single file at same time
    parser.add_argument("-file", "-f", help="Creates output txt file", action="store_false")
    wtt.add_argument("-dir", "-directory", type=str, help="Set directory to be scanned")
    wtt.add_argument("-contract", "-c", type=str, help="Set contract to be scanned")
    parser.add_argument("-t", "-terminal", help="Don't print results to terminal", action="store_false")

    args = parser.parse_args()
    no_file_flag = True if args.file else False

    script_dir = os.path.dirname(os.path.realpath(__file__))
    
    # Define file path
    if args.contract:
        file_path = os.path.join(script_dir, args.contract)
    else:
        file_path = os.path.join(script_dir, "testContracts/reentrency.sol")

    # Prepare report file
    report_folder = os.path.join(script_dir, "reports")
    os.makedirs(report_folder, exist_ok=True)
    file_name = os.path.splitext(os.path.basename(file_path))[0]
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    report_path = os.path.join(report_folder, f"{file_name}_{timestamp}.txt")

    # Exploit folder path
    exploit_folder = os.path.join(script_dir, "exploits")





    # Find all files if directory should be checked
    combined_vulnerabilities = {}
    if args.dir:
        dir_name = os.path.join(script_dir, args.dir)

        if not os.path.isdir(dir_name):
            print(f"The directory {dir_name} does not exist.")
            return

        vulnerabilities = []
         # Dictionary to hold combined vulnerabilities
        all_files = []  # List to hold all found .sol files
        path = os.path.join(script_dir, dir_name)
        # Walk through the directory and all its subdirectories
        for root, dirs, filenames in os.walk(path):
            for filename in filenames:
                if filename.endswith(".sol"):
                    # Construct the full file path
                    file_location = os.path.join(root, filename)
                    print("Found file: " + file_location)

                    # Append the full file path to the list
                    all_files.append(file_location)

                    # Scan the file
                    scanner = ContractScanner(file_location, exploit_folder)
                    vuln = scanner.scan()

                    # Combine vulnerabilities by `function`
                    if vuln:
                        for item in vuln:
                            function_name = item['function']
                            if function_name not in combined_vulnerabilities:
                                combined_vulnerabilities[function_name] = {'function': function_name, 'issues': []}

                            combined_vulnerabilities[function_name]['issues'].extend(item['issues'])

        # Convert combined_vulnerabilities to a list format if needed
        vulnerabilities = list(combined_vulnerabilities.values())
    else:
        # If a single file is specified
        all_files = []
        all_files.append(file_path)
        scanner = ContractScanner(file_path, exploit_folder)
        vulnerabilities = scanner.scan()

    afterscan_scanner = AfterDetectionRunner(exploit_folder, vulnerabilities, all_files)
    afterscanresult = afterscan_scanner.run()
    for item in afterscanresult:
            function_name = item['function']
            if function_name not in combined_vulnerabilities:
                combined_vulnerabilities[function_name] = {'function': function_name, 'issues': []}
                combined_vulnerabilities[function_name]['issues'].extend(item['issues'])
    
    # Write vulnerabilities to the report file
    with open(report_path, "w") as report_file:
        if vulnerabilities:
            if args.t:
                report_file.write("Potential vulnerabilities detected:\n")
            priority_order = {"Critical": 0, "High": 1, "Normal": 2, "Low": 3, "Informational": 4, "Unknown": 5}

            grouped_vulnerabilities = {}
            for vuln in vulnerabilities:
                function_name = vuln['function']
                if function_name not in grouped_vulnerabilities:
                    grouped_vulnerabilities[function_name] = []
                grouped_vulnerabilities[function_name].extend(vuln['issues'])

            for function_name, issues in grouped_vulnerabilities.items():
                report_file.write(f"\nFunction: {function_name}\n")
                issues.sort(key=lambda issue: priority_order.get(issue.get("type", "Unknown"), 5))

                for issue in issues:
                    issue_type = issue.get("type", "Unknown")
                    report_file.write(f"  - [{issue_type}] {issue.get('description')}\n")

        else:
            report_file.write("No vulnerabilities detected.\n")

    # Print vulnerabilities to terminal
    if args.t:
        print("\033[0m Potential vulnerabilities detected:")
        if vulnerabilities:
            priority_order = {"Critical": 0, "High": 1, "Normal": 2, "Low": 3, "Informational": 4, "Unknown": 5}

            grouped_vulnerabilities = {}
            for vuln in vulnerabilities:
                function_name = vuln['function']
                if function_name not in grouped_vulnerabilities:
                    grouped_vulnerabilities[function_name] = []
                grouped_vulnerabilities[function_name].extend(vuln['issues'])

            for function_name, issues in grouped_vulnerabilities.items():
                print(f"\033[36m Function: {function_name}")
                issues.sort(key=lambda issue: priority_order.get(issue.get("type", "Unknown"), 5))

                for issue in issues:
                    issue_type = issue.get("type", "Unknown")
                    match issue_type:
                        case "Critical":
                            print(f"\033[35m  !!! {issue.get('description')}")
                        case "High":
                            print(f"\033[31m  !!  {issue.get('description')}")
                        case "Normal":
                            print(f"\033[33m  !   {issue.get('description')}")
                        case "Low":
                            print(f"\033[34m  *   {issue.get('description')}")
                        case "Informational":
                            print(f"\033[0m  -   {issue.get('description')}")
                        case _:
                            print(f"\033[0m      {issue.get('description')}")
        else:
            print("No vulnerabilities detected.")

    # Keep the report file if the -f flag is set
    if no_file_flag:
        try:
            os.remove(report_path)
        except Exception as e:
            print(f"Failed to delete report file: {e}")
    else:
        print(f"Scan completed. Results saved to {report_path}")


if __name__ == "__main__":
    main()
