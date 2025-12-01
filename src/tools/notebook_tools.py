import nbformat
import os

def read_notebook(path: str) -> str:
    """
    Reads a Jupyter Notebook and returns a string representation of the code cells.
    
    Args:
        path (str): The path to the .ipynb file.
        
    Returns:
        str: A string containing the code from the notebook cells.
    """
    try:
        with open(path, 'r', encoding='utf-8') as f:
            nb = nbformat.read(f, as_version=4)
            
        code_content = []
        for cell in nb.cells:
            if cell.cell_type == 'code':
                code_content.append(f"# Cell {len(code_content) + 1}\n{cell.source}\n")
                
        return "\n".join(code_content)
    except Exception as e:
        return f"Error reading notebook: {str(e)}"

def write_file(path: str, content: str):
    """
    Writes content to a file at the specified path.
    Creates directories if they don't exist.
    """
    try:
        # Ensure directory exists
        directory = os.path.dirname(path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
            
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"Successfully wrote to {path}"
    except Exception as e:
        return f"Error writing to {path}: {str(e)}"

def read_file(path: str):
    """
    Reads content from a file at the specified path.
    """
    try:
        if not os.path.exists(path):
            return f"Error: File not found at {path}"
            
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error reading {path}: {str(e)}"
