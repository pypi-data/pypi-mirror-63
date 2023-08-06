from core import *
from core import train_gen
from core import test_gen
from core import CNN_model
from core import train_model
from core import plot_data

def test_train_gen():
    assert train_gen()
    return

def test_test_gen():
    assert test_gen()
    return


def test_CNN_model():
    assert CNN_model()
    return

def test_train_model():
    assert train_model()
    return

def plot_data():
    assert plot_data()
    return
