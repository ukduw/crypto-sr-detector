from support_resistance_detector import level_detector
from parameter_writer import parameter_writer
from log_writer import log_writer


if __name__ == "__main__":
    levels_dict = level_detector()
    parameter_writer(levels_dict)
    log_writer(levels_dict)

