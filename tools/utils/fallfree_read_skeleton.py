import numpy as np
import os
import csv


def read_skeleton(file):
    with open(file, 'r') as f:
        info = list(csv.reader(f))

        skeleton_sequence = {}
        skeleton_sequence['numFrame'] = len(info) // 25
        skeleton_sequence['frameInfo'] = []
        joint_info_key = ['jointName', 'x', 'y', 'z', 'state']

        for f in range(skeleton_sequence['numFrame']):
            frame_info = {}
            frame_info['numBody'] = 1
            frame_info['bodyInfo'] = []

            for b in range(frame_info['numBody']):
                body_info = {}
                body_info['numJoint'] = 25
                body_info['jointInfo'] = []

                for j in range(body_info['numJoint']):
                    joint_info_value = info[25 * f + j]
                    joint_info = {k: v for k, v in zip(joint_info_key, joint_info_value)}

                    body_info['jointInfo'].append(joint_info)
                frame_info['bodyInfo'].append(body_info)
            skeleton_sequence['frameInfo'].append(frame_info)
    return skeleton_sequence


def read_xyz(file, max_body=2, num_joint=25):
    seq_info = read_skeleton(file)
    data = np.zeros((3, seq_info['numFrame'], num_joint, max_body))
    for nf, f in enumerate(seq_info['frameInfo']):
        for nb, b in enumerate(f['bodyInfo']):
            for nj, j in enumerate(b['jointInfo']):
                if nb < max_body and nj < num_joint:
                    data[:, nf, nj, nb] = [j['x'], j['y'], j['z']]
                else:
                    pass
    return data