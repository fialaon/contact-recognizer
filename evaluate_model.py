import argparse
import random
import h5py
import time
import pickle as pk
import numpy as np
from datetime import datetime
from os import makedirs, remove
from os.path import join, exists, abspath, dirname, basename, isfile

import torch
import torchvision
import torch.nn as nn
import torch.optim as optim
from torch.optim import lr_scheduler
from torch.autograd import Variable
from torchvision import datasets, models, transforms
from sklearn.preprocessing import label_binarize
from sklearn.metrics import precision_recall_curve
from sklearn.metrics import average_precision_score
from sklearn.metrics import roc_curve, auc

from contact_dataset import ContactDataset


def evaluate_model(dataloaders,
                   classes,
                   phase_names,
                   dataset_sizes,
                   model_ft,
                   use_gpu):

    nclasses = 3#len(classes)#TODO: clean up this
    #nclasses = 2#neck
    model_ft.train(False)

    # prepare precision recall curve
    precision_by_phase = dict()
    recall_by_phase = dict()
    ap_by_phase = dict()
    # prepare roc curve
    tpr_by_phase = dict()
    fpr_by_phase = dict()
    roc_auc_by_phase = dict()
    # prepare accuracy
    acc_by_phase = dict()
    # training statistics
    scores_by_phase = dict()
    labels_by_phase = dict()

    for phase in phase_names:
        ncorrects = 0.
        labels_all = -1 * np.ones((0))
        scores_all = -1 * np.ones((0,nclasses))

        # Iterate over data.
        for inputs, labels in dataloaders[phase]:
            # wrap them in Variable
            if use_gpu:
                inputs = Variable(inputs.cuda())
                labels = Variable(labels.cuda())
            else:
                inputs, labels = Variable(inputs), Variable(labels)
            # forward
            outputs = model_ft(inputs)
            outputs = outputs.cpu()
            labels = labels.cpu()
            _, preds = torch.max(outputs.data, 1)
            ncorrects += torch.sum(preds == labels.data)

            labels_all = np.concatenate((labels_all, labels.data.numpy()))
            scores_all = np.concatenate((
                scores_all, outputs.data.numpy()), axis=0)

        # calculate accuracy over all classes
        accuracy = ncorrects / dataset_sizes[phase]

        # calculate PR curve and average precision using scikit-learn
        labels_bin = label_binarize(labels_all, classes=range(3))
        labels_bin = labels_bin[:,:nclasses]

        # precision-recall curve
        precision = dict()
        recall = dict()
        average_precision = dict()
        # roc curve
        fpr = dict()
        tpr = dict()
        roc_auc = dict()
        print(f"PHASE: {phase}")
        # for n in range(nclasses):
        #     name = str(classes[n])
        #     precision[name], recall[name], _ = \
        #         precision_recall_curve(labels_bin[:, n], scores_all[:, n])
        #     average_precision[name] = \
        #         average_precision_score(labels_bin[:, n], scores_all[:, n])
        #     fpr[name], tpr[name], _ = \
        #         roc_curve(labels_bin[:, n], scores_all[:, n])
        #     roc_auc[name] = auc(fpr[name], tpr[name])
        #     print(f"--name: {name}")
        #     print(f"--value: {roc_auc[name]}")

        name = '0'
        n = 0
        precision[name], recall[name], _ = \
            precision_recall_curve(labels_bin[:, n], scores_all[:, n])
        average_precision[name] = \
            average_precision_score(labels_bin[:, n], scores_all[:, n])
        fpr[name], tpr[name], _ = \
            roc_curve(labels_bin[:, n], scores_all[:, n])
        roc_auc[name] = auc(fpr[name], tpr[name])
        print(f"--name: {name}")
        print(f"--value: {roc_auc[name]}")

        acc_by_phase[phase] = accuracy

        precision_by_phase[phase] = precision
        recall_by_phase[phase] = recall
        ap_by_phase[phase] = average_precision

        tpr_by_phase[phase] = tpr
        fpr_by_phase[phase] = fpr
        roc_auc_by_phase[phase] = roc_auc

        scores_by_phase[phase] = scores_all.copy()
        labels_by_phase[phase] = labels_all.copy()

    return acc_by_phase, precision_by_phase, recall_by_phase, ap_by_phase, \
           tpr_by_phase, fpr_by_phase, roc_auc_by_phase, scores_by_phase, labels_by_phase

# import pickle
# import matplotlib.pyplot as plt
# path_res = '/home/ondra/contact-recognizer/our_data.pkl'
# res = pickle.load(open(path_res, 'rb'))
# plt.figure()
# lw = 2
# plt.plot(res[5]['train']['2'], res[4]['train']['2'], color='darkorange',
#          lw=lw, label='ROC curve (area = %0.2f)' % res[6]['train']['2'])
# plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')
# plt.xlim([0.0, 1.0])
# plt.ylim([0.0, 1.05])
# plt.xlabel('False Positive Rate')
# plt.ylabel('True Positive Rate')
# plt.title('Receiver operating characteristic example')
# plt.legend(loc="lower right")
# plt.show()
