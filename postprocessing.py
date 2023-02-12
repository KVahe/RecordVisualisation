import matplotlib
from matplotlib import pyplot as plt

def create_hist(data: dict, loc_id: tuple, mix_type: str):
    actual_data = data[loc_id[0]][loc_id[1]]
    matplotlib.use('TkAgg')
    xlabel = "Metres" if "throw" in loc_id[0] else "Time"

    if mix_type.upper() == "MIXED":
        figure, axis = plt.subplots(1, 1)
        axis.grid()
        axis.hist(actual_data["Men"]["Mark"].astype(float), color="b", label="Men")
        axis.hist(actual_data["Women"]["Mark"].astype(float), color='r', label="Women")
        axis.set_xlabel(xlabel)
        axis.set_ylabel("Number of Participants")
        axis.set_title(loc_id[1].split("_")[1].capitalize())
        figure.legend()
        figure.show()
