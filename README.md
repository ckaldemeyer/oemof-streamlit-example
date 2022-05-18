oemof streamlit example
=======================

The following steps within the cloned repository should start the app under
Windows 10 using `Python 3.9.10`:

```bash
$ virtualenv venv
$ venv\Scripts\activate.bat  # activate.ps on power shell (e.g. in VS Code)
(venv) $ pip install pip-tools
(venv) $ pip-sync
(venv) $ streamlit run app.py
```

The service can be stopped via `CTRL+C` and the environment be deactivated via:

```bash
$ venv\Scripts\deactivate.bat # deactivate.ps on power shell (e.g. in VS Code)
```