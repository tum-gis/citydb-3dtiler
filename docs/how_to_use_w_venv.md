# How to use citydb-3dtiler independently?

If you are familiar with common Python application workflows, you can use the following instructions to run the software independently.

## Running Software using Virtual Environment (VEnv)

- [ ] Download the latest release or the main branch in the github repository.

- [ ] Create a Virtual Environment using following command:

=== "on Windows"
    ```powershell
    python -m venv env
    ```

=== "on Unix-based Systems"
    ```bash
    python3 -m venv env
    ```


- [ ] Activate the virtual environment (venv) using following command:

=== "on Windows"
    ```powershell
    .\env\Scripts\Activate
    ```

=== "on Unix-based Systems"
    ```bash
    source env/bin/activate
    ```

- [ ] Ensure that the PIP package is updated (optional).

=== "on Windows"
    ```powershell
    python -m pip install --upgrade pip
    ```

=== "on Unix-based Systems"
    ```bash
    python3 -m pip install --upgrade pip
    ```

- [ ] Install the dependent libraries:

=== "on Windows"
    ```powershell
    pip install -r requirements.txt
    ```

=== "on Unix-based Systems"
    ```bash
    pip install -r requirements.txt
    ```

- [ ] Run the Application

=== "on Windows"
    ```powershell
    python citydb-3dtiler.py --help
    ```

=== "on Unix-based Systems"
    ```bash
    python3 citydb-3dtiler.py --help
    ```