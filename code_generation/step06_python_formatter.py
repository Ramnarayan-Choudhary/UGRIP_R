import subprocess
import re

class ScriptHelper:
    def __init__(self):
        pass

    def save_to_file(self, script_string, file_name):
        # Remove surrounding '''python ... ''' or ```python ... ```
        clean_script = re.sub(r"^'''python\s*|'''$", '', script_string.strip(), flags=re.DOTALL)
        clean_script = re.sub(r'^```python\s*|```$', '', clean_script.strip(), flags=re.MULTILINE)
        
        # Save the cleaned script to a file
        with open(file_name, 'w') as file:
            file.write(clean_script)

    def run_script(self, file_name):
        # Run the script using subprocess and collect the output
        result = subprocess.run(['python', file_name], capture_output=True, text=True)
        return result.stdout, result.stderr

# Example usage:
if __name__ == "__main__":
    helper = ScriptHelper()

    script_string = f'''```python
print("Hello, World!")
```'''
    file_name = "test_script.py"
    helper.save_to_file(script_string, file_name)
    
    stdout, stderr = helper.run_script(file_name)
    print("STDOUT:\n", stdout)
    print("STDERR:\n", stderr)

    # wrapped_script = f"Hers is your script:\n{script_string}\nGood luck!"
    # print("Wrapped Script:\n", wrapped_script)
