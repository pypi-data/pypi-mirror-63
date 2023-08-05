# Keytime
### install keytime
Linux/MacOS: ```pip3 install keytime``` or ```python3 -m install keytime```

Windows: ```pip install keytime``` or ```py -m pip install keytime```

### run keytime
**default:**
```
$ python3
>>> from keytime.keytime import run
>>> run()
```
**interactive:**
```
$ python3
>>> from keytime.keytime import run
>>> run(interactive=True)
```

keytime will now read your keyboard input. By pressing 'Escape', keytime will stop reading your input and display
collected data as a table. Keytime also writes a ```.csv```-file named 'output.csv' if you selected corresponding
settings.

### update 0.1.2
- Reset the collected data after each ```run()``` call
- Adding an interactive environment for saving output.csv