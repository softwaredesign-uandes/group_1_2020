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

##Api documentation

###Load a block model

The following structure is an example of what is required to insert a block model in endpoint POST: /api/block_models/
```console

{
"name": "mclaughlin_limit",
"columns": ["id", "x", "y", "z", "ton", "au","destination"],
"minerals": {"au": "proportion", "mass_columns": ["ton"]},
"blocks":
        [
        {
             "id": 0,
             "x": 0,
             "y": 0,
             "z": 0,
             "ton": 30,
             "au": 30,
             "destination": 0
        },
        {"id": 1, "x": 1, "y": 0, "z": 0, "ton": 20, "au": 10, "destination": 1},
        {"id": 2, "x": 2, "y": 0, "z": 0, "ton": 10, "au": 20, "destination": 1},
        {"id": 3, "x": 3, "y": 0, "z": 0, "ton": 40, "au": 10, "destination": 1}
        ]
}
```
If a model has an special form of calculating the grade information, the json has to specify it. Here is an example:
```console

{
"name": "zuck_small",
"columns": ["id", "x", "y", "z", "cost", "value", "rockTonnes", "oreTonnes"],
"minerals": {"mass_columns": ["rockTonnes", "oreTonnes"], "oreTonnes": "special_proportion"},
"blocks":
        [
        {
             "id": 0,
             "x": 0,
             "y": 0,
             "z": 0,
             "cost": 301.97,
             "value": 901.812,
             "rockTonnes": 312,
             "oreTonnes": 45
        },
        {"id": 1, "x": 1, "y": 0, "z": 0, "cost": 2.321, "value": 876.23, "rockTonnes": 987.2, "oreTonnes": 321.43},
        {"id": 2, "x": 2, "y": 0, "z": 0, "cost": 0.3, "value": 0.32, "rockTonnes": 1398, "oreTonnes": 0},
        {"id": 3, "x": 3, "y": 0, "z": 0, "cost": 45.123, "value": 10.32, "rockTonnes": 32.1, "oreTonnes": 312}
        ]
}
```

###Reblock block model

The following structure is an example of what is required to reblock a block model in endpoint POST: /api/block_models/block_model_name/reblock
```console
{
            "rx": 1,
            "ry": 1,
            "rz": 1,
            "continuous_attributes": [
                "blockvalue",
                "ton"
            ],
            "proportional_attributes": {"au": "oz_per_ton"},
            "categorical_attributes": ["destination"],
            "columns_with_mass": ["ton"]
        }
```


