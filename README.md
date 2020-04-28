# group_1_2020

## Requirements
To use the application run the following commands:

```console
python -m pip install --upgrade pip
pip install -r requirements.txt
```



## Use main application

To use application please run the following command

```console
python -m block_model_cli
```

## Run tests
Tests are automatically ran when a pull request or push is made to the master branch. Also if you want to run the tests
anyway, run the following command

```console
python -m unit_tests
```

##Considerations

While entering the elements that conforms a block model, please enter the 
chemical symbol. (Ej: Gold must be entered as au)\\

Test models are available to load but they cannot be used in the query console

The "Grade in percentage for each mineral function only work for 
block models in http://mansci-web.uai.cl/minelib/kd.xhtml"