# webpage2pdf

This is a repository which could be useful when it's needed to convert some webpages to the pdf files. Now it's working with `xlsx` format.

# Get started

Clone this repository and **create a virtual environment** by running:

```bash 
cd webpage2pdf && python -m venv .
```

Then you need to install the required packages:
```bash 
pip install -r requirements.txt
```

After that place your `.xlsx` file to the `webpage2pdf`, change the name of the file to read in the [main file](main.py#L65) folder and simply run:
```bash
python main.py
```
You should see the `.pdf` files in the `webpage2pdf/pdf_files` directory