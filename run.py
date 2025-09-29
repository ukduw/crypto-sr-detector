from support_resistance_detector import level_detector
from parameter_writer import parameter_writer

# rememeber crypto exchanges use UTC


if __name__ == "main":
    levels_dict = level_detector()
    parameter_writer(levels_dict)

