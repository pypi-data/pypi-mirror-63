from AnyQt import QtCore, QtGui
from AnyQt.QtCore import QThread, pyqtSlot
import Orange.data

import logging

from Orange.widgets.widget import OWWidget
from Orange.widgets.utils.widgetpreview import WidgetPreview
from Orange.widgets.utils.owlearnerwidget import OWBaseLearner
from Orange.base import Learner, Model, SklLearner, SklModel


from Orange.data import ContinuousVariable

from Orange.widgets import gui


from Orange.widgets import settings, gui

from sklearn.cross_decomposition import PLSRegression
from sklearn.model_selection import LeaveOneOut

import Orange.evaluation

import pyqtgraph as pg

from collections import OrderedDict

from functools import partial


import numpy as np

import concurrent.futures
from Orange.widgets.utils.concurrent import (
    ThreadExecutor, FutureWatcher, methodinvoke
)
