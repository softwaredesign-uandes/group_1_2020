LOADED_MODELS_INFORMATION_FILE_NAME = "models_information.json"
MINERAL_GRADES_INFORMATION_FILE_NAME = "mineral_grades_information.json"
TEST_LOADED_MODELS_INFORMATION_FILE_NAME = "models_information_test.json"
TEST_MINERAL_GRADES_INFORMATION_FILE_NAME = "mineral_grades_information_test.json"
DIFFERENT_UNITS = "ppm percentage oz_per_ton"
MASS_UNIT_FOR_REBLOCK = ["ppm", "percentage", "oz_per_ton", "proportion"]
MATRIX_PROCESS_NAME = "Converting block list to three dimentional matrix"
REBLOCKING_PROCESS_NAME = "Reblocking"
CONVERT_TO_LIST_PROCESS_NAME = "Converting block matrix to block list"
PROCESS_STATES = ["START", "PROCESSING", "COMPLETED"]
COPPER_PROPORTION = "cu_proportion"
GOLD_PROPORTION = "au_proportion"
NOTIFICATION_EVENT_ARGS = notification_event_args = {"actual": None, "total": None,
                                                     "process": None, "state": None}
TYPES_OF_PROPORTION_OPTIONS = ["ppm percentage oz_per_ton", "au_proportion", "cu_proportion"]
MAIN_MENU_VALID_OPTIONS = ["0", "1", "2", "3"]
MAIN_MENU_OPTIONS = ["Load block file", "Open query console", "Reblock model", "Exit"]
QUERY_MENU_VALID_OPTIONS = ["0", "1", "2", "3", "4", "5"]
QUERY_CONSOLE_OPTIONS = ["Block List",
                         "Number of blocks",
                         "Mass of a block",
                         "Grade in percentage for each minerals",
                         "Block attributes",
                         "Exit to main menu"]
ENTER_COLUMNS_OPTIONS = ["0", "1"]
TYPES_OF_COLUMN_ATTRIBUTES = ["Continuous attribute",
                              "Mass Proportional Attribute",
                              "Categorical Attributes",
                              "Exit"]
CONTINUE_SHOWING_OPTIONS = ["y", "n"]
DEFAULT_USER_INPUT = "1"
EXIT_INPUT = "0"
DB_NAME = "block_model.db"
TEST_DB_NAME = "block_model_test.db"

