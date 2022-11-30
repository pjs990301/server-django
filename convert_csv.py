import csv
import numpy
from CSIKit.util.csitools import get_CSI
from CSIKit.reader import get_reader

numpy.seterr(divide='ignore')


def round_int(x):
    if x in [float("-inf"), float("inf")]:
        return int(0)
    return int(round(x))


def generate_csv(path: str, dest: str, metric: str = "amplitude"):
    reader = get_reader(path)
    csi_data = reader.read_file(path)

    csi_matrix, no_frames, no_subcarriers = get_CSI(csi_data, metric)
    no_rx, no_tx = csi_matrix.shape[2:]
    # print("CSI Shape: {}".format(csi_matrix.shape))
    # print("Number of Frames: {}".format(no_frames))
    # print("Generating CSI {}...".format(metric))
    # print("CSV dimensions: {} Rows, {} Columns".format(no_frames, no_subcarriers * no_rx * no_tx))

    csv_header = []
    for subcarrier in range(no_subcarriers):
        for rx in range(no_rx):
            for tx in range(no_tx):
                csv_header.append("Subcarrier_{}".format(subcarrier + 1))
    with open(dest, "w", newline="") as csv_file:
        writer = csv.writer(csv_file, delimiter=",")
        writer.writerow(csv_header)

        # 프레임이 존재하는 동안 그 정도를 작성
        for frame in range(no_frames):
            frame_data = csi_matrix[frame]
            row_data = []
            for subcarrier in range(no_subcarriers):
                subcarrier_data = frame_data[subcarrier]
                for rx in range(no_rx):
                    rx_data = subcarrier_data[rx]
                    for tx in range(no_tx):
                        tx_data = rx_data[tx]
                        tx_data = round_int(tx_data)
                        row_data.append(tx_data)

            writer.writerow(row_data)

        # 프레임의 크기가 500이 아닌 경우 500까지 0으로 채워주기
        if no_frames != 500:
            for i in range(no_frames, 500):
                for subcarrier in range(no_subcarriers):
                    for rx in range(no_rx - 1):
                        tx_data = 0
                        row_data.append(tx_data)
                writer.writerow(row_data)

    # print("File written to: {}".format(dest))
