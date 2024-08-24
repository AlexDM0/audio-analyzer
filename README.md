### Updated `README.md`:

```markdown
# Project Setup

## Prerequisites

Ensure you have Python 3.11 installed. You can download it from the [official Python website](https://www.python.org/downloads/).

## Setting Up the Virtual Environment

1. **Create a virtual environment**:
    ```sh
    python -m venv .venv
    ```

2. **Activate the virtual environment**:
    - On Windows:
        ```sh
        .venv\Scripts\activate
        ```
    - On macOS and Linux:
        ```sh
        source .venv/bin/activate
        ```

## Installing Dependencies

Install the required Python packages using `pip`:
```sh
pip install numpy sounddevice scipy soundfile matplotlib
```

## Running the Application

To run the `main.py` script:
```sh
python main.py
```

## Notes

- Ensure your audio input device (e.g., microphone) is properly configured and working.
- The script will run indefinitely, capturing audio input, printing the volume level, and updating the plot in real-time.
- The plot will display a red horizontal line representing the threshold.
- Audio snapshots and volume data will be saved in the `snapshots` and `data` directories respectively.
```